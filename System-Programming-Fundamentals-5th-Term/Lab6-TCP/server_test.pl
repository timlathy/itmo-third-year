#!/usr/bin/env perl

use strict;
use Test2::V0;
use IO::Socket::INET;

my $port = shift or die "Usage $0 port\n";

my $resp = send_request("/home/dir1\r\n/home/dir1/nested\r\n\r\n");
is $resp, "Directory: [/home/dir1]\r\nDirectory: [/home/dir1/nested]\r\n\r\n";

$resp = send_request("\r\n");
is $resp, "Malformed request: make sure you're sending at least one path, " .
  "each path on a separate line, each line terminated by CRLF, " .
  "and the request terminated by an empty line.\r\n";

done_testing();

sub send_request {
  my $request = shift;

  my $clt = new IO::Socket::INET(
    PeerHost => 'localhost',
    PeerPort => $port,
    Proto => 'tcp'
  ) or die "Failed to connect to the server: $!\n";

  $clt->send($request);

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
  $response
}
