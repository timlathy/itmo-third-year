#include "sysload.h"

#include <unistd.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

// IPC
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/msg.h>
#include <sys/mman.h>
#include <fcntl.h>

int query_sysv_shmem_server(int ipc_id, server_state_t** state_pp) {
  *state_pp = (server_state_t*) shmat(ipc_id, NULL, SHM_RDONLY);
  DIE_ON_ERRNO("Unable to access the server's shared memory region");
  return 0;
}

int query_sysv_msgq_server(int ipc_id, server_state_t** state_pp) {
  msgbuf_t msg;
  msg.mtype = MSGTYPE_QUERY;
  msgsnd(ipc_id, &msg, 0, 0);
  DIE_ON_ERRNO("Unable to send a query message");

  msgrcv(ipc_id, &msg, sizeof(server_state_t), MSGTYPE_REPLY, 0);
  DIE_ON_ERRNO("Unable to receive a reply message");

  *state_pp = (server_state_t*) malloc(sizeof(server_state_t));
  memcpy(*state_pp, msg.mtext, sizeof(server_state_t));
  return 0;
}

int query_mmap_server(const char* file, server_state_t** state_pp) {
  int fd = open(file, O_RDONLY);
  DIE_ON_ERRNO("Unable to open the shared file for reading");

  *state_pp = (server_state_t*) mmap(NULL, sizeof(server_state_t),
    PROT_READ, MAP_SHARED, fd, 0);
  DIE_ON_ERRNO("Unable to mmap the shared file");
  return 0;
}

bool try_parse_int(const char* str, int* val) {
  errno = 0;
  char* endptr;
  *val = strtol(str, &endptr, 10);
  return errno == 0 && endptr != str && *endptr == '\0';
}

int main(int argc, char** argv) {
  #define USAGE "Usage: %s mode, where mode is either of:\n"\
    "  -s srvmemid: connect to the server using System V shared memory with ID srvmemid\n"\
    "  -q srvmqid: connect to the server using System V message queue with ID srvmqid\n"\
    "  -m file: connect to the server using a memory-mapped file\n"

  int c, ipc_id;
  server_state_t* state = NULL;

  while ((c = getopt(argc, argv, "s:q:m:")) != EOF) {
    switch (c) {
      case 's':
        if (!try_parse_int(optarg, &ipc_id)) {
          fprintf(stderr, "%s: invalid shared memory ID: '%s'\n", argv[0], optarg);
          return 1;
        }
        if (query_sysv_shmem_server(ipc_id, &state) != 0) return 1;
        break;
      case 'q':
        if (!try_parse_int(optarg, &ipc_id)) {
          fprintf(stderr, "%s: invalid message queue ID: '%s'\n", argv[0], optarg);
          return 1;
        }
        if (query_sysv_msgq_server(ipc_id, &state) != 0) return 1;
        break;
      case 'm':
        if (query_mmap_server(optarg, &state) != 0) return 1;
        break;
    }
  }
  if (!state) {
    fprintf(stderr, USAGE, argv[0]);
    return 1;
  }

  printf("Connected to server with pid=%jd, uid=%jd, gid=%jd\n",
      (intmax_t) state->srv_pid, (intmax_t) state->srv_uid, (intmax_t) state->srv_gid);
  printf("Load average:\n  1 minute: %.2lf\n  5 minutes: %.2lf\n  15 minutes: %.2lf\n",
      state->loadavg[0], state->loadavg[1], state->loadavg[2]);

  return 0;
}
