#!/usr/bin/env perl

use strict;
use Test2::V0;
use IO::Socket::INET;

my $port = shift or die "Usage $0 port\n";

`rm -rf test; mkdir -p test/abc; touch test/h; touch test/abc/h; mkdir test/forbidden; chmod u-r test/forbidden`;

my $resp = send_request("test/forbidden\r\n./test\r\n\r\n");
is $resp, "Failed to open test/forbidden: Permission denied\r\n" .
  "\r\n" .
  "Contents of ./test:\r\n" .
  "forbidden\r\n" .
  ".\r\n" .
  "h\r\n" .
  "..\r\n" .
  "abc\r\n" .
  "\r\n" .
  "\r\n";

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
