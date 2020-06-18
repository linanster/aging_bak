#!/usr/bin/env bash
#
# set -o errexit


usage=$"
Usage: $0 [starttest] [allkickout]
"

workdir=$(cd "$(dirname $0)" && pwd)
topdir=$(cd "$(dirname $0)" && cd ..  && pwd)

cd "$workdir"

function activate_venv() {
  cd "$topdir"
  if [ -d venv ]; then
    source ./venv/bin/activate || source ./venv/Script/activate
  else
    echo "==venv error=="
    exit 1
  fi
}


function run_starttest() {
    cd "$topdir"
    activate_venv
    cd "$workdir"
    python3 rasp_api_caller.py starttest
    exit "$?"
}

function run_allkickout() {
    cd "$topdir"
    activate_venv
    cd "$workdir"
    python3 rasp_api_caller.py allkickout
    exit "$?"
}


# if [ $# -eq 0 ]; then
#     echo "${usage}"
#     exit 1
# fi

if [ $# -eq 1 ]; then
  case $1 in
    --help|-h)
        echo "$usage"
        exit 0
        ;;
    starttest)
        run_starttest
        ;;
    allkickout)
        run_allkickout
        ;;
    *)
        echo "$usage"
        exit 1
        ;;
  esac
else
  echo "$usage"
  exit 1
fi

