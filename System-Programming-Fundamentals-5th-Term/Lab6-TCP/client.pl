#!/usr/bin/perl -T

use strict;
use warnings qw(FATAL all);
use IO::Socket::INET;

use constant USAGE => "Usage $0 host port [files...]\n";

my ($host) = shift =~ /([A-Za-z0-9.]+)/ or die USAGE;
my ($port) = shift =~ /(\d+)/ or die USAGE;

scalar @ARGV or die USAGE;
my $request = join("\r\n", @ARGV) . "\r\n\r\n";

my $clt = new IO::Socket::INET(
  PeerHost => $host, PeerPort => $port, Proto => 'tcp'
) or die "Failed to connect to $host:$port: $!\n";

$clt->send($request);

while (<$clt>) {
  print;
}
