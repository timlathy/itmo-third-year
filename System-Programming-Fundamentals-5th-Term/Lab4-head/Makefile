CC=gcc
CFLAGS=-std=c11 -g -Wall -Wextra -pedantic -Werror

all: head xargs

head: head.c
	$(CC) $(CFLAGS) -o head head.c

xargs: xargs.c
	$(CC) $(CFLAGS) -o xargs xargs.c

clean:
	@rm head xargs
