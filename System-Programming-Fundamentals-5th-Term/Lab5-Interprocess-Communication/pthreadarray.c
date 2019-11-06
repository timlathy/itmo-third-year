#include "error.h"
#include <pthread.h>

volatile char letters[26];
pthread_mutex_t letters_mutex;

void* invert_case_thread(void* arg) {
  while (1) {
    T_ERR_RET(pthread_mutex_lock(&letters_mutex));

    int case_incr = letters[0] >= 'a' ? -32 : 32; // 'a' - 32 = 'A', 'A' + 32 = 'a'
    for (int i = 0; i < 26; ++i)
      letters[i] += case_incr;

    T_ERR_RET(pthread_mutex_unlock(&letters_mutex));

    sleep(1);
  }
}

void* reverse_thread(void* arg) {
  while (1) {
    sleep(1);

    T_ERR_RET(pthread_mutex_lock(&letters_mutex));

    for (int i = 0; i < 26 / 2; ++i) {
        int temp = letters[i];
        letters[i] = letters[25 - i];
        letters[25 - i] = temp;
    }

    T_ERR_RET(pthread_mutex_unlock(&letters_mutex));
  }
}

int main(int argc, char** argv) {
  for (int i = 0; i < 26; ++i)
    letters[i] = 'a' + i;

  pthread_t invcase_thrd, reverse_thrd;

  ERR_RET(pthread_mutex_init(&letters_mutex, NULL));
  ERR_RET(pthread_create(&invcase_thrd, NULL, invert_case_thread, NULL));
  ERR_RET(pthread_create(&reverse_thrd, NULL, reverse_thread, NULL));

  while (1) {
    ERR_RET(pthread_mutex_lock(&letters_mutex));

    for (int i = 0; i < 26; ++i)
      printf("%c", letters[i]);
    printf("\n");

    ERR_RET(pthread_mutex_unlock(&letters_mutex));

    sleep(1);
  }

  return 0;
}
