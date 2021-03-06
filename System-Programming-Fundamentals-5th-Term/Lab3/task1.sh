#!/bin/bash

if [ $# -ne 1 ]; then
  echo Usage: $(basename "$0") dir_path
  exit
fi

# Sample stat output: drwxrwxrwx 1000 1000
dir_info=$(stat -c '%A %u %g' "$1" 2>/dev/null)
if [ $? -ne 0 ]; then
  >&2 echo Unable to open $1
  >&2 echo Please ensure the directory exists and you have sufficient permissions
  exit 1
fi

read -r perms owner_uid owner_gid <<< "$dir_info"

if [ ${perms:0:1} != 'd' ]; then
  >&2 echo "$1 is not a directory"
  exit 1
fi

owner_name=$(getent passwd $owner_uid | cut -d: -f1)
owner_group_members=$(getent group $owner_gid | cut -d: -f4 | tr , '\n')

if [ ${perms:1:1} == 'r' ]; then
  echo $owner_name
fi

if [ ${perms:4:1} == 'r' ]; then
  for user in $owner_group_members; do
    if [ "$user" != "$owner_name" ]; then
      echo $user
    fi
  done
fi

if [ ${perms:7:1} == 'r' ]; then
  newline=$'\n'
  owner_and_owner_group_members="${owner_group_members}${newline}${owner_name}"
  for user in $(getent passwd | cut -d: -f1); do
    if ! grep -q "^${user}$" <<< "$owner_and_owner_group_members"; then
      echo $user
    fi
  done
fi
