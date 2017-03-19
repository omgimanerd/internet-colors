#!/usr/bin/env python3

from jinja2 import Template

import pickle

FREQ_BY_PIXEL_COUNT_TXT = 'data/freq_by_pixel_count.txt'
FREQ_BY_PIXEL_COUNT_PKL = 'data/freq_by_pixel_count.pkl'
FREQ_BY_OCCURRENCE_TXT = 'data/freq_by_occurrence.txt'
FREQ_BY_OCCURRENCE_PKL = 'data/freq_by_occurrence.pkl'

def load_freq_by_pixel_count():
    return pickle.load(FREQ_BY_PIXEL_COUNT_PKL)

def load_freq_by_occurrence():
    return pickle.load(FREQ_BY_OCCURRENCE_PKL)

def load_pixel_count_template():


if __name__ == '__main__':
