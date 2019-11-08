#!/usr/bin/perl -T

use strict;
use warnings qw(FATAL all);

my $filename = shift @ARGV;
die "Usage: $0 file\n" if !$filename;

open my $fd, '<', $filename or die "Can't open $filename: $!\n";
pipe my $pipefd_rd, my $pipefd_wr or die "Can't create a pipe: $!\n";

my $pid = fork();
if (!$pid) {
  # Child process
  close $pipefd_wr or die "Can't close parent's end of the pipe: $!\n";
  open STDIN, '<&', $pipefd_rd or die "Can't replace STDIN with the pipe: $!\n"; 

  $ENV{'PATH'} = '/usr/bin';
  exec "wc -c" or die "Can't exec wc: $!\n";
}
else {
  # Parent process
  close $pipefd_rd or die "Can't close child's end of the pipe: $!\n";

  my $buf = "";
  while (read $fd, $buf, 2) {
    print $pipefd_wr substr($buf, 1, 1);
  }
}

