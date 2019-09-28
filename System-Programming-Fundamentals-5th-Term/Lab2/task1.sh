#!/usr/bin/env sh
last | LC_TIME=C awk 'BEGIN{time=strftime("%a %b %e")}{if ($0 ~ time) print $1; else exit;}' | sort -u
