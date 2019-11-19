CC=gcc
CFLAGS=-std=c11 -g -Wall -Wextra -pedantic

all: server client

server: server.c dir.h
	$(CC) $(CFLAGS) -pthread -o server server.c

client: client.c
	$(CC) $(CFLAGS) -o client client.c

clean:
	@rm server client
