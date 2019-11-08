#!/usr/bin/perl -T

use strict;
use warnings qw(FATAL all);
use IO::Socket::UNIX;

use constant STATE_FMT => 'i<i<i<d<d<d<d<';
use constant STATE_SIZE => length pack(STATE_FMT, 0, 0, 0, 0, 0, 0);
use constant LAB_SOCK_PATH => '/tmp/spf-lab5-sysload-sock';

my $client = IO::Socket::UNIX->new(Type => SOCK_STREAM(), Peer => LAB_SOCK_PATH)
  or die "Failed to connect to a socket: $!\n";

my $state_buf = "";
read $client, $state_buf, STATE_SIZE;
my ($spid, $suid, $sgid, $rt, $sl1, $sl5, $sl15) = unpack STATE_FMT, $state_buf;

print "Connected to server with pid=$spid, uid=$suid, gid=$sgid, runtime=${rt}s\n";
print "Load average:\n  1 minute: $sl1\n  5 minutes: $sl5\n  15 minutes: $sl15\n";
