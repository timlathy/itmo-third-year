#!/usr/bin/env sh
if [ $# -ge 1 ]; then
  dir="$1"
else
  dir=.
fi

ls -lq "$dir" \
  | tail -n+2 \
  | sort -nk 5 \
  | sed -E 's/([^ ]+\s+){7}[^ ]+\s//' \
  | awk '{if (/[^A-Za-z.]/) print}'
