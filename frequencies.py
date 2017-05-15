#!/usr/bin/env python3

from multiprocessing import Manager

from util import map_colors

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
    manager = Manager()
    by_pixel_count = manager.dict()
    by_occurrence = manager.dict()
    def cb(url, colors):
        for entry in colors:
            color = tuple(entry[1])
            if color in by_pixel_count:
                by_pixel_count[color] += entry[0]
                by_occurrence[color] += 1
            else:
                by_pixel_count[color] = entry[0]
                by_occurrence[color] = 1
        log.debug('Indexed {}'.format(url))
    map_colors(cb)
    return by_pixel_count, by_occurrence

def load_freq_by_pixel_count():
    with open(FREQ_BY_PIXEL_COUNT_PKL, 'rb') as f:
        return pickle.load(f)

def load_freq_by_occurrence():
    with open(FREQ_BY_OCCURRENCE_PKL, 'rb') as f:
        return pickle.load(f)

def write_to_files():
    by_pixel_count, by_occurrence = get_frequencies()
    print(by_pixel_count)
    # sorted_keys = sorted(by_pixel_count.keys(), key=lambda x: by_pixel_count[x])
    # with open(FREQ_BY_PIXEL_COUNT_TXT, 'w') as f:
    #     for key in sorted_keys:
    #         f.write('{}\t{}\n'.format(key, by_pixel_count[key]))
    # log.debug('Wrote {}...'.format(FREQ_BY_PIXEL_COUNT_TXT))
    # with open(FREQ_BY_OCCURRENCE_TXT, 'w') as f:
    #     for key in sorted_keys:
    #         f.write('{}\t{}\n'.format(key, by_occurrence[key]))
    # log.debug('Wrote {}...'.format(FREQ_BY_OCCURRENCE_TXT))
    # with open(FREQ_BY_PIXEL_COUNT_PKL, 'wb') as f:
    #     pickle.dump(by_pixel_count, f)
    # log.debug('Wrote {}...'.format(FREQ_BY_PIXEL_COUNT_PKL))
    # with open(FREQ_BY_OCCURRENCE_PKL, 'wb') as f:
    #     pickle.dump(by_occurrence, f)
    # log.debug('Wrote {}...'.format(FREQ_BY_OCCURRENCE_PKL))

if __name__ == '__main__':
    write_to_files()
