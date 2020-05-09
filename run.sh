#!/usr/bin/env bash
#
# set -o errexit


usage=$"
Usage: run.sh [--start] [--stop] [--status] [--init] [--upload] [--purge] [--upgrade]
"

workdir=$(cd "$(dirname $0)" && pwd)
cd "$workdir"


function activate_venv() {
  if [ -d venv ]; then
    source ./venv/bin/activate
  else
    echo "==venv error=="
    exit 1
  fi
}


function run_init(){
    pip3 install virtualenv
    virtualenv venv
    source ./venv/bin/activate
    pip3 install -r requirements.txt
    # pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
    if [ $? -eq 0 ]; then
        echo "==init config complete=="
        exit 0
    else
        echo "==init config fail=="
        exit 1
    fi
}

function run_start() {
    activate_venv
    echo "gunicorn --workers 1 --bind 0.0.0.0:5000 --timeout 300 --worker-class eventlet wsgi:application_ge_aging"
    # echo "gunicorn --workers 1 --bind 0.0.0.0:5000 --timeout 300 --worker-class gevent wsgi:application_ge_aging"
    # todo --user user1 --group user1
    if [ "$1" == '--nodaemon' ]; then
        gunicorn --workers 1 --bind 0.0.0.0:5000 --timeout 300 --worker-class eventlet wsgi:application_ge_aging
        # gunicorn --workers 1 --bind 0.0.0.0:5000 --timeout 300 --worker-class gevent wsgi:application_ge_aging
    else
        gunicorn --daemon --workers 1 --bind 0.0.0.0:5000 --timeout 300 --worker-class eventlet wsgi:application_ge_aging
        # gunicorn --daemon --workers 1 --bind 0.0.0.0:5000 --timeout 300 --worker-class gevent wsgi:application_ge_aging
    fi
    ps -ef | fgrep "gunicorn" | grep "application_ge_aging" | awk '{if($3==1) print $2}'
    exit 0
}

function run_stop() {
    activate_venv
    pid=$(ps -ef | fgrep "gunicorn" | grep "application_ge_aging" | awk '{if($3==1) print $2}')
    if [ "$pid" == "" ]; then
        echo "not running" 
        exit 1
    else
        echo "kill $pid"
        kill "$pid"
        exit 0
    fi
}

function run_status(){
    activate_venv
    pid=$(ps -ef | fgrep "gunicorn" | grep "application_ge_aging" | awk '{if($3==1) print $2}')
    if [ "$pid" == "" ]; then
        echo "stopped" 
    else
        echo "$pid"
        echo "started"
    fi
    exit 0
}

function run_upload(){
    activate_venv
    python3 manage.py upload
    errno="$?"
    echo "$errno" 
    exit "$errno"
}

function run_purge(){
    activate_venv
    python3 manage.py purge
    errno="$?"
    echo "$errno" 
    exit "$errno"
}

function run_upgrade(){
    cd "$workdir"
    activate_venv
    if [ "$1" == "--checkout" ]; then
        git checkout origin/upgrade upgrade/pin.txt && { echo "checkout auth code success"; exit 0; } || { echo "checkout auth code error,exit"; exit 11; }
    fi
    sleep 1
    git pull --quiet origin upgrade>/dev/null && { echo "1. pull upgrade success"; } ||  { echo "1. pull upgrade error, exit"; exit 1; }
    sleep 1
    systemctl restart --quiet aging.service>/dev/null && { echo "2. restart service success"; } ||  { echo "2. restart service error, exit"; exit 2; }
    sleep 1
    systemctl status --quiet aging.service>/dev/null && { echo "3. check service success"; exit 0; } ||  { echo "3. check service error, exit"; exit 3; }
}

if [ $# -eq 0 ]; then
    echo "${usage}"
    exit 1
fi

if [ $# -ge 1 ]; then
  case $1 in
    --help|-h)
        echo "$usage"
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
        run_upgrade $2
        ;;
    *)
        echo "$usage"
        exit 1
        ;;
  esac
fi
            
