#!/usr/bin/env perl

use strict;
use Test2::V0;
use IO::Socket::INET;

my $port = shift or die "Usage $0 port\n";

my $clt = new IO::Socket::INET(PeerHost => 'localhost', PeerPort => $port, Proto => 'tcp')
  or die "Failed to connect to the server: $!\n";

$clt->send("/home/dir1\r\n/home/dir1/nested\r\n\r\n");

my $response = "";
while (1) {
  $clt->recv(my $chunk, 1024);
  if (scalar $chunk) {
    $response .= $chunk;
  }
  else {
    last
  }
}

is $response, "Directory: [/home/dir1]\r\nDirectory: [/home/dir1/nested]\r\n\r\n";

done_testing();
