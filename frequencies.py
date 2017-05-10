#!/usr/bin/env python3

from collections import Counter

from util import map_colors, iter_colors

import json
import logging
import pickle

log = logging.getLogger('frequencies')
log.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
log.addHandler(streamHandler)

COLORS_FILE = 'data/colors.txt'
FREQ_BY_PIXEL_COUNT_TXT = 'data/freq_by_pixel_count.txt'
FREQ_BY_PIXEL_COUNT_PKL = 'data/freq_by_pixel_count.pkl'
FREQ_BY_OCCURRENCE_TXT = 'data/freq_by_occurrence.txt'
FREQ_BY_OCCURRENCE_PKL = 'data/freq_by_occurrence.pkl'

def get_frequencies():
    by_pixel_count = Counter()
    by_occurrence = Counter()
    def cb(url, colors):
        for entry in colors:
            by_pixel_count[tuple(entry[1])] += entry[0]
            by_occurrence[tuple(entry[1])] += 1
        log.debug('Indexed {}'.format(url))
    map_colors(cb)
    return by_pixel_count, by_occurrence

def load_freq_by_pixel_count():
    with open(FREQ_BY_PIXEL_COUNT_PKL, 'rb') as f:
        return pickle.load(f)

def load_freq_by_occurrence():
    with open(FREQ_BY_OCCURRENCE_PKL, 'rb') as f:
        return pickle.load(f)

def write_to_files(by_pixel_count, by_occurrence):
    sorted_keys = sorted(freq.keys(), key=lambda x: freq[x])
    with open(FREQ_BY_PIXEL_COUNT_TXT, 'w') as f:
        for key in sorted_keys:
            f.write('{}\t{}\n'.format(key, by_pixel_count[key]))
    log.debug('Wrote {}...'.format(FREQ_BY_PIXEL_COUNT_TXT))
    with open(FREQ_BY_OCCURRENCE_TXT, 'w') as f:
        for key in sorted_keys:
            f.write('{}\t{}\n'.format(key, by_occurrence[key]))
    log.debug('Wrote {}...'.format(FREQ_BY_OCCURRENCE_TXT))
    with open(FREQ_BY_PIXEL_COUNT_PKL, 'wb') as f:
        pickle.dump(by_pixel_count, f)
    log.debug('Wrote {}...'.format(FREQ_BY_PIXEL_COUNT_PKL))
    with open(FREQ_BY_OCCURRENCE_PKL, 'wb') as f:
        pickle.dump(by_occurrence, f)
    log.debug('Wrote {}...'.format(FREQ_BY_OCCURRENCE_PKL))


if __name__ == '__main__':
    write_to_files(*get_frequencies())
