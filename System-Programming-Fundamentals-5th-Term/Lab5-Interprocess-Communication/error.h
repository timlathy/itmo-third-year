#pragma once

#include <errno.h>
#include <string.h>
#include <stdio.h>

#define CHK_ERRNO(expr) GEN_CHK_ERRNO(expr, return 1)
#define T_CHK_ERRNO(expr) GEN_CHK_ERRNO(expr, pthread_exit((void*)1))

#define GEN_CHK_ERRNO(expr, err_ret_expr) do {\
  expr;\
  if (errno != 0) {\
    fprintf(stderr, "%s:%d: Encountered an error, %s\n",\
        __FILE__, __LINE__, strerror(errno));\
    err_ret_expr;\
  }\
} while (0)

#define ERR_RET(expr) GEN_ERR_RET(expr, return 1)
#define T_ERR_RET(expr) GEN_ERR_RET(expr, pthread_exit((void*)1))

#define GEN_ERR_RET(expr, err_ret_expr) do {\
  int __ret__ = expr;\
  if (__ret__ != 0) {\
    fprintf(stderr, "%s:%d: Encountered an error, %s\n",\
        __FILE__, __LINE__, strerror(__ret__));\
    err_ret_expr;\
  }\
} while (0)

