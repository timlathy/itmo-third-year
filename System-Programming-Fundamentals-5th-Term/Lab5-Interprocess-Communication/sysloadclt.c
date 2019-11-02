#include "sysload.h"

#include <unistd.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

// IPC
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/msg.h>

int query_server(ipc_mode_t mode, int ipc_id) {
  server_state_t* state;
  msgbuf_t msg;

  switch (mode) {
    case M_SHMEM:
      state = (server_state_t*) shmat(ipc_id, NULL, SHM_RDONLY);
      DIE_ON_ERRNO("Unable to access the server's shared memory region");
      break;
    case M_MSGQ:
      msg.mtype = MSGTYPE_QUERY;
      msgsnd(ipc_id, &msg, 0, 0);
      DIE_ON_ERRNO("Unable to send a query message");

      msgrcv(ipc_id, &msg, sizeof(server_state_t), MSGTYPE_REPLY, 0);
      DIE_ON_ERRNO("Unable to receive a reply message");

      state = malloc(sizeof(server_state_t));
      memcpy(state, msg.mtext, sizeof(server_state_t));
      break;
    case M_UNDEF:
      return 1;
  }

  printf("Connected to server with pid=%jd, uid=%jd, gid=%jd\n",
      (intmax_t) state->srv_pid, (intmax_t) state->srv_uid, (intmax_t) state->srv_gid);
  printf("Load average:\n  1 minute: %.2lf\n  5 minutes: %.2lf\n  15 minutes: %.2lf\n",
      state->loadavg[0], state->loadavg[1], state->loadavg[2]);

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
    "  -s srvmemid: connect to a server using System V shared memory with ID srvmemid\n"\
    "  -q srvmqid: connect to a server using System V message queue with ID srvmqid\n"

  int c;
  int ipc_id;
  ipc_mode_t mode = M_UNDEF;
  while ((c = getopt(argc, argv, "s:q:")) != EOF) {
    switch (c) {
      case 's':
        if (!try_parse_int(optarg, &ipc_id)) {
          fprintf(stderr, "%s: invalid shared memory ID: '%s'\n", argv[0], optarg);
          return 1;
        }
        mode = M_SHMEM;
        break;
      case 'q':
        if (!try_parse_int(optarg, &ipc_id)) {
          fprintf(stderr, "%s: invalid message queue ID: '%s'\n", argv[0], optarg);
          return 1;
        }
        mode = M_MSGQ;
        break;
    }
  }
  if (mode == M_UNDEF) {
    fprintf(stderr, USAGE, argv[0]);
    return 1;
  }

  return query_server(mode, ipc_id);
}
