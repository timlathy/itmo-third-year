#define _POSIX_C_SOURCE 2
#define _DEFAULT_SOURCE // getloadavg
#include <sys/types.h>
#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
// Shared memory
#include <sys/ipc.h>
#include <sys/shm.h>

typedef struct {
  pid_t srv_pid;
  uid_t srv_uid;
  gid_t srv_gid;
  double loadavg[3];
} server_state_t;

int run_sysv_shmem_server(pid_t pid, uid_t uid, gid_t gid) {
  int shmemid = shmget(IPC_PRIVATE, sizeof(server_state_t), IPC_CREAT | 0444);
  if (shmemid == -1)
    return 1;

  void* shmem = shmat(shmemid, NULL, 0);
  if (shmem == (void*) -1)
    return 1;

  server_state_t* state = (server_state_t*)shmem;
  state->srv_pid = pid;
  state->srv_uid = uid;
  state->srv_gid = gid;

  printf("Shared memory id: %d\n", shmemid);

  while (1) {
    getloadavg(state->loadavg, 3);
    sleep(1);
  }

  return 0;
}

int main(int argc, char** argv) {
  pid_t pid = getpid();
  uid_t uid = getuid();
  gid_t gid = getgid();

  printf("Started a server with pid=%jd, uid=%jd, gid=%jd\n",
      (intmax_t) pid, (intmax_t) uid, (intmax_t) gid);

  return run_sysv_shmem_server(pid, uid, gid);
}
