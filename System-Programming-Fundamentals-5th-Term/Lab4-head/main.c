#define _POSIX_C_SOURCE 2
#include <unistd.h>

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <stdbool.h>

#define BUF_SIZE 4096

void print_lines_buffered(int fd, unsigned int num_lines) {
  unsigned int printed = 0;

  char inbuf[BUF_SIZE];
  int bytes_read;
  while (printed < num_lines && (bytes_read = read(fd, inbuf, BUF_SIZE)) > 0) {
    unsigned int pos;
    for (pos = 0; pos < bytes_read; ++pos)
      if (inbuf[pos] == '\n' && ++printed == num_lines) break;

    write(STDOUT_FILENO, inbuf, pos);
  }

  write(STDOUT_FILENO, "\n", sizeof("\n"));
}

bool try_parse_uint(const char* str, unsigned int* val) {
  char* endptr;
  *val = strtoul(str, &endptr, 10);
  return endptr != str && *endptr == '\0';
}

void handle_filename_args(int argc, char** argv, int num_lines) {
  // According to POSIX,
  // If multiple file operands are specified, head shall precede the output for each with the header:
  // "\n==> %s <==\n", <pathname>
  // except that the first header written shall not include the initial <newline>.
  #define HEADER_START "==> "
  #define HEADER_END " <==\n"
  #define HEADER_STDIN HEADER_START "standard input" HEADER_END

  bool first_header = true;
  do {
    if (first_header)
      first_header = false;
    else
      write(STDOUT_FILENO, "\n", sizeof("\n"));

    if (*argv[optind] == '-') {
      write(STDOUT_FILENO, HEADER_STDIN, sizeof(HEADER_STDIN));
      print_lines_buffered(STDIN_FILENO, num_lines);
    }
    else {
      int fd = open(argv[optind], O_RDONLY);
      if (fd == -1) {
        fprintf(stderr, "%s: Cannot open %s for reading", argv[0], argv[optind]);
      }
      else {
        write(STDOUT_FILENO, HEADER_START, sizeof(HEADER_START));
        write(STDOUT_FILENO, argv[optind], strlen(argv[optind]));
        write(STDOUT_FILENO, HEADER_END, sizeof(HEADER_END));
        print_lines_buffered(fd, num_lines);
        close(fd);
      }
    }
  }
  while (++optind < argc);
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
    handle_filename_args(argc, argv, num_lines);

  return 0;
}
