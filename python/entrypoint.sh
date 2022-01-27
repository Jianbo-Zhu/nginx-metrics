#!/bin/sh
# start crond
crond -b -L /tmp/crond.log -c /etc/crontab
# the main process
nginx -g "daemon off;"
