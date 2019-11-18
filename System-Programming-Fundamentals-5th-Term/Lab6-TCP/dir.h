#pragma once

#include <sys/types.h>
#include <dirent.h>

void print_dir(int fd, const char* dirname) {
  errno = 0;
  DIR* dir = opendir(dirname);
  if (errno != 0) {
    dprintf(fd, "Failed to open %s: %s\r\n\r\n", dirname, strerror(errno));
    errno = 0;
    return;
  }

  dprintf(fd, "Contents of %s:\r\n", dirname);

  struct dirent* ent;
  while ((ent = readdir(dir)) != NULL)
    dprintf(fd, "%s\r\n", ent->d_name);

  dprintf(fd, "\r\n");
  closedir(dir);
}
