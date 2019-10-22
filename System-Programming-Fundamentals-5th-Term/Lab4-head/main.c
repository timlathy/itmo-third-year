#include <stdio.h>

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

int main(int argc, char** argv) {
  print_lines_buffered(stdin, 10);
  return 0;
}
