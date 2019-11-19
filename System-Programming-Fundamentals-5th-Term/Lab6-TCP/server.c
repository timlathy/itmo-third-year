#define _POSIX_C_SOURCE 200809L // dprintf
#include <unistd.h>
#include <stdlib.h>
#include <stdbool.h>
#include <pthread.h>
#include <sys/socket.h>
#include <netinet/in.h>

#include "error.h"
#include "dir.h"

#define CLIENT_BUFSIZE 512

// Protocol definition:
//
// <request> ::= <path> { <path> } CR LF
// <path> ::= <non-empty string not including NUL or CR or LF> CR LF

const char MALFORMED_REQ_ERR[] = "Malformed request: "
  "make sure you're sending at least one path, "
  "each path on a separate line, each line terminated by CRLF, "
  "and the request terminated by an empty line.\r\n";

char* read_request(int fd, int* request_len) {
  char* request = NULL;
  *request_len = 0;

  char buf[CLIENT_BUFSIZE];
  int bytes_read;
  while ((bytes_read = read(fd, buf, CLIENT_BUFSIZE)) > 0) {
    request = realloc(request, *request_len + bytes_read);
    memcpy(request + *request_len, buf, bytes_read);
    *request_len += bytes_read;

    if (*request_len < 2) continue;
    if (request[*request_len - 2] == '\r' && request[*request_len - 1] == '\n') {
      if (*request_len == 2)
        goto malformed;
      if (*request_len > 4 && request[*request_len - 4] == '\r' && request[*request_len - 3] == '\n') {
        *request_len -= 1;
        return request;
      }
    }
  }

malformed:
  write(fd, MALFORMED_REQ_ERR, sizeof(MALFORMED_REQ_ERR) - 1);
  free(request);
  return NULL;
}

void* process_request(void* fdptr) {
  int fd = *(int*)fdptr;
  printf("Client connected: %d\n", fd);

  int request_len;
  char* paths = read_request(fd, &request_len);
  if (!paths)
    goto connection_end;

  char* path_start = paths;
  for (char* path_end = paths; path_end < paths + request_len; ++path_end) {
    if (*path_end == '\r') {
      *path_end = '\0';
      print_dir(fd, path_start);
      path_end += 2; // skip LF
      path_start = path_end;
    }
  }

  dprintf(fd, "\r\n");

connection_end:
  close(fd);
  return NULL;
}

bool try_parse_ushort(const char* str, unsigned short* val) {
  errno = 0;
  char* endptr;
  *val = strtoul(str, &endptr, 10);
  return *str != '-' && errno == 0 && endptr != str && *endptr == '\0';
}

int main(int argc, char** argv) {
  unsigned short port;
  if (argc != 2 || !try_parse_ushort(argv[1], &port)) {
    fprintf(stderr, "Usage: %s port\n", argv[0]);
    return 1;
  }

  int sockfd;
  CHK_ERRNO(sockfd = socket(AF_INET, SOCK_STREAM, 0));

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

    pthread_t client_thrd;
    ERR_RET(pthread_create(&client_thrd, NULL, process_request, &clientfd));
  }

  return 0;
}
