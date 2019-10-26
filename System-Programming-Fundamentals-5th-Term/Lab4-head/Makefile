CC=gcc
CFLAGS=-std=c11 -g -Wall -Werror -march=native

all: head xargs

head: head.c
	$(CC) $(CFLAGS) -o head head.c

xargs: xargs.c
	$(CC) $(CFLAGS) -o xargs xargs.c

clean:
	@rm head xargs
