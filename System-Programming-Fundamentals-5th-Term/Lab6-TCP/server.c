#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

#include "error.h"

int main(int argc, char** argv) {
  int sockfd;
  CHK_ERRNO(sockfd = socket(AF_INET, SOCK_STREAM, 0));

  int port = 9090;
  int backlog = 2;

  struct sockaddr_in srv_addr = {
    .sin_family = AF_INET,
    .sin_addr = {
      // `INADDR_ANY` = listen on all addresses, `htonl` converts
      // host byte order (little-endian on x86) to network order (big-endian)
      .s_addr = htonl(INADDR_ANY)
    },
    .sin_port = htons(port)
  };
  CHK_ERRNO(bind(sockfd, (struct sockaddr*) &srv_addr, sizeof(struct sockaddr_in)));
  CHK_ERRNO(listen(sockfd, backlog));

  while (1) {
    int clientfd;
    CHK_ERRNO(clientfd = accept(sockfd, NULL, NULL));

    printf("Client connected: %d\n", clientfd);

    CHK_ERRNO(close(clientfd));
  }

  return 0;
}
