#define _DEFAULT_SOURCE // rwlock
#include "error.h"
#include <unistd.h>
#include <pthread.h>

volatile char letters[26];
#ifdef MUTEX
pthread_mutex_t letters_mutex = PTHREAD_MUTEX_INITIALIZER;
#endif
#ifdef RWLOCK
pthread_rwlock_t letters_lock = PTHREAD_RWLOCK_INITIALIZER;
#endif

void* invert_case_thread(void* arg) {
  while (1) {
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
  while (1) {
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

int main(int argc, char** argv) {
  for (int i = 0; i < 26; ++i)
    letters[i] = 'a' + i;

  pthread_t invcase_thrd, reverse_thrd;

  ERR_RET(pthread_create(&invcase_thrd, NULL, invert_case_thread, NULL));
  ERR_RET(pthread_create(&reverse_thrd, NULL, reverse_thread, NULL));

  while (1) {
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

    sleep(1);
  }

  return 0;
}
