#define _DEFAULT_SOURCE // getloadavg
#include "sysload.h"

#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>

// IPC
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/msg.h>
#include <sys/mman.h>
#include <fcntl.h>

int run_sysv_shmem_server(pid_t pid, uid_t uid, gid_t gid, time_t starttime) {
  errno = 0;

  int shmemid = shmget(IPC_PRIVATE, sizeof(server_state_t), IPC_CREAT | 0644);
  DIE_ON_ERRNO("Unable to allocate a shared memory region");

  void* shmem = shmat(shmemid, NULL, 0);
  DIE_ON_ERRNO("Unable to access the shared memory region");

  server_state_t* state = (server_state_t*)shmem;
  state->srv_pid = pid;
  state->srv_uid = uid;
  state->srv_gid = gid;

  printf("Using System V shared memory, id: %d\n", shmemid);

  while (1) {
    getloadavg(state->loadavg, 3);
    state->runtime = difftime(time(NULL), starttime);
    sleep(1);
  }

  return 0;
}

int run_sysv_msgq_server(pid_t pid, uid_t uid, gid_t gid, time_t starttime) {
  errno = 0;

  int mqid = msgget(IPC_PRIVATE, IPC_CREAT | 0644);
  DIE_ON_ERRNO("Unable to create a message queue");

  server_state_t state;
  state.srv_pid = pid;
  state.srv_uid = uid;
  state.srv_gid = gid;

  printf("Using System V message queue, id: %d\n", mqid);

  while (1) {
    msgbuf_t msg;
    msgrcv(mqid, &msg, 0, MSGTYPE_QUERY, 0);
    DIE_ON_ERRNO("Unable to receive an incoming query message");

    getloadavg(state.loadavg, 3);
    state.runtime = difftime(time(NULL), starttime);

    msg.mtype = MSGTYPE_REPLY;
    memcpy(msg.mtext, &state, sizeof(server_state_t));

    msgsnd(mqid, &msg, sizeof(server_state_t), 0);
    DIE_ON_ERRNO("Unable to send a reply message");
  }

  return 0;
}

int run_mmap_server(pid_t pid, uid_t uid, gid_t gid, time_t starttime, const char* file) {
  int fd = open(file, O_CREAT | O_RDWR, 0644);
  DIE_ON_ERRNO("Unable to open the shared file for writing");

  ftruncate(fd, sizeof(server_state_t));
  DIE_ON_ERRNO("Unable to open the shared file for writing");

  server_state_t* state = (server_state_t*) mmap(NULL, sizeof(server_state_t),
    PROT_WRITE, MAP_SHARED, fd, 0);
  DIE_ON_ERRNO("Unable to mmap the shared file");

  state->srv_pid = pid;
  state->srv_uid = uid;
  state->srv_gid = gid;

  printf("Using memory-mapped file %s\n", file);

  while (1) {
    getloadavg(state->loadavg, 3);
    state->runtime = difftime(time(NULL), starttime);
    sleep(1);
  }

  return 0;
}

int main(int argc, char** argv) {
  #define USAGE "Usage: %s mode, where mode is either of:\n"\
    "  -s: use System V shared memory\n"\
    "  -q: use System V message queue\n"\
    "  -m filename: use memory-mapped file\n"

  int c;
  ipc_mode_t mode = M_UNDEF;
  char* ipc_filename = NULL;
  while ((c = getopt(argc, argv, "sqm:")) != EOF) {
    switch (c) {
      case 's': mode = M_SHMEM; break;
      case 'q': mode = M_MSGQ; break;
      case 'm':
        ipc_filename = malloc(strlen(optarg));
        strcpy(ipc_filename, optarg);
        mode = M_MMAP;
        break;
    }
  }
  if (mode == M_UNDEF) {
    fprintf(stderr, USAGE, argv[0]);
    return 1;
  }

  pid_t pid = getpid();
  uid_t uid = getuid();
  gid_t gid = getgid();
  time_t starttime = time(NULL);

  printf("Started a server with pid=%jd, uid=%jd, gid=%jd\n",
      (intmax_t) pid, (intmax_t) uid, (intmax_t) gid);

  switch (mode) {
    case M_SHMEM: return run_sysv_shmem_server(pid, uid, gid, starttime);
    case M_MSGQ: return run_sysv_msgq_server(pid, uid, gid, starttime);
    case M_MMAP: return run_mmap_server(pid, uid, gid, starttime, ipc_filename);
    case M_UNDEF: return 1; // unreachable
  }
}
