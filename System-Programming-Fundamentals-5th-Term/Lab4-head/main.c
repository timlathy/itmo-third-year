#define _POSIX_C_SOURCE 2
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

#define BUF_SIZE 8192

void print_lines_buffered(FILE* src, unsigned int lines_requested) {
  unsigned int lines_printed = 0;
  char inbuf[BUF_SIZE];

  while (fgets(inbuf, BUF_SIZE, src) == inbuf) {
    for (unsigned int i = 0; i < BUF_SIZE; ++i) {
      if (inbuf[i] == '\n') {
        fwrite(inbuf, i + 1, 1, stdout);
        if (++lines_printed == lines_requested)
          return;
      }
      else if (inbuf[i] == '\0') {
        if (i > 0 && inbuf[i - 1] != '\n')
          fwrite(inbuf, i + 1, 1, stdout);
        break;
      }
    }
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
            exit(EXIT_FAILURE);
        }
    }
  }

  print_lines_buffered(stdin, num_lines);
  return 0;
}
