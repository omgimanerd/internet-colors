#!/usr/bin/env python3

from jinja2 import Template

from util import get_color_distance, rgb_to_hex, rgb_to_hsv

import colorsys
import pickle

FREQ_BY_PIXEL_COUNT_TXT = 'data/freq_by_pixel_count.txt'
FREQ_BY_PIXEL_COUNT_PKL = 'data/freq_by_pixel_count.pkl'
FREQ_BY_OCCURRENCE_TXT = 'data/freq_by_occurrence.txt'
FREQ_BY_OCCURRENCE_PKL = 'data/freq_by_occurrence.pkl'
D2N_THRESHOLD = 7500

def get_dist_to_next(rgb_colors):
    d2n = []
    for i in range(len(rgb_colors) - 1):
        d2n.append(get_color_distance(rgb_colors[i], rgb_colors[i + 1]))
    d2n.append(999999)
    return d2n

def load_freq_by_pixel_count():
    with open(FREQ_BY_PIXEL_COUNT_PKL, 'rb') as f:
        return pickle.load(f)

def load_freq_by_occurrence():
    with open(FREQ_BY_OCCURRENCE_PKL, 'rb') as f:
        return pickle.load(f)

def load_template():
    with open('templates/color_freq.html') as html:
        return Template(html.read())

if __name__ == '__main__':
    template = load_template()
    colors = load_freq_by_pixel_count()
    sorted_rgb_colors = sorted(colors, key=lambda x: colors[x])[-200:][::-1]
    sorted_hex_colors = list(map(rgb_to_hex, sorted_rgb_colors))
    sorted_hsv_colors = list(map(rgb_to_hsv, sorted_rgb_colors))
    text_colors = list(map(get_text_color, sorted_rgb_colors))
    d2n = get_dist_to_next(sorted_rgb_colors)
    data = []
    for i in range(len(sorted_rgb_colors)):
        data.append({
            'rgb': sorted_rgb_colors[i],
            'hex': sorted_hex_colors[i],
            'hsv': sorted_hsv_colors[i],
            'text': text_colors[i],
            'd2n': d2n[i]
        })
    with open('output/freq_by_pixel_count.html', 'w') as out:
        out.write(template.render(
            data=data
        ))
    filtered = filter(lambda x: x['d2n'] > D2N_THRESHOLD, data)
    with open('output/filtered_freq_by_pixel_count.html', 'w') as out:
        out.write(template.render(
            data=filtered
        ))
