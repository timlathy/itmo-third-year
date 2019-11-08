#pragma once

#define LAB_SOCK_PATH "/tmp/spf-lab5-sysload-sock"

typedef struct __attribute__((__packed__)) {
  pid_t pid;
  uid_t uid;
  gid_t gid;
  double runtime;
  double loadavg[3];
} server_state_t;
