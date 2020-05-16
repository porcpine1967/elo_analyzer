#!/usr/bin/env python
from collections import defaultdict
import json
import os
import sys

import requests

MAX_DOWNLOAD = 10000
URL_TEMPLATE = 'https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id=3&start={start}&count={count}'

def country_elo():
    country_counter = defaultdict(lambda: [])
    records = 0
    download_record_count = 0
    start = 1
    while True:
        print("Downloading from {} to {}".format(start, start - 1 + MAX_DOWNLOAD))
        r = requests.get(URL_TEMPLATE.format(start=start, count=MAX_DOWNLOAD))
        if r.status_code != 200:
            print(r.text)
            sys.exit(1)
        d = json.loads(r.text)
        print(d.keys())
        if not records:
            records = d['total']
        for record in d['leaderboard']:
            country_counter[record['country']].append(record['rating'])
            download_record_count += 1
        if download_record_count >= records:
            break
        start = MAX_DOWNLOAD + start
    with open('results.json', 'w') as f:
        f.write(json.dumps(country_counter))
if __name__ == '__main__':
    if os.path.exists('results.json'):
        print('Already done')
    else:
        country_elo()
    
