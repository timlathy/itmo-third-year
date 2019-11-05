#include <errno.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <pthread.h>

#ifdef SEM_POSIX
#include <semaphore.h>

typedef struct { char* letters; sem_t sem_begin; sem_t sem_end; } thread_data_t;
#endif

#ifdef SEM_SYSV
typedef struct { char* letters; sem_t sem_begin; sem_t sem_end; } thread_data_t;
#endif

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

void* invert_case_posix_sem_thread(void* arg) {
  thread_data_t* data = (thread_data_t*) arg;

  while (1) {
    T_CHK_ERRNO(sem_wait(&data->sem_begin));

    int case_incr = data->letters[0] == 'a' ? -32 : 32; // 'a' - 32 = 'A', 'A' + 32 = 'a'
    for (int i = 0; i < 26; ++i)
      data->letters[i] += case_incr;

    T_CHK_ERRNO(sem_post(&data->sem_end));
  }
}

void* reverse_posix_sem_thread(void* arg) {
  thread_data_t* data = (thread_data_t*) arg;

  while (1) {
    T_CHK_ERRNO(sem_wait(&data->sem_begin));

    for (int i = 0; i < 26 / 2; ++i) {
        int temp = data->letters[i];
        data->letters[i] = data->letters[25 - i];
        data->letters[25 - i] = temp;
    }

    T_CHK_ERRNO(sem_post(&data->sem_end));
  }
}

int main(int argc, char** argv) {
  volatile char letters[26];
  for (int i = 0; i < 26; ++i)
    letters[i] = 'a' + i;

  pthread_t invcase_thrd, reverse_thrd;

  thread_data_t invcase_thrd_data = { .letters = letters };
  CHK_ERRNO(sem_init(&invcase_thrd_data.sem_begin, 0, 0));
  CHK_ERRNO(sem_init(&invcase_thrd_data.sem_end, 0, 0));

  thread_data_t reverse_thrd_data = { .letters = letters };
  CHK_ERRNO(sem_init(&reverse_thrd_data.sem_begin, 0, 0));
  CHK_ERRNO(sem_init(&reverse_thrd_data.sem_end, 0, 0));

  if (pthread_create(&invcase_thrd, NULL, invert_case_posix_sem_thread, &invcase_thrd_data) != 0 ||
      pthread_create(&reverse_thrd, NULL, reverse_posix_sem_thread, &reverse_thrd_data) != 0) {
    fprintf(stderr, "Unable to create a thread\n");
    return 1;
  }

  int thread = 0;

  while (1) {
    thread_data_t* tdata = thread == 0 ? &invcase_thrd_data : &reverse_thrd_data;
    thread = !thread;

    CHK_ERRNO(sem_post(&tdata->sem_begin));
    CHK_ERRNO(sem_wait(&tdata->sem_end));

    for (int i = 0; i < 26; ++i)
      printf("%c", letters[i]);
    printf("\n");

    sleep(1);
  }

  return 0;
}
