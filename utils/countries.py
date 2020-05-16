#!/usr/bin/env python

import csv
import pathlib

CONSOLIDATIONS = {

}

class Country():
    def __init__(self, row):
        self.name, self.code, lat, long, self.player_count, self.loc = row
        self.lat = float(lat)
        self.long = float(long)
    def __str__(self):
        return "{}, {}, lat: {}, long: {}".format(self.name, self.code, self.lat, self.long)

def country_dict():
    countries = {}
    with open('{}/{}'.format(pathlib.Path(__file__).parent.absolute(), 'countries.csv')) as f:
        reader = csv.reader(f)
        for row in reader:
            countries[row[1]] = Country(row)
    return countries

if __name__ == '__main__':
    c = country_dict()
    for x in c.values():
        print(x)
