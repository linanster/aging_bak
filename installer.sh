#! /usr/bin/env bash
#
set -u
set +e
# set -o noglob
#
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

# green "hello"
# red "hello"

cat << eof
   _____ ______   _      _       _     _   _                             _               _______        _     _______          _ 
  / ____|  ____| | |    (_)     | |   | | (_)                 /\        (_)             |__   __|      | |   |__   __|        | |
 | |  __| |__    | |     _  __ _| |__ | |_ _ _ __   __ _     /  \   __ _ _ _ __   __ _     | | ___  ___| |_     | | ___   ___ | |
 | | |_ |  __|   | |    | |/ _  |  _ \| __| |  _ \ / _  |   / /\ \ / _  | |  _ \ / _  |    | |/ _ \/ __| __|    | |/ _ \ / _ \| |
 | |__| | |____  | |____| | (_| | | | | |_| | | | | (_| |  / ____ \ (_| | | | | | (_| |    | |  __/\__ \ |_     | | (_) | (_) | |
  \_____|______| |______|_|\__  |_| |_|\__|_|_| |_|\__  | /_/    \_\__  |_|_| |_|\__  |    |_|\___||___/\__|    |_|\___/ \___/|_|
                            __/ |                   __/ |           __/ |         __/ |                                          
                           |___/                   |___/           |___/         |___/                                           
eof

echo
echo

function conf_apt(){
  if [ -f /etc/apt/sources.list ]; then
    read -p "/etc/apt/sources.list exist, proceed anyway(Y/n)? " opt
    if [ "$opt" == "n" ]; then
      return 1
    fi
  fi
  mv /etc/apt/sources.list /etc/apt/sources.list.bak
  echo "deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi" > /etc/apt/sources.list
  wget http://raspbian.raspberrypi.org/raspbian.public.key
  apt-key add raspbian.public.key
}

function install_python3(){
  if python3 --version &> /dev/null; then
    read -p "$(python3 --version) already installed, proceed anyway(Y/n)? " opt
    if [ "$opt" == "n" ]; then
      return 1
    fi
  fi
  apt install python3.6 python3.6-dev python3-pip
}

function install_mariadb(){
  if dpkg -l mariadb-server &>/dev/null; then
    read -p "$(dpkg -l mariadb-server | awk '/mariadb-server/{print $2,$3}') already installed, proceed anyway(Y/n)? " opt
    if [ "$opt" == "n" ]; then
      return 1
    fi
  fi
  apt install mariadb-server mariadb-client
  systemctl enable mariadb
  systemctl restart mariadb
}

function init_config_mariadb(){
  read -p "Config MariaDB again(root password listening address, Y/n)?" opt
  if [ 'n' == "$opt" ]; then
    return 1
  fi
  mysql -e "update mysql.user set password=PASSWORD('123456'),host='%' where user='root' and host='localhost';"
  mysql -e "UPDATE mysql.user SET plugin='mysql_native_password' WHERE user = 'root';"
  mysql -e "flush privileges;"
  if ! fgrep -q "bind-address=0.0.0.0" /etc/mysql/mariadb.cnf; then
    echo "[mysqld]" >> /etc/mysql/mariadb.cnf
    echo "bind-address=0.0.0.0" >> /etc/mysql/mariadb.cnf
  fi
  systemctl restart mariadb
  echo
}

function init_mariadb_tables(){
  read -p "Initialize MariaDB tables again(Note that this will empty your data, Y/n)?" opt
  if [ 'n' == "$opt" ]; then
    return 1
  fi
  read -p "hostname[localhost]: " hostname
  if [ '' == "$hostname" ]; then hostname='localhost'; fi
  read -p "user[root]: " user
  if [ '' == "$user" ]; then user='root'; fi
  read -p "password[123456]: " password
  if [ "" == "$password" ]; then password='123456'; fi
  read -p "script file path[.aging/mariadb/db1.sql]: " path
  if [ "" == "$path" ]; then path='./aging/mariadb/db1.sql'; fi
  mysql -h${hostname} -u${user} -p${password} < ${path}
  echo
}

function config_flask(){
  pip3 install flask flask-script flask-blueprint flask-sqlalchemy flask-migrate flask-session pymysql
}

function git_clone(){
  git clone https://github.com/linanster/aging.git
}

function option1(){
  conf_apt
  green "option1 done!"
}
function option2(){
  install_python3
  green "option2 done!"
}
function option3(){
  install_mariadb
  green "option3 done!"
}
function option4(){
  init_config_mariadb
  init_mariadb_tables
  green "option4 done!"
}
function option5(){
  config_flask
  green "option5 done!"
}
function option6(){
  git_clone
  green "option6 done!"
}
function option7(){
  green "option7 done!"
}

cat << eof
====
1) config apt source
2) install python3
3) install mariadb
4) config mariadb [applied only once]
5) config flask framework
6) clone codes from github
7) raspbian os customized configuration
q) quit 
====
eof

while echo; read -p "Enter your option: " option; do
  case $option in
    1)
      option1
      break
      ;;
    2)
      option2
      break
      ;;
    3)
      option3
      break
      ;;
    4)
      option4
      break
      ;;
    5)
      option5
      break
      ;;
    6)
      option6
      break
      ;;
    q|Q)
      break
      ;;
    *)
      echo "invalid option, enter again..."
      continue
  esac
done

	
