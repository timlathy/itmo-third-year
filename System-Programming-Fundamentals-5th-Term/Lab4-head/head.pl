#!/usr/bin/perl -T

# Run
# cpan Getopt::Long
# to fetch script dependencies

use strict;
use warnings qw(FATAL all);
use Getopt::Long;

use constant USAGE => "Usage: $0 [-n num-lines] [-c num-bytes] [file...]\n";

my $num_lines;
my $num_chars;

GetOptions("n=i" => \$num_lines, "c=i" => \$num_chars) or die(USAGE);
die("$0: invalid number of lines: '$num_lines'\n") if ($num_lines and $num_lines < 0);
die("$0: invalid number of characters: '$num_chars'\n") if ($num_chars and $num_chars < 0);
exit if $num_lines and $num_lines == 0 or $num_chars and $num_chars == 0;
$num_lines = 10 if not $num_lines and not $num_chars;

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

  if ($num_lines and $printed++ < $num_lines) {
    eval {
      my $line = <>;
      print $line;
    }
    or do {
      print $@; # error
      $printed = 0;
    }
  }
  elsif ($num_chars and $printed < $num_chars) {
    eval {
      my $line = <>;
      my $remaining_chars = $num_chars - $printed;
      my $should_print = $remaining_chars < length $line ? $remaining_chars : length $line;
      print substr $line, 0, $should_print;
      $printed += $should_print;
    }
    or do {
      print $@; # error
      $printed = 0;
    }
  }

  if ($num_lines and $printed == $num_lines or $num_chars and $printed == $num_chars or eof) {
    $printed = 0;
    close ARGV;
  }
}
