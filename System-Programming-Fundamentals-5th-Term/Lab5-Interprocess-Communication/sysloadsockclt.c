#define _DEFAULT_SOURCE
#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>

#include <sys/un.h>
#include <sys/types.h>
#include <sys/socket.h>

#include "error.h"
#include "sysloadsock.h"

int main(unused(int argc), unused(char** argv)) {
  int sockfd;
  CHK_ERRNO(sockfd = socket(AF_UNIX, SOCK_STREAM, 0));

  struct sockaddr_un sockaddr;
  sockaddr.sun_family = AF_UNIX;
  strncpy(sockaddr.sun_path, LAB_SOCK_PATH, sizeof(sockaddr.sun_path) - 1);
  unsigned int sockaddr_len = sizeof(struct sockaddr_un);

  CHK_ERRNO(connect(sockfd, (const struct sockaddr *) &sockaddr, sockaddr_len));

  server_state_t state;
  CHK_ERRNO(read(sockfd, &state, sizeof(server_state_t)));

  printf("Connected to server with pid=%jd, uid=%jd, gid=%jd\n",
      (intmax_t) state.pid, (intmax_t) state.uid, (intmax_t) state.gid);
  printf("Load average:\n  1 minute: %.2lf\n  5 minutes: %.2lf\n  15 minutes: %.2lf\n",
      state.loadavg[0], state.loadavg[1], state.loadavg[2]);

  close(sockfd);

  return 0;
}
