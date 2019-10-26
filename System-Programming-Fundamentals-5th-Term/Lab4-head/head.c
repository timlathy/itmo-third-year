#define _POSIX_C_SOURCE 2
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <stdbool.h>
#include <stdarg.h>
#include <errno.h>

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
  errno = 0;
  char* endptr;
  *val = strtoul(str, &endptr, 10);
  return *str != '-' && errno == 0 && endptr != str && *endptr == '\0';
}

// An fprintf()-like wrapper over write().
// Rationale: the assignment requires we only use raw syscalls to perform IO.
void fdprintf(int fd, const char* fmt, ...) {
  #define MSG_BUF_SIZE 512
  char buf[MSG_BUF_SIZE];
  va_list args;
  va_start(args, fmt);
  int msg_len = vsnprintf(buf, MSG_BUF_SIZE, fmt, args);
  va_end(args);
  write(fd, buf, msg_len < MSG_BUF_SIZE ? msg_len : MSG_BUF_SIZE);
}

void handle_filename_args(int argc, char** argv, int num_lines) {
  // According to POSIX,
  // If multiple file operands are specified, head shall precede the output for each with the header:
  // "\n==> %s <==\n", <pathname>
  // except that the first header written shall not include the initial <newline>.
  #define HEADER_STDIN "\n==> standard input <==\n"
  #define HEADER_FILE_FMT "\n==> %s <==\n"

  bool first_header = true;
  do {
    int header_offset = first_header ? 1 : 0;
    first_header = false;

    if (*argv[optind] == '-') {
      write(STDOUT_FILENO, HEADER_STDIN + header_offset, sizeof(HEADER_STDIN) - header_offset);
      print_lines_buffered(STDIN_FILENO, num_lines);
    }
    else {
      errno = 0;
      int fd = open(argv[optind], O_RDONLY);
      if (fd == -1) {
        const char* error_fmt = "%s: Cannot open %s for reading\n";
        switch (errno) {
          case EACCES:
            error_fmt = "%s: Cannot open %s for reading (access denied)\n";
            break;
          case ENOENT:
            error_fmt = "%s: Cannot open %s for reading (file not found)\n";
            break;
        }
        fdprintf(STDERR_FILENO, error_fmt, argv[0], argv[optind]);
      }
      else {
        fdprintf(STDOUT_FILENO, HEADER_FILE_FMT + header_offset, argv[optind]);
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
          fdprintf(STDERR_FILENO, "%s: invalid number of lines: '%s'\n", argv[0], optarg);
          return 1;
        }
        break;
      case '?':
        fdprintf(STDERR_FILENO, "Usage: %s [-n num-lines] [file...]\n", argv[0]);
        return 1;
    }
  }

  if (optind == argc)
    print_lines_buffered(STDIN_FILENO, num_lines);
  else
    handle_filename_args(argc, argv, num_lines);

  return 0;
}
