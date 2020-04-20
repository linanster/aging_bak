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
Usage: run.sh [--start] [--stop] [--status] [--init] [--upload] [--purge] [--upgrade]
"

workdir=$(cd "$(dirname $0)" && pwd)
cd "$workdir"


function activate_venv() {
  if [ -d venv ]; then
    source ./venv/bin/activate
  else
    red "==venv error=="
    exit 1
  fi
}


function run_init(){
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
}

function run_start() {
    activate_venv
    green "gunicorn --workers 1 --bind 0.0.0.0:5000 --timeout 300 --worker-class eventlet wsgi:application_ge_aging"
    # todo --daemon
    # todo --user user1 --group user1
    if [ "$1" == '--nodaemon' ]; then
        gunicorn --workers 1 --bind 0.0.0.0:5000 --timeout 300 --worker-class eventlet wsgi:application_ge_aging
    else
        gunicorn --daemon --workers 1 --bind 0.0.0.0:5000 --timeout 300 --worker-class eventlet wsgi:application_ge_aging
    fi
    ps -ef | fgrep "gunicorn" | grep "application_ge_aging" | awk '{if($3==1) print $2}'
    exit 0
}

function run_stop() {
    activate_venv
    pid=$(ps -ef | fgrep "gunicorn" | grep "application_ge_aging" | awk '{if($3==1) print $2}')
    if [ "$pid" == "" ]; then
        red "not running" 
        exit 1
    else
        green "kill $pid"
        kill "$pid"
        exit 0
    fi
}

function run_status(){
    activate_venv
    pid=$(ps -ef | fgrep "gunicorn" | grep "application_ge_aging" | awk '{if($3==1) print $2}')
    if [ "$pid" == "" ]; then
        red "stopped" 
    else
        green "$pid"
        green "started"
    fi
    exit 0
}

function run_upload(){
    activate_venv
    python3 manage.py upload
    errno="$?"
    green "$errno" 
    exit "$errno"
}

function run_purge(){
    activate_venv
    python3 manage.py purge
    errno="$?"
    green "$errno" 
    exit "$errno"
}

function run_upgrade(){
    activate_venv
    cd "$workdir"
    git checkout master
    systemctl stop aging.service
    sleep 1
    git pull origin upgrade:master
    sleep 1
    systemctl start aging.service
    sleep 1
    systemctl status aging.service && exit 0 || exit 1
}

if [ $# -eq 0 ]; then
    red "${usage}"
    exit 1
fi

if [ $# -ge 1 ]; then
  case $1 in
    --help|-h)
        green "$usage"
        exit 0
        ;;
    --init)
        run_init
        ;;
    --status)
        run_status
        ;;
    --start)
        run_start $2
        ;;
    --stop)
        run_stop
        ;;
    --upload)
        run_upload
        ;;
    --purge)
        run_purge
        ;;
    --upgrade)
        run_upgrade
        ;;
    *)
        red "$usage"
        exit 1
        ;;
  esac
fi
            
