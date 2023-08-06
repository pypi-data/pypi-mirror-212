#include <algorithm>
#include <filesystem>
#include <initializer_list>
#include <iostream>
#include <set>
#include <sstream>
#include <streambuf>
#include <string>
#include <string_view>
#include <type_traits>
#include <vector>

#include <cerrno>
#include <cstdio>
#include <cstring>
#include <dirent.h>
#include <fcntl.h>
#include <grp.h>
#include <mntent.h>
#include <net/if.h>
#include <poll.h>
#include <pwd.h>
#include <sched.h>
#include <signal.h>
#include <sys/ioctl.h>
#include <sys/mount.h>
#include <sys/prctl.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

const int WORKER_STACK_SIZE = 30 * 1024;
char worker_stack[WORKER_STACK_SIZE];

std::string image_root;
std::vector<std::tuple<char *, char *, std::string_view>> bind_mounts;
uid_t root_uid;
gid_t root_gid;
std::string size_limit;
std::string work_dir = "/";
int notify_fd;
std::vector<std::pair<char *, char *>> env;
std::vector<char *> program_argv;

int child_pidfd = -1;

std::set<std::string> rebind_readonly;

#define REINTR(expr)                                                           \
  ({                                                                           \
    decltype((expr)) _value;                                                   \
    do {                                                                       \
      errno = 0;                                                               \
      _value = (expr);                                                         \
    } while (errno == EINTR);                                                  \
    _value;                                                                    \
  })

#define CHECK(expr, msg, ...)                                                  \
  check(expr, #expr, [&]() { std::cerr << msg << std::endl; }, {__VA_ARGS__})

template <typename T, typename F>
T check(T ret, const char *text, F error_reporter,
        std::initializer_list<int> allowed_codes = {}) {
  T err_val;
  if constexpr (std::is_pointer_v<T>) {
    err_val = nullptr;
  } else if constexpr (std::is_integral_v<T>) {
    err_val = -1;
  } else {
    static_assert(sizeof(T) < 0, "CHECK cannot handle this type");
  }
  if (ret == err_val && std::find(allowed_codes.begin(), allowed_codes.end(),
                                  errno) == allowed_codes.end()) {
    std::cerr << "Check failed at " << text << ": " << strerror(errno)
              << " (errno " << errno << "): ";
    error_reporter();
    std::exit(1);
  }
  return ret;
}

int pidfd_open(pid_t pid, unsigned int flags) {
  return syscall(SYS_pidfd_open, pid, flags);
}
int pidfd_send_signal(int pidfd, int sig, siginfo_t *info, unsigned int flags) {
  return syscall(SYS_pidfd_send_signal, pidfd, sig, info, flags);
}
int pivot_root(const char *new_root, const char *put_old) {
  return syscall(SYS_pivot_root, new_root, put_old);
}

void bind_mount(std::string_view source, std::string_view target,
                unsigned long flags = 0) {
  CHECK(mount(source.data(), target.data(), nullptr, MS_BIND | flags, nullptr),
        "Failed to bind-mount " << source << " to " << target);
}

void set_propagation(unsigned long flags) {
  CHECK(mount("none", "/", nullptr, flags, nullptr),
        "Failed to set mountns propagation");
}

void mount_tmpfs(std::string_view target, mode_t mode = 0,
                 std::string_view size = {}) {
  std::filesystem::create_directories(target);
  std::stringstream opts_ss;
  opts_ss << "uid=" << root_uid << ",gid=" << root_gid;
  if (mode != 0) {
    opts_ss << ",mode=" << std::oct << mode << std::dec;
  }
  if (!size.empty()) {
    opts_ss << ",size=" << size;
  }
  auto opts = opts_ss.str();
  CHECK(mount("tmp", target.data(), "tmpfs", 0, opts.c_str()),
        "Failed to mount tmpfs at " << target);
}

void chown_recursive(std::string_view path, uid_t uid, gid_t gid) {
  CHECK(lchown(path.data(), uid, gid),
        "Failed to chown " << path << " to " << uid << ":" << gid);
  std::unique_ptr<DIR, decltype(&closedir)> dir{
      CHECK(opendir(path.data()), "Failed to open " << path), closedir};
  dirent *entry;
  while (entry = readdir(dir.get())) {
    if (std::strcmp(entry->d_name, ".") == 0 ||
        std::strcmp(entry->d_name, "..") == 0) {
      continue;
    }
    std::string file_path(path);
    file_path += '/';
    file_path += entry->d_name;
    if (entry->d_type == DT_DIR) {
      chown_recursive(file_path, uid, gid);
    } else {
      CHECK(lchown(file_path.c_str(), uid, gid),
            "Failed to chown " << file_path << " to " << uid << ":" << gid);
    }
  }
}

void auto_bind_mount(const std::filesystem::path &source,
                     std::string_view target_rel, unsigned long flags = 0) {
  std::string target = "/mnt/";
  target += target_rel;
  target = std::filesystem::weakly_canonical(target).string();
  bool need_mount;
  if (std::filesystem::is_symlink(source)) {
    std::filesystem::copy_symlink(source, target);
    need_mount = false;
  } else if (std::filesystem::is_directory(source)) {
    std::filesystem::create_directories(target);
    need_mount = true;
  } else {
    int fd = CHECK(open(target.c_str(), O_WRONLY | O_CREAT),
                   "Failed to create " << target);
    CHECK(close(fd), "Failed to close " << target);
    need_mount = true;
  }
  CHECK(lchown(target.c_str(), root_uid, root_gid),
        "Failed to chown " << target << " to " << root_uid << ":" << root_gid);
  if (need_mount) {
    bind_mount(source.string(), target, flags & ~MS_RDONLY);
    if (flags & MS_RDONLY) {
      rebind_readonly.insert(std::move(target));
    }
  }
}

void mount_bind_mounts() {
  for (auto [source, target_rel, options] : bind_mounts) {
    unsigned long flags = 0;
    if (options == "ro") {
      flags = MS_RDONLY;
    } else if (options != "") {
      std::cerr << "Invalid volume option " << options << std::endl;
      std::exit(1);
    }
    auto_bind_mount(source, target_rel, flags);
  }

  std::unique_ptr<FILE, decltype(&endmntent)> f{
      CHECK(setmntent("/proc/mounts", "r"), "Failed to open /proc/mounts"),
      endmntent};
  mntent *entry;
  while (entry = getmntent(f.get())) {
    if (rebind_readonly.count(entry->mnt_dir)) {
      // util-linux does not set these additional flags. util-linux is wrong.
      unsigned long flags = MS_BIND | MS_REMOUNT | MS_RDONLY;
      if (hasmntopt(entry, "nodev")) {
        flags |= MS_NODEV;
      }
      if (hasmntopt(entry, "nosuid")) {
        flags |= MS_NOSUID;
      }
      if (hasmntopt(entry, "noexec")) {
        flags |= MS_NOEXEC;
      }

      CHECK(mount("none", entry->mnt_dir, nullptr, flags, nullptr),
            "Failed to remount " << entry->mnt_dir << " as read-only");
    }
  }
}

void mount_proc() {
  CHECK(mkdir("/mnt/proc", 0777), "Failed to mkdir /mnt/proc", EEXIST);
  CHECK(mount("proc", "/mnt/proc", "proc", 0, nullptr),
        "Failed to mount procfs at /mnt/proc");
}

void mount_dev() {
  CHECK(mkdir("/mnt/dev", 0755), "Failed to mkdir /mnt/dev", EEXIST);
  CHECK(mkdir("/mnt/dev/shm", 01777), "Failed to mkdir /mnt/dev/shm", EEXIST);

  // XXX: on default configuration, mqueue may store up to 20 MB memory. Do we
  // want to limit that?
  CHECK(mkdir("/mnt/dev/mqueue", 0777), "Failed to mkdir /mnt/dev/mqueue");
  CHECK(mount("mqueue", "/mnt/dev/mqueue", "mqueue", 0, nullptr),
        "Failed to mount mqueue at /mnt/dev/mqueue");

  CHECK(mkdir("/mnt/dev/pts", 0777), "Failed to mkdir /mnt/dev/pts");
  CHECK(mount("devpts", "/mnt/dev/pts", "devpts", 0, nullptr),
        "Failed to mount devpts at /mnt/dev/pts");

  std::filesystem::create_symlink("/proc/self/fd/0", "/mnt/dev/stdin");
  std::filesystem::create_symlink("/proc/self/fd/1", "/mnt/dev/stdout");
  std::filesystem::create_symlink("/proc/self/fd/2", "/mnt/dev/stderr");
  std::filesystem::create_directory_symlink("/proc/self/fd", "/mnt/dev/fd");
  std::filesystem::create_symlink("/proc/kcore", "/mnt/dev/core");
  std::filesystem::create_symlink("pts/ptmx", "/mnt/dev/ptmx");

  chown_recursive("/mnt/dev", root_uid, root_gid);

  for (const char *path : std::initializer_list<const char *>{
           "/dev/null", "/dev/zero", "/dev/full", "/dev/random",
           "/dev/urandom"}) {
    auto_bind_mount(path, path);
  }
}

void setup_mntns() {
  set_propagation(MS_REC | MS_PRIVATE);

  mount_tmpfs("/mnt", 0755, size_limit);

  for (auto name : std::initializer_list<const char *>{"upperdir", "workdir"}) {
    std::string target = "/mnt/";
    target += name;
    CHECK(mkdir(target.c_str(), 0755), "Failed to create " << target);
    CHECK(chown(target.c_str(), root_uid, root_gid),
          "Failed to chown " << target << " to " << root_uid << ":"
                             << root_gid);
  }

  // Do I love shadowing mountpoints!
  std::stringstream opts_ss;
  opts_ss << "lowerdir=" << image_root
          << ",upperdir=/mnt/upperdir,workdir=/mnt/workdir,metacopy=on";
  auto opts = opts_ss.str();
  CHECK(mount("overlay", "/mnt", "overlay", 0, opts.c_str()),
        "Failed to mount tmpfs at /mnt");

  mount_proc();
  mount_dev();

  CHECK(mkdir("/mnt/run", 0755), "Failed to mkdir /mnt/run", EEXIST);
  CHECK(chown("/mnt/run", root_uid, root_gid),
        "Failed to chown /mnt/run to " << root_uid << ":" << root_gid);

  CHECK(mkdir("/mnt/tmp", 01777), "Failed to mkdir /mnt/tmp", EEXIST);
  CHECK(chown("/mnt/tmp", root_uid, root_gid),
        "Failed to chown /mnt/tmp to " << root_uid << ":" << root_gid);

  mount_bind_mounts();
}

void bring_interface_up(std::string_view name) {
  int fd = CHECK(socket(AF_INET, SOCK_DGRAM, 0), "Failed to open socket");

  ifreq ifr;
  std::memset(&ifr, 0, sizeof(ifr));
  std::memcpy(ifr.ifr_name, name.data(), name.size());

  ifr.ifr_flags |= IFF_UP;
  CHECK(ioctl(fd, SIOCSIFFLAGS, &ifr),
        "Failed to bring interface " << name << " up");

  CHECK(close(fd), "Failed to close socket");
}

uid_t resolve_uid(const std::string &name) {
  if (name.find_first_not_of("0123456789") == std::string::npos) {
    return std::stoi(name);
  } else {
    std::unique_ptr<FILE, decltype(&fclose)> f{
        CHECK(fopen("/mnt/etc/passwd", "r"), "Failed to open /mnt/etc/passwd"),
        fclose};
    passwd *user;
    while (user = fgetpwent(f.get())) {
      if (name == user->pw_name) {
        return user->pw_uid;
      }
    }
    std::cerr << "Unknown user " << name << std::endl;
    std::exit(1);
  }
}

gid_t resolve_gid(const std::string &name) {
  if (name.find_first_not_of("0123456789") == std::string::npos) {
    return std::stoi(name);
  } else {
    std::unique_ptr<FILE, decltype(&fclose)> f{
        CHECK(fopen("/mnt/etc/group", "r"), "Failed to open /mnt/etc/group"),
        fclose};
    group *group;
    while (group = fgetgrent(f.get())) {
      if (name == group->gr_name) {
        return group->gr_gid;
      }
    }
    std::cerr << "Unknown group " << name << std::endl;
    std::exit(1);
  }
}

void write_map(pid_t pid, const char *name,
               const std::vector<std::tuple<int, int, int>> &maps) {
  std::stringstream ss;
  for (auto &[a, b, cnt] : maps) {
    ss << a << '\t' << b << '\t' << cnt << '\n';
  }
  auto buf = ss.str();
  auto path = "/proc/" + std::to_string(pid) + "/" + name;
  int fd = CHECK(open(path.c_str(), O_WRONLY),
                 "Failed to open "
                     << path
                     << ". This may be caused by an earlier worker's failure");
  CHECK(write(fd, buf.c_str(), buf.size()), "Failed to write to " << path);
  CHECK(close(fd), "Failed to close " << path);
}

void show_usage(char **argv) {
  std::cerr << "Usage: " << argv[0]
            << " -R<image root> [-b<bind source>:<bind target>]* -u<root uid> "
               "-g<root gid> [-s<tmpfs size limit>] [-U<setuid inside box>] "
               "[-G<setgid inside box>] [-w<workdir>] [-N<notify fd>] "
               "[-E<name>=<value>]* <command> <args...>"
            << std::endl;
  std::exit(1);
}

int main(int argc, char **argv, char** envp) {
  std::string sandbox_user = "0", sandbox_group = "0";

  int opt;
  while ((opt = getopt(argc, argv, ":R:b:u:g:s:U:G:w:N:E:")) != -1) {
    switch (opt) {
    case 'R':
      image_root = optarg;
      break;
    case 'b': {
      char *source = optarg;
      char *colon = strchr(source, ':');
      if (colon == nullptr) {
        show_usage(argv);
      }
      *colon = '\0';
      char *target = colon + 1;
      colon = strchr(target, ':');
      std::string_view options;
      if (colon != nullptr) {
        *colon = '\0';
        options = colon + 1;
      }
      bind_mounts.emplace_back(source, target, options);
      break;
    }
    case 'u':
      root_uid = std::atoi(optarg);
      break;
    case 'g':
      root_gid = std::atoi(optarg);
      break;
    case 's':
      size_limit = optarg;
      break;
    case 'U':
      sandbox_user = optarg;
      break;
    case 'G':
      sandbox_group = optarg;
      break;
    case 'w':
      work_dir = optarg;
      break;
    case 'N':
      notify_fd = std::atoi(optarg);
      break;
    case 'E':
      char* p = std::strchr(optarg, '=');
      if(p == nullptr) {
        std::cerr << "No value is set to environment variable " << optarg << std::endl;
        return 1;
      }
      *p = '\0';
      env.emplace_back(optarg, p + 1);
      break;
    case '?':
      std::cerr << "Unknown option -" << optopt << std::endl;
      return 1;
    case ':':
      std::cerr << "Option -" << optopt << " requires an argument" << std::endl;
      return 1;
    }
  }
  if (optind == argc || image_root.empty() || root_uid == 0 || root_gid == 0 ||
      sandbox_user.empty() || sandbox_group.empty() || work_dir.empty()) {
    show_usage(argv);
  }

  char **p = argv + optind;
  while (*p) {
    program_argv.push_back(*p++);
  }
  program_argv.push_back(nullptr);

  CHECK(unshare(CLONE_NEWCGROUP | CLONE_NEWNS | CLONE_NEWNET | CLONE_NEWIPC |
                CLONE_NEWUTS),
        "Failed to unshare namespaces");

  setup_mntns();


  int info_pipe[2];
  int userns_block_pipe[2];
  CHECK(pipe2(info_pipe, O_CLOEXEC), "Failed to create info pipe");
  CHECK(pipe2(userns_block_pipe, O_CLOEXEC), "Failed to create userns block pipe");

  for(int fd: std::initializer_list<int>{info_pipe[1], userns_block_pipe[0]}) {
    CHECK(fcntl(info_pipe[1], F_SETFD, CHECK(fcntl(info_pipe[1], F_GETFD), "Failed to get flags of fd") | FD_CLOEXEC), "Failed to set flags of fd");
  }

  auto info_fd = std::to_string(info_pipe[1]);
  auto userns_block_fd = std::to_string(userns_block_pipe[0]);
  auto sandbox_uid = std::to_string(resolve_uid(sandbox_user));
  auto sandbox_gid = std::to_string(resolve_gid(sandbox_group));

  std::vector<const char*> bwrap_argv{
    "bwrap",
    "--unshare-user", 
               "--info-fd", info_fd.c_str(), "--userns-block-fd", userns_block_fd.c_str(), "--unshare-net",
               "--dev-bind", "/mnt", "/", "--uid", sandbox_uid.c_str(), "--gid",
               sandbox_gid.c_str(), "--die-with-parent", "--as-pid-1", "--chdir", work_dir, "--clearenv"
  };
  for(auto [name, value]: env) {
    bwrap_argv.push_back("--setenv");
    bwrap_argv.push_back(name);
    bwrap_argv.push_back(value);
  }
  bwrap_argv.push_back(nullptr);

  if(CHECK(fork(), "Failed to fork") > 0) {
    CHECK(execvp("bwrap", bwrap_argv.data()), "Failed to run bwrap");
    return 1;
  }
  int bwrap_pid = getppid();

  CHECK(close(info_pipe[1]), "Failed to close pipe end");
  CHECK(close(userns_block_pipe[0]), "Failed to close pipe end");

  // The fact that this is hacky does not mean there is a cleaner solution--this is C++ for you
  std::string info;
  {
    std::ifstream info_file("/proc/self/fd/" + std::to_string(info_pipe[0]));
    std::stringstream info_ss;
    info_ss << info_file.rdbuf();
    info = info_ss.str();
    if(!info_file) {
      std::cerr << "Failed to read info from bwrap" << std::endl;
      return 1;
    }
  }

  std::cerr << info << std::endl;

  // Map nobody/nogroup inside the sandbox too
  write_map(
      child_pid, "uid_map",
      {{0, root_uid, 1}, {1, 1, root_uid - 1}, {root_uid, root_uid + 1, 1}});
  // setgroups must be allowed for PHP and others to work
  write_map(
      child_pid, "gid_map",
      {{0, root_gid, 1}, {1, 1, root_gid - 1}, {root_gid, root_gid + 1, 1}});
  close(ctl_pipe2[1]);
  CHECK(read(ctl_pipe3[0], &buf, 1), "Failed to await child's notification");

  // For the user's convenience
  CHECK(setns(child_pidfd, CLONE_NEWNS | CLONE_NEWUSER),
        "Failed to move to worker's mount and user namespaces");

  if (notify_fd != 0) {
    char buf = '+';
    CHECK(write(notify_fd, &buf, 1),
          "Failed to notify the parent process of successful exec");
    CHECK(close(notify_fd), "Failed to close notification pipe");
  }

  siginfo_t info;
  CHECK(REINTR(waitid(P_PIDFD, child_pidfd, &info, WEXITED)),
        "Failed to wait for child");
  if (info.si_code == CLD_EXITED) {
    return info.si_status;
  } else if (info.si_code == CLD_KILLED) {
    return 128 + info.si_status;
  } else {
    return 255;
  }
}
