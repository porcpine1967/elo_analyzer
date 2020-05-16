#!/usr/bin/env python
import json
import matplotlib.pyplot as plt


import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

with open('results.json') as f:
    d = json.load(f)
x = []
for l in d.values():
    x.extend(l)

# num_bins = 500
# n, bins, patches = plt.hist(x, num_bins, facecolor='blue', alpha=0.5)
# plt.show()
print(sum(x)/len(x))
print(np.mean(x))
