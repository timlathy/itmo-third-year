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

#define DIE_ON_ERRNO(errmsg) if (errno != 0) {\
  fprintf(stderr, "%s: %s\n", errmsg, strerror(errno));\
  return 1;\
}
