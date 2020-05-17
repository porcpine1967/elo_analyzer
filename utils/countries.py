#!/usr/bin/env python

import csv
import pathlib
CURRENT_DIR = pathlib.Path(__file__).parent.absolute()

import numpy as np

class Country():
    def __init__(self, row):
        self.name, self.code, _, _, lat, long = row
        self.lat = float(lat)
        self.long = float(long)
        self.loc = self.name
        self.elos = []

    def __str__(self):
        return "{}, {}, lat: {}, long: {}, loc: {}".format(self.name, self.code, self.lat, self.long, self.loc)


def country_map():
    mappings = {}
    with open('{}/{}'.format(CURRENT_DIR, 'country_map.csv')) as f:
        reader = csv.reader(f)
        for row in reader:
            mappings[row[0]] = row[1]
    return mappings

def country_dict():
    countries = {}
    mappings = country_map()
    with open('{}/{}'.format(CURRENT_DIR, 'countries_codes_and_coordinates.csv')) as f:
        reader = csv.reader(f)
        for row in reader:
            country = Country(row)
            if country.code in mappings:
                country.loc = mappings[country.code]
            countries[country.code] = country
    return countries

if __name__ == '__main__':
    c = country_dict()
    for x in c.values():
        print(x)
