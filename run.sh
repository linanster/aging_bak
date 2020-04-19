#!/usr/bin/env bash
#
# set -o errexit


# lib: color print
bold=$(tput bold)
green=$(tput setf 2)
red=$(tput setf 4)
reset=$(tput sgr0)

function green() {
          printf "${bold}${green}%s${reset}\n" "$@";
  }
function red() {
          printf "${bold}${red}%s${reset}\n" "$@";
  }


usage=$"
Usage: run.sh [--start] [--stop] [--status] [--init] [--upload] [--purge]
"

if [ $# -eq 0 ]; then
    red "${usage}"
    exit 1
fi
if [ "$1" != "--start" -a "$1" != "--stop" -a "$1" != "--status" -a "$1" != "--init" -a "$1" != "--upload" -a "$1" != "--purge" ]; then
    red "${usage}"
    exit 1
fi

workdir=$(cd "$(dirname $0)" && pwd)
cd "$workdir"

if [ "$1" == "--init" ]; then
    pip3 install virtualenv
    virtualenv venv
    source ./venv/bin/activate
    pip3 install -r requirements.txt
    if [ $? -eq 0 ]; then
        green "==init config complete=="
        exit 0
    else
        red "==init config fail=="
        exit 1
    fi
fi

if [ -d venv ]; then
    source ./venv/bin/activate
else
    red "==venv error=="
    exit 1
fi

# cd "$workdir/app"

if [ "$1" == '--start' ]; then
    green "gunicorn --workers 1 --bind 0.0.0.0:5000 --timeout 300 --worker-class eventlet wsgi:application_ge_aging"
    # todo --daemon
    # todo --user user1 --group user1
    if [ "$2" == '--nodaemon' ]; then
        gunicorn --workers 1 --bind 0.0.0.0:5000 --timeout 300 --worker-class eventlet wsgi:application_ge_aging
    else
        gunicorn --daemon --workers 1 --bind 0.0.0.0:5000 --timeout 300 --worker-class eventlet wsgi:application_ge_aging
    fi
    ps -ef | fgrep "gunicorn" | grep "application_ge_aging" | awk '{if($3==1) print $2}'
    exit 0
fi

if [ "$1" == "--stop" ]; then
    pid=$(ps -ef | fgrep "gunicorn" | grep "application_ge_aging" | awk '{if($3==1) print $2}')
    if [ "$pid" == "" ]; then
        red "not running" 
    else
        green "kill $pid"
        kill "$pid"
    fi
    exit 0
fi

if [ "$1" == "--status" ]; then
    pid=$(ps -ef | fgrep "gunicorn" | grep "application_ge_aging" | awk '{if($3==1) print $2}')
    if [ "$pid" == "" ]; then
        red "stopped" 
    else
        green "$pid"
        green "started"
    fi
    exit 0
fi

if [ "$1" == "--upload" ]; then
    python3 manage.py upload
    green "$?" 
fi

if [ "$1" == "--purge" ]; then
    python3 manage.py purge
    green "$?" 
fi
