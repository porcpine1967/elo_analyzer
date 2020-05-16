#!/usr/bin/env python
import json
import pathlib
import sys

import matplotlib.pyplot as plt

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))
from utils.countries import country_dict

if __name__ == '__main__':
    with open('results.json') as f:
        d = json.load(f)
    c = country_dict()
    x = []
    y = []
    for cc in d:
        if cc in c and len(d[cc]) > 200:
            country = c[cc]
            print(country.name, len(d[cc]))
            x.append(country.long)
            y.append(country.lat)
    print(len(x))
    print(len(y))
    plt.scatter(x, y)
    plt.show()

            
