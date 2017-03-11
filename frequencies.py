#!/usr/bin/env python3

from collections import Counter

import json
import pickle

COLORS_FILE = 'data/colors.txt'

def get_colors(line):
    data = line.split('_')
    return data[0], json.loads(data[1])

def get_frequency_by_pixel_count():
    freq = Counter()
    with open('data/colors.txt') as data:
        for line in data:
            try:
                url, colors = get_colors(line)
                for entry in colors:
                    freq[tuple(entry[1])] += entry[0]
                print('Indexed {}...'.format(url))
            except:
                continue
    return freq

def get_frequency_by_occurrence():
    freq = Counter()
    with open(COLORS_FILE) as data:
        for line in data:
            try:
                url, colors = get_colors(line)
                for entry in colors:
                    freq[tuple(entry[1])] += 1
                print('Indexed {}...'.format(url))
            except:
                continue
    return freq

if __name__ == '__main__':
    freq = get_frequency_by_pixel_count()
    with open('data/freq_by_pixel_count.csv', 'a') as f:
        for color, frequency in freq.items():
            f.write('{}\t{}\n'.format(frequency, color))
