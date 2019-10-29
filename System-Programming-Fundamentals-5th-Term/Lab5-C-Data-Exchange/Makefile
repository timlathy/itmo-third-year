CC=gcc
CFLAGS=-std=c11 -g -Wall -Wextra -pedantic

all: sysloadsrv sysloadclt

sysloadsrv: sysloadsrv.c
	$(CC) $(CFLAGS) -o sysloadsrv sysloadsrv.c

sysloadclt: sysloadclt.c
	$(CC) $(CFLAGS) -o sysloadclt sysloadclt.c

clean:
	@rm sysloadsrv sysloadclt
