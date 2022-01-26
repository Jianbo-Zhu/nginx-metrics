# nginx-metrics
For collecting nginx metrics
# steps
Make sure you have docker installed.
1. Modify python/run.sh as shown below, to switch between `DB`, `JSON file`, and `HTTP POST` options
``` bash
mv /tmp/log/jenkins_access.log /tmp/log/jenkins_access.log.bak
kill -USR1 `cat /run/nginx.pid`
sleep 1
python3 /usr/src/app/parse.py HTTP #HTTP -> HTTP POST, DB -> database, JSON -> json file
mkdir -p /tmp/log/archive
mv -f /tmp/log/jenkins_access.log.bak /tmp/log/archive/jenkins_access.log.bak
```
2. start run the compose file

```
docker compose up -d
```
