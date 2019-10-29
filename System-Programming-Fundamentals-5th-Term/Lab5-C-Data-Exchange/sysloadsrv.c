#define _DEFAULT_SOURCE // getloadavg
#include "sysload.h"

#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>

// Shared memory
#include <sys/ipc.h>
#include <sys/shm.h>

int run_sysv_shmem_server(pid_t pid, uid_t uid, gid_t gid) {
  errno = 0;

  int shmemid = shmget(IPC_PRIVATE, sizeof(server_state_t), IPC_CREAT | 0644);
  DIE_ON_ERRNO("Unable to allocate a shared memory region");

  void* shmem = shmat(shmemid, NULL, 0);
  DIE_ON_ERRNO("Unable to access the shared memory region");

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
