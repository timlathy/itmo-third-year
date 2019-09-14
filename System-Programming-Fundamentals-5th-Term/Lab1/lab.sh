#!/usr/bin/env bash

# == Setup

if [ -z "$LOG" ]; then
  LOG="$HOME/lab1_err"
fi

if [ "$INRAW" = "1" ]; then
  echo Raw input on.
else
  echo Raw input off. TAB may be used for autocompletion. Set \$INRAW to 1 to override this behavior.
fi

function ensure_log_writable {
  if [ ! -w $LOG ]; then
    touch $LOG 2>/dev/null
    if [ $? -ne 0 ]; then
      echo_stderr Log file "$LOG" is not writable. \
        Please restore write access or specify a different log path with \$LOG.
      exit 1
    fi
  fi
}

function read_path {
  if [ "$INRAW" = "1" ]; then
    IFS= read path
  else
    IFS= read -e path
  fi
  echo "$path"
}

function run {
  echo; $1; echo
}

function echo_stderr {
  echo "$@" 1>&2
}

# === Commands

function print_cwd {
  echo $PWD
}

function list_cwd {
  echo $(ls)
}

function make_dir {
  echo Enter the path to the new directory:
  local path=$(read_path)
  echo Creating "$path"
  mkdir "$path" 2>>$LOG \
    || echo_stderr Unable to create the specified directory -- \
        are you sure you have sufficient permissions \
        and all parent directories exist while the directory itself does not?
}

function make_world_writable {
  echo Enter the path to the directory you wish to make world-writable:
  local path=$(read_path)
  echo Altering permissions for "$path"

  local current_perm=$(stat --dereference --format="%a" "$path" 2>>$LOG)
  if [ -z "$current_perm" ]; then
    echo_stderr The specified directory does not exist.
  elif ((($current_perm & 222) == 8)); then
    echo_stderr chmod: directory \'"$path"\' is already world-writable 2>>$LOG
    echo_stderr The specified directory is already world-writable. Nothing is done.
  else
    chmod ugo+w $path 2>>$LOG \
      || echo_stderr Unable to alter permissions for the specified directory -- \
          are you sure the directory exists and you have sufficient permissions?
  fi
}

function make_read_only {
  echo Enter the path to the directory you wish to make read only:
  local path=$(read_path)
  echo Altering permissions for "$path"
  chmod ugo-w $path 2>>$LOG \
    || echo_stderr Unable to alter permissions for the specified directory -- \
        are you sure the directory exists and you have sufficient permissions?
}

while true; do
  ensure_log_writable
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
    4) run make_world_writable;;
    5) run make_read_only;;
    6) break;;
    *) echo_stderr Unknown action [$action];;
    esac
  else
    break # handle EOF
  fi
done
