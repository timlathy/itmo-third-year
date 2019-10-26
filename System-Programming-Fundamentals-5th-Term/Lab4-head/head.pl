#!/usr/bin/perl -T

# Run
# cpan Getopt::Long
# to fetch script dependencies

use strict;
use warnings qw(FATAL all);
use Getopt::Long;

my $num_lines = 10;

GetOptions("n=i" => \$num_lines) or die("Usage: $0 [-n num-lines] [file...]\n");
$num_lines >= 0 or die("$0: invalid number of lines: '$num_lines'\n");
if ($num_lines == 0) {
  exit;
}

my $printed = 0;
my $first_file = 1;

while (@ARGV or $first_file or $printed > 0) {
  if ($printed == 0) {
    if (@ARGV) {
      my $leading_newline = $first_file ? "" : "\n";
      my $filename = $ARGV[0] eq "-" ? "standard input" : $ARGV[0];
      print "$leading_newline==> $filename <==\n";
      undef $first_file;
    }
    else {
      # No arguments = don't print the header, read from stdin
      undef $first_file;
    }
  }
  if ($printed++ < $num_lines) {
    eval {
      my $line = <>;
      print $line;
    }
    or do {
      print $@; # error
      $printed = 0;
    }
  }
  if ($printed == $num_lines or eof) {
    $printed = 0;
    close ARGV;
  }
}
