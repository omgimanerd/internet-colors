#!/usr/bin/env python3

from collections import Counter

from util import map_colors

import json
import pickle

COLORS_FILE = 'data/colors.txt'
FREQ_BY_PIXEL_COUNT_TXT = 'data/freq_by_pixel_count.txt'
FREQ_BY_PIXEL_COUNT_PKL = 'data/freq_by_pixel_count.pkl'
FREQ_BY_OCCURRENCE_TXT = 'data/freq_by_occurrence.txt'
FREQ_BY_OCCURRENCE_PKL = 'data/freq_by_occurrence.pkl'

def get_colors(line):
    data = line.split('_')
    return data[0], json.loads(data[1])

def get_frequency_by_pixel_count():
    freq = Counter()
    def cb(url, colors):
        for entry in colors:
            freq[tuple(entry[1])] += entry[0]
        print('Indexed {}...'.format(url))
    map_colors(cb)
    return freq

def load_freq_by_pixel_count():
    with open(FREQ_BY_PIXEL_COUNT_PKL, 'rb') as f:
        return pickle.load(f)

def get_frequency_by_occurrence():
    freq = Counter()
    def cb(url, colors):
        for entry in colors:
            freq[tuple(entry[1])] += 1
        print('Indexed {}...'.format(url))
    map_colors(cb)
    return freq

def load_freq_by_occurrence():
    with open(FREQ_BY_OCCURRENCE_PKL, 'rb') as f:
        return pickle.load(f)

def write_to_files(freq, txt_name, pkl_name):
    sorted_keys = sorted(freq.keys(), key=lambda x: freq[x])
    with open(txt_name, 'w') as f:
        for key in sorted_keys:
            f.write('{}\t{}\n'.format(key, freq[key]))
    print('Wrote {}...'.format(txt_name))
    with open(pkl_name, 'wb') as f:
        pickle.dump(freq, f)
    print('Wrote {}...'.format(pkl_name))


if __name__ == '__main__':
    freq = get_frequency_by_pixel_count()
    write_to_files(freq, FREQ_BY_PIXEL_COUNT_TXT, FREQ_BY_PIXEL_COUNT_PKL)

    print('Frequency by pixel count written... Press any key to continue...')
    t = input()

    freq = get_frequency_by_occurrence()
    write_to_files(freq, FREQ_BY_OCCURRENCE_TXT, FREQ_BY_OCCURRENCE_PKL)
