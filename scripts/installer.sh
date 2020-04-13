#! /usr/bin/env bash
#
set -u
set +e
# set -o noglob
#
workdir=$(cd "$(dirname $0)" && pwd)
topdir=$(cd "${workdir}" && cd .. && pwd)
scriptdir=${workdir}
cd "${workdir}"
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

   ____ _____   _     _       _     _   _                  _         _          _____         _     _____           _ 
  / ___| ____| | |   (_) __ _| |__ | |_(_)_ __   __ _     / \  _   _| |_ ___   |_   _|__  ___| |_  |_   _|__   ___ | |
 | |  _|  _|   | |   | |/ _  | '_ \| __| |  _ \ / _  |   / _ \| | | | __/ _ \    | |/ _ \/ __| __|   | |/ _ \ / _ \| |
 | |_| | |___  | |___| | (_| | | | | |_| | | | | (_| |  / ___ \ |_| | || (_) |   | |  __/\__ \ |_    | | (_) | (_) | |
  \____|_____| |_____|_|\__  |_| |_|\__|_|_| |_|\__  | /_/   \_\__ _|\__\___/    |_|\___||___/\__|   |_|\___/ \___/|_|
                        |___/                   |___/                                                                 

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
  apt update
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

function init_mariadb_config(){
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

function init_mariadb_db(){
  read -p "Initialize ge database (Note that this will empty your data, Y/n)?" opt
  if [ 'n' == "$opt" ]; then
    return 1
  fi
  read -p "hostname[localhost]: " hostname
  if [ '' == "$hostname" ]; then hostname='localhost'; fi
  read -p "user[root]: " user
  if [ '' == "$user" ]; then user='root'; fi
  read -p "password[123456]: " password
  if [ "" == "$password" ]; then password='123456'; fi
  sqlfile="${scriptdir}/dbinit.sql"
  mysql -h${hostname} -u${user} -p${password} < ${sqlfile}
  echo
}

function git_clone(){
  git clone https://github.com/linanster/aging.git
}

function customize(){
  # 1. set alias
  sed -i '/my_custom_start/, /my_custom_end/ d' /etc/bash.bashrc
  cat << eof >> /etc/bash.bashrc
# my_custom_start
alias ls='ls --color=auto'
alias ll='ls -l'
alias la='ls -A'
alias l='ls -CF'
alias l.='ls -d .*'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias dir='dir --color=auto'
alias vdir='vdir --color=auto'
# my_custom_end
eof

  # 2. set up vim
  apt remove vim-common
  apt install vim

  # 3. set up ssh.service
  sed -i '/^PermitRootLogin/ s/^/# /' /etc/ssh/sshd_config
  sed -i '/PermitRootLogin/ a PermitRootLogin yes' /etc/ssh/sshd_config
  sed -i '/^StrictModes/ s/^/# /' /etc/ssh/sshd_config
  sed -i '/StrictModes/ a StrictModes no' /etc/ssh/sshd_config
  systemctl enable ssh.service
  systemctl restrat ssh.service

  # 4. set up git client
  git config --global user.name linan
  git config --global user.email believelinan@aliyun.com
  git config --global color.ui true
  git config --global push.default simple
}

function chmod_dir(){
  chmod -R 700 "${topdir}"
}

function install_service(){
  cd "${scriptdir}"
  cp aging.service /usr/lib/systemd/system
  systemctl enable aging.service
  systemctl restart aging.service
  systemctl status aging.service
}
function uninstall_service(){
  cd "${scriptdir}"
  systemctl stop aging.service
  systemctl disable aging.service
  rm -f /usr/lib/systemd/system/aging.service
}

function user_modification(){
  deluser pi sudo
  gpasswd -d pi sudo
  # userdel pi
  # groupdel pi
  useradd -m -s /bin/bash user1
  echo "user1:a" | chpasswd -m
  cp /etc/sudoers /etc/sudoers.bak
  cp /etc/group /etc/group.bak
  sed -i '/%sudo/ s/^/# /' /etc/sudoers
  sed -i 's/pi$//' /etc/group
  sed -i 's/$/user1/' /etc/group
}

function option1(){
  conf_apt
  green "option1 done!"
}
function option2(){
  customize
  green "option2 done!"
}
function option3(){
  install_python3
  green "option3 done!"
}
function option4(){
  install_mariadb
  green "option4 done!"
}
function option5(){
  init_mariadb_config
  init_mariadb_db
  green "option5 done!"
}
function option6(){
  git_clone
  green "option6 done!"
}
function option7(){
  chmod_dir 
  green "option7 done!"
}
function option8(){
  install_service
  green "option8 done!"
}
function option9(){
  uninstall_service
  green "option9 done!"
}
function option10(){
  user_modification
  green "option10 done!"
}


cat << eof
====
1) config apt source
2) raspbian os customization
3) install python3
4) install mariadb
5) config mariadb
6) clone codes from github (-)
7) permission control (-)
8) install service (make sure run not --start)
9) uninstall service
10) user configuration
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
    7)
      option7
      break
      ;;
    8)
      option8
      break
      ;;
    9)
      option9
      break
      ;;
    10)
      option10
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

	
