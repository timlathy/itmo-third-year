CC=gcc
CFLAGS=-std=c11 -g -Wall -Wextra -pedantic

all: sysloadsrv sysloadclt pthreadarray

sysloadsrv: sysloadsrv.c
	$(CC) $(CFLAGS) -o sysloadsrv sysloadsrv.c

sysloadclt: sysloadclt.c
	$(CC) $(CFLAGS) -o sysloadclt sysloadclt.c

pthreadarray: pthreadarray.c
	$(CC) $(CFLAGS) -pthread -o pthreadarray pthreadarray.c

clean:
	@rm sysloadsrv sysloadclt pthreadarray
