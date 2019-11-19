#!/usr/bin/perl

use strict;
use warnings qw(FATAL all);
use IO::Socket::INET;

use constant USAGE => "Usage $0 host port [files...]\n";

my $host = shift or die USAGE;
my $port = shift or die USAGE;

scalar @ARGV or die USAGE;
my $request = join("\r\n", @ARGV) . "\r\n\r\n";

my $clt = new IO::Socket::INET(
  PeerHost => $host, PeerPort => $port, Proto => 'tcp'
) or die "Failed to connect to $host:$port: $!\n";

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

print $response;
