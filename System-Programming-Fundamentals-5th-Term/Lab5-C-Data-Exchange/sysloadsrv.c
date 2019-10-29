#define _POSIX_C_SOURCE 2
#include <sys/types.h>
#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>

typedef struct {
  pid_t srv_pid;
  uid_t srv_uid;
  gid_t srv_gid;
} server_state_t;

int main(int argc, char** argv) {
  server_state_t state;
  state.srv_pid = getpid();
  state.srv_uid = getuid();
  state.srv_gid = getgid();

  printf("Started a server with pid=%jd, uid=%jd, gid=%jd\n",
      (intmax_t) state.srv_pid, (intmax_t) state.srv_uid, (intmax_t) state.srv_gid);

  return 0;
}
