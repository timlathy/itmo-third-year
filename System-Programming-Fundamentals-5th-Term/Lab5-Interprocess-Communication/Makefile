CC=gcc
CFLAGS=-std=c11 -g -Wall -Wextra -pedantic

all: sysloadsrv sysloadclt semarray

sysloadsrv: sysloadsrv.c
	$(CC) $(CFLAGS) -o sysloadsrv sysloadsrv.c

sysloadclt: sysloadclt.c
	$(CC) $(CFLAGS) -o sysloadclt sysloadclt.c

semarray: semarray.c
	$(CC) $(CFLAGS) -pthread -o semarray_posix -DSEM_POSIX semarray.c
	#$(CC) $(CFLAGS) -pthread -o semarray_sysv -DSEM_SYSV semarray.c

clean:
	@rm sysloadsrv sysloadclt semarray_posix semarray_sysv
