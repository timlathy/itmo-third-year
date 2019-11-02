#pragma once

#define _POSIX_C_SOURCE 2
#include <sys/types.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>

typedef struct {
  pid_t srv_pid;
  uid_t srv_uid;
  gid_t srv_gid;
  double loadavg[3];
} server_state_t;

typedef enum { M_UNDEF, M_SHMEM, M_MSGQ, M_MMAP } ipc_mode_t;

#define MSGTYPE_QUERY 1
#define MSGTYPE_REPLY 2
typedef struct {
  long mtype;
  char mtext[sizeof(server_state_t)];
} msgbuf_t;

#define DIE_ON_ERRNO(errmsg) if (errno != 0) {\
  fprintf(stderr, "%s: %s\n", errmsg, strerror(errno));\
  return 1;\
}
