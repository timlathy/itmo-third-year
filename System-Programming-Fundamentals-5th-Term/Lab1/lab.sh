#!/usr/bin/env bash

log_file="$HOME/lab1_err"

function print_cwd {
  echo $PWD
}

function list_cwd {
  echo $(ls)
}

function make_dir {
  echo Enter the path to the new directory \(TAB to autocomplete\):
  read -e path
  echo Creating $path
  mkdir -p "$path" 2>>$log_file \
    || echo_stderr Unable to create the specified directory \
        -- are you sure you have sufficient permissions?
}

function make_world_writeable {
  echo Enter the path to the directory you wish to make world-writeable:
  read -e path
  echo Altering permissions for $path
  chmod +w $path 2>>$log_file \
    || echo_stderr Unable to alter permissions for the specified directory \
        -- are you sure the directory exists and you have sufficient permissions?
}

function make_read_only {
  echo Enter the path to the directory you wish to make read only:
  read -e path
  echo Altering permissions for $path
  chmod -w $path 2>>$log_file \
    || echo_stderr Unable to alter permissions for the specified directory \
        -- are you sure the directory exists and you have sufficient permissions?
}

function run {
  echo; $1; echo
}

function echo_stderr {
  echo "$@" 1>&2
}

while true; do
  echo [1] Print current working directory
  echo [2] List files in current working directory
  echo [3] Create a new directory
  echo [4] Grant every user write access to a directory
  echo [5] Revoke write access to a directory from all users
  echo [6] Quit
  if read -p "Choose the action to perform: " action; then
    case $action in
    1) run print_cwd;;
    2) run list_cwd;;
    3) run make_dir;;
    4) run make_world_writeable;;
    5) run make_read_only;;
    6) break;;
    *) echo_stderr Unknown action [$action];;
    esac
  else
    break # handle EOF
  fi
done
