#!/usr/bin/env bash

function print_cwd {
  echo $PWD
}

function list_cwd {
  echo $(ls)
}

function make_dir {
  echo Enter the path to the new directory (TAB to autocomplete):
  read -e path
  mkdir -p "$path"
}

function run {
  echo; $1; echo
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
    6) break;;
    *) echo Unknown action [$action];;
    esac
  else
    break # handle EOF
  fi
done
