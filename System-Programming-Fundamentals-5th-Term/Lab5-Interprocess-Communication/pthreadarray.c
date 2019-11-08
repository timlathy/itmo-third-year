#define _DEFAULT_SOURCE // rwlock
#include "error.h"
#include <unistd.h>
#include <stdbool.h>
#include <stdlib.h>
#include <pthread.h>

char letters[26];

#ifdef MUTEX
pthread_mutex_t letters_mutex = PTHREAD_MUTEX_INITIALIZER;
#endif
#ifdef RWLOCK
pthread_rwlock_t letters_lock = PTHREAD_RWLOCK_INITIALIZER;
#endif

void* invcase_thread(void* arg) {
  unsigned int interval = *(unsigned int*)arg;
  while (1) {
    usleep(interval);

#ifdef MUTEX
    T_ERR_RET(pthread_mutex_lock(&letters_mutex));
#endif
#ifdef RWLOCK
    T_ERR_RET(pthread_rwlock_wrlock(&letters_lock));
#endif

    int case_incr = letters[0] >= 'a' ? -32 : 32; // 'a' - 32 = 'A', 'A' + 32 = 'a'
    for (int i = 0; i < 26; ++i)
      letters[i] += case_incr;

#ifdef MUTEX
    T_ERR_RET(pthread_mutex_unlock(&letters_mutex));
#endif
#ifdef RWLOCK
    T_ERR_RET(pthread_rwlock_unlock(&letters_lock));
#endif
  }
}

void* reverse_thread(void* arg) {
  unsigned int interval = *(unsigned int*)arg;
  while (1) {
    usleep(interval);

#ifdef MUTEX
    T_ERR_RET(pthread_mutex_lock(&letters_mutex));
#endif
#ifdef RWLOCK
    T_ERR_RET(pthread_rwlock_wrlock(&letters_lock));
#endif

    for (int i = 0; i < 26 / 2; ++i) {
        int temp = letters[i];
        letters[i] = letters[25 - i];
        letters[25 - i] = temp;
    }

#ifdef MUTEX
    T_ERR_RET(pthread_mutex_unlock(&letters_mutex));
#endif
#ifdef RWLOCK
    T_ERR_RET(pthread_rwlock_unlock(&letters_lock));
#endif
  }
}

#ifdef RWLOCK
void* uppercnt_thread(void* arg) {
  unsigned int interval = *(unsigned int*)arg;
  while (1) {
    usleep(interval);

    T_ERR_RET(pthread_rwlock_rdlock(&letters_lock));

    int uppercase = 0;
    for (int i = 0; i < 26; ++i)
      if (letters[0] <= 'Z') uppercase++;

    printf("Upper case letters: %d\n", uppercase);

    T_ERR_RET(pthread_rwlock_unlock(&letters_lock));
  }
}
#endif

bool try_parse_uint(const char* str, unsigned int* val) {
  errno = 0;
  char* endptr;
  *val = strtoul(str, &endptr, 10);
  return errno == 0 && endptr != str && *endptr == '\0';
}

int main(int argc, char** argv) {
  unsigned int invcase_interval, reverse_interval, print_interval;
#ifdef RWLOCK
  unsigned int uppercnt_interval;
  if (argc != 5
      || !try_parse_uint(argv[4], &uppercnt_interval)
#endif
#ifdef MUTEX
  if (argc != 4
#endif
      || !try_parse_uint(argv[1], &invcase_interval)
      || !try_parse_uint(argv[2], &reverse_interval)
      || !try_parse_uint(argv[3], &print_interval)) {
    fprintf(stderr, "Usage: %s invcase_int reverse_int print_int"
#ifdef RWLOCK
      " uppercnt_int"
#endif
      "\n    (intervals are expresssed in microseconds)\n", argv[0]);
    return 1;
  }

  for (int i = 0; i < 26; ++i)
    letters[i] = 'a' + i;

  pthread_t invcase_thrd, reverse_thrd;
  ERR_RET(pthread_create(&invcase_thrd, NULL, invcase_thread, &invcase_interval));
  ERR_RET(pthread_create(&reverse_thrd, NULL, reverse_thread, &reverse_interval));

#ifdef RWLOCK
  pthread_t uppercnt_thrd;
  ERR_RET(pthread_create(&uppercnt_thrd, NULL, uppercnt_thread, &uppercnt_interval));
#endif

  while (1) {
    usleep(print_interval);

#ifdef MUTEX
    ERR_RET(pthread_mutex_lock(&letters_mutex));
#endif
#ifdef RWLOCK
    ERR_RET(pthread_rwlock_rdlock(&letters_lock));
#endif

    char out[27];
    memcpy(out, letters, 26);
    out[26] = '\0';
    puts(out);

#ifdef MUTEX
    ERR_RET(pthread_mutex_unlock(&letters_mutex));
#endif
#ifdef RWLOCK
    ERR_RET(pthread_rwlock_unlock(&letters_lock));
#endif
  }

  return 0;
}
