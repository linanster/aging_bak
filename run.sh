#!/usr/bin/env bash
#
# set -o errexit


usage=$"
Usage: run.sh --start [--nodaemon]
              --stop
              --status
              --init
              --requirements
              --upload
              --purge
              --upgrade
              --logmonitor --start/--stop/--status
              --gotool --start/--stop/--status
              --resetdb
"

workdir=$(cd "$(dirname $0)" && pwd)
cd "$workdir"


function activate_venv() {
  if [ -d venv ]; then
    source ./venv/bin/activate || source ./venv/Script/activate
  else
    echo "==venv error=="
    exit 1
  fi
}

function get_pid_main(){
    pid=$(ps -ef | fgrep "gunicorn" | grep "application_ge_aging" | awk '{if($3==1) print $2}')
    echo "$pid"
}
function get_pid_logmonitor(){
    pid=$(ps -ef | fgrep "gunicorn" | grep "app_aging_logmonitor" | awk '{if($3==1) print $2}')
    echo "$pid"
}
function get_pid_gotool(){
    # pid=$(ps -ef | grep "/root/aging/go/gotool" | grep -v "grep" | awk '{if($3==1) print $2}')
    pid=$(ps -ef | grep "gotool" | grep -v "grep" | awk '{if($3==1) print $2}')
    echo "$pid"
}

function run_init(){
    pip3 install virtualenv
    virtualenv venv
    source ./venv/bin/activate
    # pip3 install -r requirements.txt
    pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
    if [ $? -eq 0 ]; then
        echo "==init config complete=="
        exit 0
    else
        echo "==init config fail=="
        exit 1
    fi
}

function run_requirements(){
    activate_venv
    # pip3 install -r requirements.txt
    pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
    if [ $? -eq 0 ]; then
        echo "==pip install requirements complete=="
        exit 0
    else
        echo "==pip install requirements fail=="
        exit 1
    fi
}


function run_start() {
    activate_venv
    # todo --user user1 --group user1
    case "$1" in
        "")
            cmd="gunicorn --daemon --workers 1 --bind 0.0.0.0:5000 --timeout 300 --worker-class eventlet wsgi:application_ge_aging"
            ;;
        "--nodaemon")
            cmd="gunicorn --workers 1 --bind 0.0.0.0:5000 --timeout 300 --worker-class eventlet wsgi:application_ge_aging"
            ;;
        *)
            echo "${usage}"
            exit 1
    esac
    echo "${cmd}"
    eval "${cmd}"
    pid=$(get_pid_main)
    echo "$pid"
    exit 0
}

function run_stop() {
    activate_venv
    pid=$(get_pid_main)
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
    pid=$(get_pid_main)
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

function run_upgrade_legacy(){
    activate_venv
    if [ "$1" == "--checkout" ]; then
        git checkout origin/upgrade upgrade/pin.txt && { echo "checkout auth code success"; exit 0; } || { echo "checkout auth code error,exit"; exit 11; }
    fi
    sleep 1
    git pull --quiet origin upgrade>/dev/null && { echo "1. pull upgrade success"; } ||  { echo "1. pull upgrade error, exit"; exit 1; }
    sleep 1
    systemctl restart --quiet aging-main.service>/dev/null && { echo "2. restart service success"; } ||  { echo "2. restart service error, exit"; exit 2; }
    sleep 1
    systemctl status --quiet aging-main.service>/dev/null && { echo "3. check service success"; exit 0; } ||  { echo "3. check service error, exit"; exit 3; }
}

function run_upgrade(){
    activate_venv
    sleep 1
    git pull --quiet origin master>/dev/null && { echo "pull master latest success"; exit 0; } ||  { echo "pull master latest error"; exit 1; }
}

function run_logmonitor() {
    activate_venv
    if [ "$1" == "--start" ]; then
        cd logmonitor
        if [ "$2" == '--nodaemon' ]; then
            cmd="gunicorn --workers 1 --bind 0.0.0.0:5001 --timeout 300 --worker-class eventlet app:app_aging_logmonitor"
        else
            cmd="gunicorn --daemon --workers 1 --bind 0.0.0.0:5001 --timeout 300 --worker-class eventlet app:app_aging_logmonitor"
        fi
        eval "$cmd"
        echo "$cmd"
        pid=$(get_pid_logmonitor)
        echo "$pid"
    elif [ "$1" == "--stop" ]; then
        pid=$(get_pid_logmonitor)
        if [ "$pid" == "" ]; then
            echo "not running"
        else
            echo "kill $pid"
            kill "$pid"
        fi
    elif [ "$1" == "--status" ]; then
        pid=$(get_pid_logmonitor)
        if [ "$pid" == "" ]; then
            echo "stopped"
        else
            echo "$pid"
            echo "started"
        fi
    else
        echo "${usage}"
    fi
    exit 0
}

function run_gotool() {
    if [ "$1" == "--start" ]; then
        cd "$workdir/go"
        nohup ./gotool &>/dev/null &
        # nohup /root/aging/go/gotool &>/dev/null &
        echo $?
        # todo: get pid and print
        pid=$(get_pid_gotool)
        echo "$pid"
    elif [ "$1" == "--stop" ]; then
        pid=$(get_pid_gotool)
        if [ "$pid" == "" ]; then
            echo "not running"
        else
            echo "kill $pid"
            kill "$pid"
        fi
    elif [ "$1" == "--status" ]; then
        pid=$(get_pid_gotool)
        if [ "$pid" == "" ]; then
            echo "stopped"
        else
            echo "$pid"
            echo "started"
        fi
    else
        echo "${usage}"
    fi
    exit 0
}

function run_resetdb(){
    python3 manage.py deletedb_mysql --table
    python3 manage.py deletedb_sqlite --table
    python3 manage.py createdb_mysql --table --data
    python3 manage.py createdb_sqlite --table --data
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
    --requirements)
        run_requirements
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
    --logmonitor)
        run_logmonitor $2 $3
        ;;
    --gotool)
        run_gotool $2
        ;;
    --resetdb)
        run_resetdb
        ;;
    *)
        echo "$usage"
        exit 1
        ;;
  esac
fi
            
