#!/usr/bin/perl -T

use strict;
use warnings qw(FATAL all);
use IO::Socket::UNIX;
use English;

use sigtrap 'handler' => \&handlesig, qw(HUP INT TERM USR1 USR2);

use constant STATE_FMT => 'i<i<i<d<d<d<d<';
use constant LAB_SOCK_PATH => '/tmp/spf-lab5-sysload-sock';

unlink LAB_SOCK_PATH;

my $server = IO::Socket::UNIX->new(
  Type => SOCK_STREAM(), Local => LAB_SOCK_PATH, Listen => 1
) or die "Failed to create a socket: $!\n";

my $realgid = (split ' ', $GID)[0];
print "Started a server with pid=$PID, uid=$UID, gids=$realgid\n";

my ($starttime, $runtime) = (time(), time());
my ($l1, $l5, $l15) = (0, 0, 0);

while (my $clt = $server->accept()) {
  $runtime = time() - $starttime;
  ($l1, $l5, $l15) = getloadavg();
  my $state = pack STATE_FMT, $PID, $UID, $realgid, $runtime, $l1, $l5, $l15;

  $clt->print($state);
  $clt->close();
}

sub getloadavg {
  $ENV{'PATH'} = '/usr/bin'; # explicitly setting PATH is required for -T mode
  my $uptime = `uptime`;
  $uptime =~ s/,/./g; # crude handling for comma as a decimal separator
  $uptime =~ /load average: (\d+\.\d+)\. (\d+\.\d+)\. (\d+\.\d+)/;
  return ($1, $2, $3);
}

sub handlesig {
  $runtime = time() - $starttime;
  print "The server is shutting down: $_[0]\n";
  print "State snapshot:\nRuntime: ${runtime}s\nLoad average:\n" .
         "  1 minute: $l1\n  5 minutes: $l5\n  15 minutes: $l15\n";
}
