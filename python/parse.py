# find /tmp/cache -type f -exec grep -F -w -a 'KEY' {} \; |cut -f1
# find /tmp/cache -type f | wc -l

import os
import sys
import time
import json
import requests
from metrics import Metrics
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

def collect_metrics():
  metrics = dict()
  metrics['timestamp'] = time.ctime()
  # total items in cache
  cache_item_count = int(os.popen("find /tmp/cache -type f | wc -l").read())
  metrics['cache_item_count'] = cache_item_count
  # total size of cached files
  cache_item_size = os.popen("du -ah -d0 /tmp/cache |cut -f1").read().split()[0]
  metrics['cache_item_size'] = cache_item_size

  # cached items by type
  types = ['js', 'png', 'css', 'jpg', 'svg', 'others']
  tmp = os.popen("find /tmp/cache -type f -exec grep -w -a '^KEY:' {} \; |cut -f3 -d:").read().split()
  items_bytype = dict()
  for t in types:
    items_bytype[t] = 0

  for f in tmp:
    try:
      t = f[f.rindex('.')+1:len(f)].lower()
      if t in items_bytype:
        items_bytype[t] += 1
      else:
        items_bytype['others'] += 1
    except BaseException as ex:
      pass
  metrics['items_bytype'] = items_bytype

  # cached bandwidth
  hit_bytes = 0
  # cached requests
  hit_requests = 0
  # uncached bandwidth
  miss_bytes = 0
  # uncached requests
  miss_requests = 0

  other_bytes = 0
  other_requests = 0
  with open('/tmp/log/jenkins_access.log.bak', 'rt') as f:
    for ln in f:
      fields = ln.split('|')
      if fields[3].split()[0] == 'HIT':
        hit_bytes += int(fields[2])
        hit_requests += 1
      elif fields[3].split()[0] == 'MISS':
        miss_bytes += int(fields[2])
        miss_requests += 1
      else:
        other_bytes += int(fields[2])
        other_requests += 1

  # total bandwidth
  total_bytes = hit_bytes + miss_bytes + other_bytes
  # total requests
  total_requests = hit_requests + miss_requests + other_requests

  metrics['hit_bytes'] = hit_bytes
  metrics['hit_requests'] = hit_requests
  metrics['miss_bytes'] = miss_bytes
  metrics['miss_requests'] = miss_requests
  metrics['total_bytes'] = total_bytes
  metrics['total_requests'] = total_requests
  return metrics

if __name__ == "__main__":
  m = collect_metrics()
  print(m)
  # default store to database
  if len(sys.argv) == 1 or sys.argv[1] == 'DB':
    engine = create_engine('mysql+pymysql://metrics:IQY0n2EEdvZCgiJ_@db/nginx_metrics')
    DBSession = sessionmaker(bind=engine)
    with DBSession() as session:
      metrics = Metrics()
      metrics.collect_tms = m['timestamp']
      metrics.cache_item_count = m['cache_item_count']
      metrics.cache_item_size = m['cache_item_size']
      metrics.items_bytype = json.dumps(m['items_bytype'])
      metrics.hit_bytes = m['hit_bytes']
      metrics.hit_requests = m['hit_requests']
      metrics.miss_bytes = m['miss_bytes']
      metrics.miss_requests = m['miss_requests']
      metrics.total_bytes = m['total_bytes']
      metrics.total_requests = m['total_requests']
      try:
        session.add(metrics)
        session.commit()
      except IntegrityError:
        session.rollback()
      except BaseException as ex:
        session.rollback()
        print(type(ex))
        print(ex)
  # write to json file
  elif sys.argv[1] == 'JSON':
    with open('/tmp/out.json', 'at') as f:
      jsonstr = json.dumps(m, indent=4)
      f.write(jsonstr+'\n')
  # post to an endpoint
  else:
    headers = {'content-type': 'application/json'}
    url = 'https://enlq470brd9259a.m.pipedream.net'
    with requests.Session() as s:
      resp = s.post(url, data=json.dumps(m), headers=headers)
      print(resp.status_code)
