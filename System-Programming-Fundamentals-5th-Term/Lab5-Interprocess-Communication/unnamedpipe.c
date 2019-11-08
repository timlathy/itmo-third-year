#define _DEFAULT_SOURCE
#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>

#include <fcntl.h>

#include "error.h"

#define BUF_SIZE 4096

// Source: https://stackoverflow.com/a/46477080/1726690
void pack_even_bytes(uint8_t* __restrict__ dst, const uint16_t* __restrict__ src, size_t bytes) {
  uint8_t* end = dst + bytes;
  do *dst++ = *src++ >> 8;
  while (dst < end);
}

int pipe_file(int fd, int pipefd) {
  char inbuf[BUF_SIZE];
  char pipebuf[BUF_SIZE / 2];

  int bytes_read;
  while ((bytes_read = read(fd, inbuf, BUF_SIZE)) > 0) {
    pack_even_bytes((uint8_t*)pipebuf, (const uint16_t*)inbuf, bytes_read);
    CHK_ERRNO(write(pipefd, pipebuf, bytes_read / 2));
  }
  CHK_ERRNO(close(pipefd));
  return 0;
}

int main(int argc, char** argv) {
  if (argc != 2) {
    fprintf(stderr, "Usage: %s file\n", argv[0]);
    return 1;
  }

  int file;
  CHK_ERRNO(file = open(argv[1], O_RDONLY));

  int pipefd[2];
  CHK_ERRNO(pipe(pipefd));
  int pipefd_rd = pipefd[0];
  int pipefd_wr = pipefd[1];

  int wc_pid = fork();
  if (wc_pid == 0) {
    /* Child process */
    CHK_ERRNO(close(pipefd_wr));
    CHK_ERRNO(dup2(pipefd_rd, STDIN_FILENO));
    CHK_ERRNO(execlp("wc", "wc", "-c", (char*)NULL));
  }
  else {
    CHK_ERRNO(close(pipefd_rd));
    /* Parent process */
    return pipe_file(file, pipefd_wr);
  }
}
