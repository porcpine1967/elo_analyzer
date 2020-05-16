#!/usr/bin/env python

from collections import defaultdict
import json

from countries import country_dict

def analyze():
    cd = country_dict()
    with open('results.json') as f:
        d = json.load(f)
    region_dict = defaultdict(lambda: 0)
    for country_code, l in d.items():
        if country_code in cd:
            country = cd[country_code]
            region_dict[country.loc] += len(l)
    for region, length in region_dict.items():
        print(region, length)
if __name__ == '__main__':
    analyze()
