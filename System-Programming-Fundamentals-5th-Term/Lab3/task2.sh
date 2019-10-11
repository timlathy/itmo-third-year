#!/bin/bash

if [ $# -ne 1 ]; then
  echo Usage: $(basename "$0") username
  exit
fi

user_uid=$(getent passwd "$1" | cut -d: -f3)
if [ -z "$user_uid" ]; then
  >&2 echo "Unable to find user $1"
  exit 1
fi
user_gids=$(groups "$1" | cut -d: -f2- | xargs getent group | cut -d: -f3)

for file in *; do
  read -r perms owner_uid owner_gid <<< $(stat -c '%A %u %g' "$file")

  if [ ${perms:0:1} == 'd' ]; then
    continue # exclude subdirectories
  fi

  if [ $user_uid == $owner_uid ]; then
    if [ ${perms:3:1} == 'x' ]; then
      echo $file
    fi
    continue
  fi

  if grep -q "^${owner_gid}$" <<< "$user_gids"; then
    if [ ${perms:6:1} == 'x' ]; then
      echo $file
    fi
    continue
  fi

  if [ ${perms:9:1} == 'x' ]; then
    echo $file
  fi
done
