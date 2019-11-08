CC=gcc
CFLAGS=-std=c11 -g -Wall -Wextra -pedantic

all: sysloadsrv sysloadclt semarray pthreadarray

sysloadsrv: sysloadsrv.c
	$(CC) $(CFLAGS) -o sysloadsrv sysloadsrv.c

sysloadclt: sysloadclt.c
	$(CC) $(CFLAGS) -o sysloadclt sysloadclt.c

semarray: semarray.c
	$(CC) $(CFLAGS) -pthread -o semarray_posix -DSEM_POSIX semarray.c
	$(CC) $(CFLAGS) -pthread -o semarray_sysv -DSEM_SYSV semarray.c

pthreadarray: pthreadarray.c
	$(CC) $(CFLAGS) -pthread -o pthread_mutex -DMUTEX pthreadarray.c
	$(CC) $(CFLAGS) -pthread -o pthread_rwlock -DRWLOCK pthreadarray.c

sysloadsocksrv: sysloadsocksrv.c
	$(CC) $(CFLAGS) -o sysloadsocksrv sysloadsocksrv.c

sysloadsockclt: sysloadsockclt.c
	$(CC) $(CFLAGS) -o sysloadsockclt sysloadsockclt.c

unnamedpipe: unnamedpipe.c
	$(CC) $(CFLAGS) -o unnamedpipe unnamedpipe.c

clean:
	@rm sysloadsrv sysloadclt \
		semarray_posix semarray_sysv \
		pthread_mutex pthread_rwlock \
		sysloadsocksrv sysloadsockclt \
		unnamedpipe
