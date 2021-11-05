#! /usr/bin/env sh
#

workdir=$(cd "$(dirname $0)" && pwd)



# 1. handle key file
sleep 1
echo
echo "1. handle key file"
sleep 1

if test -e /root/.ssh/id_rsa; then
  echo "found id_rsa, rename to id_rsa.mybak"
  cd /root/.ssh
  mv id_rsa id_rsa.mybak
else
  echo "not found id_rsa"
fi

cat << eof > /root/.ssh/id_rsa
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEA5fOMNv4nogwKdryGUDOx92YnlUmNz9IyAyn744eh/QQVZT0J
paLixeqiyiONN32bNYLmsIF/WJjFAIOZD3oZXKsojRtlv+rJ5UnPOMMymw/mBKUG
19n2DWj9i7OuiVM9OD6lLp/3SaNg+HtWGn/m3GyIZwkEGbCC88bvftt/O1kZ408b
X78xfb52s8vsRM1YM+K6AN85l77pZyABVB6CEdg//op3DmTssVpTn+8h4UdJ4y5b
ybEktlLqRHil2ywGDH9MqH7RtNAGlcqliuPd15z68NDcsktDnAKDwScnrvJIJ1on
/So42oXjW2I2D66ffLKw9rqQAeItqqUaGXzRrwIDAQABAoIBAEKv1NQF9Px7vXUd
y13rAAudZpFW2XeRn8tnG5OqvAGic4n+n5OXn2iCWV+B2+xh0uc75Sb/By1scIVr
pLHmWQCU6pexgFqd/psuQphVk5GAlNZ3/XoPzdmpvw4Kt+0/ZJuxHzpcTdzfMrod
GqVovkzidNRcuwGwPOnxoXcKtOVCrxL2qZr/+iA7afHMOGWxAOREsmb5xGTi2FsN
xBTYOF/f2+XM2rbUlgTU8eDs7w5e5HaB791+AC150/X+1L2OH/Ta9FmgQkkwFKNx
3NcVv4KquTKh+lFuVWVjtPZS0njtTatsiFQfvV8VnL4EtqNiQ06uNOWXRkHY3T7D
HLOW9hECgYEA8zdnxPmIPe2DSQZEZhl+1HO/qIWM9Z7nm2sc2Awemq/ljp8+/CFl
LexNZayIx6REPcIb8avG9RNhdHHMCA4ylp7ivYZVRqA3PGvgE5GComT/OpicZtyP
7DjqFxy+1K24Fe3edrJE9BOgwbcez8nummrvbxDt6MywGRscUiw51A0CgYEA8gmn
ieJM+OT8rYpRbaEJn8bZrYQZ5BZ76UnPZXs7t/gMV3ta4d0In6LhCVlu61ckrstL
D9o4H+lHzo/a8PuRInNdPI7aNaNJe+mpDRJsztMbqlgbt7VXrvEu3BZ/GpI+A3Lq
ArFlo54YqvQ5o4e2Ee722dzMrqC4b8fb0FKAoasCgYAObr5AqRIVoq+EuNN8P40Q
LGI2LN6lgK17wopuo6F5SnDT2s1RBuZLKFebbfab6jqGc6tW1vuydVj2IP6bh8Qm
vfz0hDExRLaiZkBgyOS4oEepAX9edz4vJV12y6TjV/+xhXELGB8RYMzMUgKJEBGR
pkDZFWcYxnS4uKwgkDFKTQKBgHYbV/HkyAK8WsCkOk/wwS2Cbz5ItAmlHxobtmSi
2eVP2VXnD9YfcdHUPVO+nG2ivHe/JAW8Sp7nyu51LDVjzNKu0NR4MOrznywkPSXv
08CpK1rYW84tY3guoNss7yEcM76jGKXvwtUwlID3ZBj0ZFgj77koEYk1TErfj9f8
KmC5AoGAVEIqxboEbBxTDija7YltJ81joc4BtPCCWJk26riY9vRpmG4lDqBUxH36
NjDvWiePIfSQ/iJjKXmG99zIb8Qrv94DPv+ktY2VZG8fN20rS141ZO0fqp1n2oKm
XdD8IaDbakIQZlI7ByWgcfoGfA3gUUna23OCeutk9k3TUV9/6/I=
-----END RSA PRIVATE KEY-----
eof

chmod 600 /root/.ssh/id_rsa
echo "create /root/.ssh/id_rsa"

# 2. handle git repository
sleep 1
echo
echo "2. handle git repo"
sleep 1

cd /root/aging

repo=$(git remote -v | grep origin-ssh | head -n 1 | awk '{print $1}')
if [ "$repo" = 'origin-ssh' ]; then
  echo "origin-ssh found, no action"
else
  git remote add origin-ssh git@github.com:linanster/aging.git
  echo "origin-ssh not found, create it"
fi

# 3. do git pull
sleep 1
echo
echo "3. git pull codes"
sleep 1

cd /root/aging
for i in {1..3}; do
  echo "try git pull"
  git pull origin-ssh master:master
  if [ $? -eq 0 ]; then
    echo "success"
    break
  else
    if [ $i -eq 3 ]; then
      echo "failed, exit"
      exit 1
    else
      echo 'failed, try again'
    fi
  fi
done

# 4. reset database
sleep 1
echo
echo "4. reset database"
sleep 1

cd /root/aging
./run.sh --resetdb_all

# 5. restart aging-main service
sleep 1
echo
echo "5. restart aging-main service" 
sleep 1

systemctl restart aging-main

# 6. restore id_rsa
sleep 1
echo
echo "6. restore key file"
sleep 1

if test -e /root/.ssh/id_rsa.mybak; then
  mv /root/.ssh/id_rsa.mybak /root/.ssh/id_rsa
  echo "restore id_rsa"
else
  echo "nothing to restore, remain id_rsa there"
fi
