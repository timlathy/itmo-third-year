#define _POSIX_C_SOURCE 2
#include <unistd.h>

#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>

#define BUF_SIZE 4096

void print_lines_buffered(int fd, unsigned int num_lines) {
  unsigned int printed = 0;

  char inbuf[BUF_SIZE];
  int bytes_read;
  while (printed < num_lines && (bytes_read = read(fd, inbuf, BUF_SIZE)) > 0) {
    unsigned int pos;
    for (pos = 0; pos < bytes_read; ++pos)
      if (inbuf[pos] == '\n' && ++printed == num_lines) break;

    write(STDOUT_FILENO, inbuf, pos + 1);
  }
}

int try_parse_uint(const char* str, unsigned int* val) {
  char* endptr;
  *val = strtoul(str, &endptr, 10);
  return endptr != str && *endptr == '\0';
}

int main(int argc, char** argv) {
  unsigned int num_lines = 10;

  int c;
  while ((c = getopt(argc, argv, "n:")) != EOF) {
    switch (c) {
      case 'n':
        if (!try_parse_uint(optarg, &num_lines)) {
            fprintf(stderr, "%s: invalid number of lines: '%s'\n", argv[0], optarg);
            return 1;
        }
    }
  }

  if (optind == argc)
    print_lines_buffered(STDIN_FILENO, num_lines);
  else
    do {
      int fd = open(argv[optind], O_RDONLY);
      if (fd == -1) {
        fprintf(stderr, "%s: Cannot open %s for reading", argv[0], argv[optind]);
      }
      else {
        print_lines_buffered(fd, num_lines);
        close(fd);
      }
    }
    while (++optind < argc);

  return 0;
}
