#pragma once

#include <errno.h>
#include <string.h>
#include <stdio.h>

#define CHK_ERRNO(expr) GEN_CHK_ERRNO(expr, int)
#define T_CHK_ERRNO(expr) GEN_CHK_ERRNO(expr, void*)

#define GEN_CHK_ERRNO(expr, ty) do {\
  expr;\
  if (errno != 0) {\
    fprintf(stderr, "%s:%d: Encountered an error, %s\n",\
        __FILE__, __LINE__, strerror(errno));\
    return (ty)1;\
  }\
} while (0)
