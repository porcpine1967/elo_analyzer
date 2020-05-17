#!/usr/bin/env python
import json
import pathlib
import sys

import numpy as np

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))
from utils.countries import country_dict

HEADER = """<html>
<head>
<title>Test Elo table</title>
<style>
table, th, td {border-style: solid; border-width: 1px; border-color: black; padding: 5px;}
td {text-align: right}
td.name {text-align: left}
</style>
</head>
<body>
<table>
"""

class Region():
    def __init__(self, name):
        self.name = name
        self.elos = []
    @property
    def median(self):
        return np.median(self.elos)

    def expected_buckets(self):
        # Assumes divided into six buckets
        cnt = len(self.elos)
        return [.025*cnt, .135*cnt, .34*cnt, .34*cnt, .135*cnt, .025*cnt,]

    def to_html(self, median, edges):
        html = '<tr><td class="name">{}</td><td>{}</td><td style="{}">{}</td>'.format(self.name, len(self.elos), style(median, self.median), int(self.median))
        eb = self.expected_buckets()
        for idx, bucket in enumerate(self.buckets(edges)):
            html += '<td style="{}">{}</td>'.format(style(eb[idx], len(bucket)), len(bucket))
        html += '</tr>'
        return html

    def buckets(self, edges):
        holder = []
        for i in range(len(edges) + 1):
            holder.append([])
        for score in self.elos:
            found = False
            for idx, edge in enumerate(sorted(edges, reverse=True)):
                if score > edge:
                    holder[len(edges) - idx].append(score)
                    found = True
                    break
            if not found:
                holder[0].append(score)
        return holder

def style(expected, actual):
    # returns the value for style for a given condition
    color = 'black'
    if expected > actual:
        bgcolor = 0
        lightness = (float(expected) - actual)/expected
        if lightness > .55:
            color = 'white'
    else:
        bgcolor = 240
        lightness = (float(actual) - expected)/actual
        if lightness > .4:
            color = 'white'

    return "color:{};background-color:hsl({},100%,{}%)".format(color,bgcolor, 100 - int(lightness*100)/2)
    

if __name__ == '__main__':
    with open('results.json') as f:
        d = json.load(f)
    c = country_dict()
    total = Region('Total')
    no_country = Region('No Country')
    regions = {'nc': no_country}
    for cc in d:
        if cc in c and len(d[cc]) > 0:
            country = c[cc]
            if country.loc not in regions:
                regions[country.loc] = Region(country.loc)
            regions[country.loc].elos.extend(d[cc])
        else:
            no_country.elos.extend(d[cc])
        total.elos.extend(d[cc])

    total_cnt = len(total.elos)
    total_elos = sorted(total.elos)
    median = np.median(total_elos)
    edges = [total_elos[int(.025*total_cnt)] - 1, 
             total_elos[int(.16*total_cnt)] - 1,
             int(median) - 1, 
                 total_elos[int(.84*total_cnt)] - 1, 
                 total_elos[int(.975*total_cnt)] -1]
    header_edges = [x + 1 for x in edges]
    print(HEADER)
    print('<tr><th>Country</th><th># players<th>Median ELO</th><th>0-{0[0]}</th><th>{1[0]}-{0[1]}</th><th>{1[1]}-{0[2]}</th><th>{1[2]}-{0[3]}</th><th>{1[3]}-{0[4]}</th><th>&gt; {0[4]}</th></tr>'.format(edges, header_edges))
    print(total.to_html(median, edges))
    for region in sorted(regions.values(), key=lambda x: len(x.elos), reverse=True):
        print(region.to_html(median, edges))
            
