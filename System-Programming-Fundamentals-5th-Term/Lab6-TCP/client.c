#define _POSIX_C_SOURCE 200112L // getaddrinfo()
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>

#include "error.h"

#define READ_BUFSIZE 512

const char CRLF[] = "\r\n";

int make_request(int serverfd, int argc, char **argv) {
  for (int i = 3; i < argc; ++i) {
    write(serverfd, argv[i], strlen(argv[i]));
    write(serverfd, CRLF, sizeof(CRLF));
  }
  write(serverfd, CRLF, sizeof(CRLF));

  char buf[READ_BUFSIZE];
  int bytes_read;
  while ((bytes_read = read(serverfd, buf, READ_BUFSIZE)) > 0) {
    write(STDOUT_FILENO, buf, bytes_read);
  }

  close(serverfd);
  return 0;
}

int main(int argc, char** argv) {
  if (argc < 4) {
    fprintf(stderr, "Usage: %s host port [paths...]\n", argv[0]);
    return 1;
  }

  struct addrinfo hints = {
    .ai_family = AF_INET, .ai_socktype = SOCK_STREAM, .ai_protocol = IPPROTO_TCP
  };
  struct addrinfo *addr;
  int err;
  if ((err = getaddrinfo(argv[1], argv[2], &hints, &addr)) != 0) {
    fprintf(stderr, "Failed to resolve host: %s\n", gai_strerror(err));
    return 1;
  }

  // getaddrinfo() returns a list of addresses, we need to try each one until
  // we find the correct one.
  int sockfd = 0;
  for (struct addrinfo* a = addr; a != NULL; a = a->ai_next) {
    if ((sockfd = socket(a->ai_family, a->ai_socktype, a->ai_protocol)) == -1)
      continue;
    if (connect(sockfd, a->ai_addr, a->ai_addrlen) == 0)
      break;
    sockfd = close(sockfd);
  }
  if (sockfd <= 0) {
    fprintf(stderr, "Unable to connect to %s:%s\n", argv[1], argv[2]);
    return 1;
  }
  freeaddrinfo(addr);

  return make_request(sockfd, argc, argv); 
}
