#!/usr/bin/perl -T

use strict;
use warnings qw(FATAL all);
use IO::Socket::UNIX;
use English;

use constant STATE_FMT => 'i<i<i<d<d<d<';
use constant LAB_SOCK_PATH => '/tmp/spf-lab5-sysload-sock';

unlink(LAB_SOCK_PATH);

my $server = IO::Socket::UNIX->new(
  Type => SOCK_STREAM(), Local => LAB_SOCK_PATH, Listen => 1
) or die("Failed to create a socket: $!\n");

my $realgid = (split ' ', $GID)[0];
print "Started a server with pid=$PID, uid=$UID, gids=$realgid\n";

while (my $clt = $server->accept()) {
  my ($l1, $l5, $l15) = getloadavg();
  my $state = pack(STATE_FMT, $PID, $UID, $realgid, $l1, $l5, $l15);

  $clt->print($state);
  $clt->close();
}

sub getloadavg {
  $ENV{'PATH'} = '/usr/bin';
  my $uptime = `uptime`;
  $uptime =~ s/,/./g;
  $uptime =~ /load average: (\d+\.\d+)\. (\d+\.\d+)\. (\d+\.\d+)/;
  return ($1, $2, $3);
}
