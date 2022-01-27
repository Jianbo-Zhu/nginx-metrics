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
3. checkout the database by visiting http://localhost:8080, login with `root/nv2mNzUig3fG8RUz`
4. for `JSON` option, it writes in `shared/out.json`
5. for `HTTP` option, need to update the `python/parse.py`, replace `https://enlq470brd9259a.m.pipedream.net` with whatever url you got from https://requestbin.com

# how it works
1. there is a cron job on the `nginx-local` container, triggers the python collecting code every 5 minutes
2. the nginx is proxing a backend jenkins server, you can access by `http://localhost`, and make serveral refreshes to generates access log entries.