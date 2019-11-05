#include "error.h"
#include <unistd.h>
#include <pthread.h>

#ifdef SEM_POSIX
#include <semaphore.h>

typedef struct { char* letters; sem_t sem_begin; sem_t sem_end; } thread_data_t;
#endif

#ifdef SEM_SYSV
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>

typedef struct { char* letters; int sem_id; } thread_data_t;

void sysv_wait_sem(int sem_id, int sem_num) {
  struct sembuf op[2] = {
    { .sem_num = sem_num, .sem_op = 0, .sem_flg = 0 }, // wait for zero
    { .sem_num = sem_num, .sem_op = 1, .sem_flg = 0 }  // increment
  };
  semop(sem_id, op, 2);
}

void sysv_signal_sem(int sem_id, int sem_num) {
  struct sembuf op = { .sem_num = sem_num, .sem_op = -1, .sem_flg = 0 };
  semop(sem_id, &op, 1);
}
#endif

void* invert_case_posix_sem_thread(void* arg) {
  thread_data_t* data = (thread_data_t*) arg;

  while (1) {
#ifdef SEM_POSIX
    T_CHK_ERRNO(sem_wait(&data->sem_begin));
#endif
#ifdef SEM_SYSV
    T_CHK_ERRNO(sysv_wait_sem(data->sem_id, 0)); // sem #0 = begin
#endif

    int case_incr = data->letters[0] == 'a' ? -32 : 32; // 'a' - 32 = 'A', 'A' + 32 = 'a'
    for (int i = 0; i < 26; ++i)
      data->letters[i] += case_incr;

#ifdef SEM_POSIX
    T_CHK_ERRNO(sem_post(&data->sem_end));
#endif
#ifdef SEM_SYSV
    T_CHK_ERRNO(sysv_signal_sem(data->sem_id, 1)); // sem #1 = end
#endif
  }
}

void* reverse_posix_sem_thread(void* arg) {
  thread_data_t* data = (thread_data_t*) arg;

  while (1) {
#ifdef SEM_POSIX
    T_CHK_ERRNO(sem_wait(&data->sem_begin));
#endif
#ifdef SEM_SYSV
    T_CHK_ERRNO(sysv_wait_sem(data->sem_id, 0)); // sem #0 = begin
#endif

    for (int i = 0; i < 26 / 2; ++i) {
        int temp = data->letters[i];
        data->letters[i] = data->letters[25 - i];
        data->letters[25 - i] = temp;
    }

#ifdef SEM_POSIX
    T_CHK_ERRNO(sem_post(&data->sem_end));
#endif
#ifdef SEM_SYSV
    T_CHK_ERRNO(sysv_signal_sem(data->sem_id, 1)); // sem #1 = end
#endif
  }
}

int main(int argc, char** argv) {
  volatile char letters[26];
  for (int i = 0; i < 26; ++i)
    letters[i] = 'a' + i;

  pthread_t invcase_thrd, reverse_thrd;

  thread_data_t invcase_thrd_data = { .letters = letters };
  thread_data_t reverse_thrd_data = { .letters = letters };
#ifdef SEM_POSIX
  CHK_ERRNO(sem_init(&invcase_thrd_data.sem_begin, 0, 0));
  CHK_ERRNO(sem_init(&invcase_thrd_data.sem_end, 0, 0));
  CHK_ERRNO(sem_init(&reverse_thrd_data.sem_begin, 0, 0));
  CHK_ERRNO(sem_init(&reverse_thrd_data.sem_end, 0, 0));
#endif
#ifdef SEM_SYSV
  short init_vals[2] = { 1, 1 };
  CHK_ERRNO(invcase_thrd_data.sem_id = semget(IPC_PRIVATE, 2, 0600 | IPC_CREAT));
  CHK_ERRNO(reverse_thrd_data.sem_id = semget(IPC_PRIVATE, 2, 0600 | IPC_CREAT));
  CHK_ERRNO(semctl(invcase_thrd_data.sem_id, 0, SETALL, init_vals));
  CHK_ERRNO(semctl(reverse_thrd_data.sem_id, 0, SETALL, init_vals));
#endif

  if (pthread_create(&invcase_thrd, NULL, invert_case_posix_sem_thread, &invcase_thrd_data) != 0 ||
      pthread_create(&reverse_thrd, NULL, reverse_posix_sem_thread, &reverse_thrd_data) != 0) {
    fprintf(stderr, "Unable to create a thread\n");
    return 1;
  }

  int thread = 0;

  while (1) {
    thread_data_t* tdata = thread == 0 ? &invcase_thrd_data : &reverse_thrd_data;
    thread = !thread;

#ifdef SEM_POSIX
    CHK_ERRNO(sem_post(&tdata->sem_begin));
    CHK_ERRNO(sem_wait(&tdata->sem_end));
#endif
#ifdef SEM_SYSV
    CHK_ERRNO(sysv_signal_sem(tdata->sem_id, 0)); // sem #0 = begin
    CHK_ERRNO(sysv_wait_sem(tdata->sem_id, 1)); // sem #1 = end
#endif

    for (int i = 0; i < 26; ++i)
      printf("%c", letters[i]);
    printf("\n");

    sleep(1);
  }

  return 0;
}
