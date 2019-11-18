#include <unistd.h>
#include <stdlib.h>
#include <stdbool.h>
#include <sys/socket.h>
#include <netinet/in.h>

#include "error.h"

#define CLIENT_BUFSIZE 512

// Protocol definition:
//
// <request> ::= <path> { <path> } CR LF
// <path> ::= <non-empty string not including NUL or CR or LF> CR LF

int handle_client(int fd) {
  char* request = NULL;

  char buf[CLIENT_BUFSIZE];
  int bytes_read, request_len = 0;
  while ((bytes_read = read(fd, buf, CLIENT_BUFSIZE)) > 0) {
    request = realloc(request, request_len + bytes_read);
    memcpy(request + request_len, buf, bytes_read);
    request_len += bytes_read;

    if (request_len < 2) continue;
    if (request[request_len - 2] == '\r' && request[request_len - 1] == '\n') {
      if (request_len == 2) {
        fprintf(stderr, "Malformed request: empty pathstr recieved\n");
        return 1;
      }
      else if (request_len > 4 && request[request_len - 4] == '\r' && request[request_len - 3] == '\n') {
        request_len -= 1;
        break;
      }
    }
  }

  char* path_start = request;
  for (char* path_end = request; path_end < request + request_len; ++path_end) {
    if (*path_end == '\r') {
      *path_end = '\0';
      printf("Directory: [%s]\n", path_start);
      path_end += 2; // skip LF
      path_start = path_end;
    }
  }

  return 0;
}

bool try_parse_ushort(const char* str, unsigned short* val) {
  errno = 0;
  char* endptr;
  *val = strtoul(str, &endptr, 10);
  return *str != '-' && errno == 0 && endptr != str && *endptr == '\0';
}

int main(int argc, char** argv) {
  int sockfd;
  CHK_ERRNO(sockfd = socket(AF_INET, SOCK_STREAM, 0));

  unsigned short port;
  if (argc != 2 || !try_parse_ushort(argv[1], &port)) {
    fprintf(stderr, "Usage: %s port\n", argv[0]);
    return 1;
  }

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
  CHK_ERRNO(listen(sockfd, 2)); // TODO: tweak the backlog -- what should it be set to?

  printf("Listening on %d\n", port);

  while (1) {
    int clientfd;
    CHK_ERRNO(clientfd = accept(sockfd, NULL, NULL));

    printf("Client connected: %d\n", clientfd);
    ERR_RET(handle_client(clientfd));

    CHK_ERRNO(close(clientfd));
  }

  return 0;
}
