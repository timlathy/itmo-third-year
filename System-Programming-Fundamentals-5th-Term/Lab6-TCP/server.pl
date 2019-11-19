#!/usr/bin/perl

use strict;
use warnings qw(FATAL all);
use threads;
use IO::Socket::INET;

use constant USAGE => "Usage $0 port\n";
my ($port) = shift =~ /(\d+)/ or die USAGE;

my $server = IO::Socket::INET->new(
  LocalPort => $port, Proto => 'tcp', Listen => SOMAXCONN
) or die "Failed to start the server: $!\n";

print "Listening on $port\n";

while (my $clt = $server->accept()) {
  threads->create(\&process_request, $clt)->detach();
}

sub process_request {
  my $clt = shift;

  my $cltaddr = $clt->peerhost;
  my $cltport = $clt->peerport;
  print "Client connected: $cltaddr:$cltport\n";

  my $request = "";
  while (<$clt>) {
    $request .= $_;
    last if $request =~ /\r\n\r\n$/;
  }

  my @dirs = split /\r\n/, $request;

  for my $dir (@dirs) {
    if (opendir my $dirent, $dir) {
      my @files = readdir $dirent;
      closedir $dirent;

      print $clt "Contents of $dir:\r\n" . join("\r\n", @files) . "\r\n\r\n";
    }
    else {
      print $clt "Failed to open $dir: $!\r\n\r\n";
    }
  }

  close $clt;
}
