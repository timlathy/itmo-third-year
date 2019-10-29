#include "sysload.h"

#include <stdint.h>

// Shared memory
#include <sys/ipc.h>
#include <sys/shm.h>

int main(int argc, char** argv) {
  int srvmemid;
  if (argc != 2 || sscanf(argv[1], "%d", &srvmemid) != 1) {
    fprintf(stderr, "Usage: %s srvmemid\n  where srvmemid is the server's shared region id\n", argv[0]);
    return 1;
  }

  server_state_t* state = (server_state_t*) shmat(srvmemid, NULL, SHM_RDONLY);
  DIE_ON_ERRNO("Unable to access the server's shared memory region");

  printf("Connected to server with pid=%jd, uid=%jd, gid=%jd\n",
      (intmax_t) state->srv_pid, (intmax_t) state->srv_uid, (intmax_t) state->srv_gid);
  printf("Load average:\n  1 minute: %.2lf\n  5 minutes: %.2lf\n  15 minutes: %.2lf\n",
      state->loadavg[0], state->loadavg[1], state->loadavg[2]);

  return 0;
}
