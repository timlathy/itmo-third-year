#define _DEFAULT_SOURCE // getloadavg
#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>
#include <signal.h>

#include <sys/un.h>
#include <sys/types.h>
#include <sys/socket.h>

#include "error.h"
#include "sysloadsock.h"

volatile sig_atomic_t last_sig = 0;

void handle_signal(int sig) {
  last_sig = sig;
}

void check_signals(server_state_t* state) {
  if (last_sig == 0) return;
  psignal(last_sig, "The server is shutting down");
  printf("State snapshot:\nLoad average:\n"
         "  1 minute: %.2lf\n  5 minutes: %.2lf\n  15 minutes: %.2lf\n",
         state->loadavg[0], state->loadavg[1], state->loadavg[2]);
  exit(0);
}

int setup_signal_handlers() {
  struct sigaction action = { .sa_handler = handle_signal, .sa_flags = 0 };
  sigemptyset(&action.sa_mask);
  CHK_ERRNO(sigaction(SIGHUP, &action, NULL));
  CHK_ERRNO(sigaction(SIGINT, &action, NULL));
  CHK_ERRNO(sigaction(SIGTERM, &action, NULL));
  CHK_ERRNO(sigaction(SIGUSR1, &action, NULL));
  CHK_ERRNO(sigaction(SIGUSR2, &action, NULL));
  return 0;
}

int main(unused(int argc), unused(char** argv)) {
  server_state_t state = { .pid = getpid(), .uid = getuid(), .gid = getgid() };

  printf("Started a server with pid=%jd, uid=%jd, gid=%jd\n",
      (intmax_t) state.pid, (intmax_t) state.uid, (intmax_t) state.gid);

  if (setup_signal_handlers() != 0) return 1;

  int sockfd;
  CHK_ERRNO(sockfd = socket(AF_UNIX, SOCK_STREAM, 0));
  
  struct sockaddr_un sockaddr;
  sockaddr.sun_family = AF_UNIX;
  strncpy(sockaddr.sun_path, LAB_SOCK_PATH, sizeof(sockaddr.sun_path) - 1);
  unsigned int sockaddr_len = sizeof(struct sockaddr_un);

  unlink(LAB_SOCK_PATH);
  errno = 0;
  CHK_ERRNO(bind(sockfd, (const struct sockaddr *) &sockaddr, sockaddr_len));
  CHK_ERRNO(listen(sockfd, 0));

  puts("Listening on socket " LAB_SOCK_PATH);

  while (1) {
    int cltfd = accept(sockfd, (struct sockaddr*) &sockaddr, &sockaddr_len);
    if (errno == EINTR) {
      check_signals(&state);
      errno = 0;
      continue;
    }
    CHK_ERRNO();

    getloadavg(state.loadavg, 3);

    write(cltfd, (const void*) &state, sizeof(server_state_t));
    if (errno != 0)
      fprintf(stderr, "Failed to send data to a client: %s\n", strerror(errno));

    close(cltfd);
    errno = 0;
  }

  return 0;
}
