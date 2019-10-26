#define _POSIX_C_SOURCE 2
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

#define BUF_SIZE 4096
#define MAX_ARG_SIZE 1024 * 1024

void read_arg_string(char* arg_buf) {
  unsigned int args_pos = strlen(arg_buf);

  char inbuf[BUF_SIZE];
  int bytes_read;
  while (args_pos < MAX_ARG_SIZE - 1 &&
          (bytes_read = read(STDIN_FILENO, inbuf, BUF_SIZE)) > 0)
    for (int pos = 0; pos < bytes_read && args_pos < MAX_ARG_SIZE - 1; ++pos)
      arg_buf[args_pos++] = inbuf[pos] == '\n' ? ' ' : inbuf[pos];
}

int main(int argc, char** argv) {
  char* arg_string = calloc(1, MAX_ARG_SIZE);

  if (argc == 1) {
    strcat(arg_string, "echo ");
  }
  else {
    for (int i = 1; i < argc; ++i) {
      strcat(arg_string, argv[i]);
      strcat(arg_string, " ");
    }
  }

  read_arg_string(arg_string);
  return system(arg_string);
}
