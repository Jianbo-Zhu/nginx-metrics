mv /tmp/log/jenkins_access.log /tmp/log/jenkins_access.log.bak
kill -USR1 `cat /run/nginx.pid`
sleep 1
python3 /usr/src/app/parse.py HTTP
mkdir -p /tmp/log/archive
mv -f /tmp/log/jenkins_access.log.bak /tmp/log/archive/jenkins_access.log.bak