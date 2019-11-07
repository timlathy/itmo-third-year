#define _DEFAULT_SOURCE // getloadavg
#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>

#include <sys/un.h>
#include <sys/types.h>
#include <sys/socket.h>

#include "error.h"
#include "sysloadsock.h"

int main(int argc, char** argv) {
  server_state_t state = { .pid = getpid(), .uid = getuid(), .gid = getgid() };

  printf("Started a server with pid=%jd, uid=%jd, gid=%jd\n",
      (intmax_t) state.pid, (intmax_t) state.uid, (intmax_t) state.gid);

  int sockfd;
  CHK_ERRNO(sockfd = socket(AF_UNIX, SOCK_STREAM, 0));
  
  struct sockaddr_un sockaddr;
  sockaddr.sun_family = AF_UNIX;
  strncpy(sockaddr.sun_path, LAB_SOCK_PATH, sizeof(sockaddr.sun_path) - 1);
  int sockaddr_len = sizeof(struct sockaddr_un);

  CHK_ERRNO(bind(sockfd, (const struct sockaddr *) &sockaddr, sockaddr_len));
  CHK_ERRNO(listen(sockfd, 0));

  puts("Listening on socket " LAB_SOCK_PATH);

  while (1) {
    int cltfd;
    CHK_ERRNO(cltfd = accept(sockfd, (struct sockaddr *) &sockaddr, sockaddr_len));
  }

  return 0;
}
