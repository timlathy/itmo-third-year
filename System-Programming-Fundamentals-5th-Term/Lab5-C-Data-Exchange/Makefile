CC=gcc
CFLAGS=-std=c11 -g -Wall -Wextra -pedantic

all: sysloadsrv

sysloadsrv: sysloadsrv.c
	$(CC) $(CFLAGS) -o sysloadsrv sysloadsrv.c

clean:
	@rm sysloadsrv
