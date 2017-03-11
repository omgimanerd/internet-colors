#!/usr/bin/env python3

from collections import Counter

import json

COLORS_BINARY = 'colors.bin'

def load():
    return pickle.load(COLORS_BINARY)

"""
data format:
[
  [frequency, [r, g, b]],
  [frequency, [r, b, b]],
  ...
]
"""
def freq_by_pixel_count(data):
    counter = Counter()
    for entry in data:
        entry[tuple(data[1])] += data[0]
    return counter

if __name__ == '__main__':
    f = freq_by_pixel_count(load())
    pickle.dump(f, open('freq_by_pixel_count'))
    
