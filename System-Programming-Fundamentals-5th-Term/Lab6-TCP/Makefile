CC=gcc
CFLAGS=-std=c11 -g -Wall -Wextra -pedantic

all: server

server: server.c dir.h
	$(CC) $(CFLAGS) -pthread -o server server.c

clean:
	@rm server
