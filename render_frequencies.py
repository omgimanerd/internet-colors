#!/usr/bin/env python3

from jinja2 import Template

from frequencies import load_freq_by_pixel_count, load_freq_by_occurrence
from search_color import search_colors
from util import *

import itertools
import logging
import pickle
import os

D2N_THRESHOLD = 7500

logging.basicConfig(level=logging.DEBUG)

def get_dist_to_next(rgb_colors):
    d2n = []
    for i in range(len(rgb_colors) - 1):
        d2n.append(get_color_distance(rgb_colors[i], rgb_colors[i + 1]))
    d2n.append(999999)
    return d2n

def get_template(template_path):
    with open(template_path) as html:
        return Template(html.read())

def get_color_objects(colors):
    sorted_rgb_colors = sorted(colors, key=lambda x: colors[x])[-200:][::-1]
    sorted_hex_colors = [rgb_to_hex(color) for color in sorted_rgb_colors]
    text_colors = [get_foreground_color(color) for color in sorted_rgb_colors]
    d2n = get_dist_to_next(sorted_rgb_colors)
    return [{
        'rgb': tuple(sorted_rgb_colors[i]),
        'hex': sorted_hex_colors[i],
        'text': text_colors[i],
        'd2n': d2n[i]
    } for i in range(len(sorted_rgb_colors))]

def render():
    template = get_template('render/templates/color_freq.html')
    colors = get_color_objects(load_freq_by_pixel_count())
    with open('render/output/freq_by_pixel_count.html', 'w') as out:
        out.write(template.render(data=colors))
    logging.debug('Wrote freq_by_pixel_count.html')
    filtered = list(filter(lambda x: x['d2n'] > D2N_THRESHOLD, colors))
    with open('render/output/filtered_freq_by_pixel_count.html', 'w') as out:
        out.write(template.render(data=filtered))
    logging.debug('Wrote filtered_freq_by_pixel_count.html')
    top = filtered[:35]
    rgb = [list(data['rgb']) for data in top]
    matches = search_colors(rgb)
    template = get_template('render/templates/color_freq_websites.html')
    for color in matches:
        matches[color] = sorted(
            matches[color], key=lambda match: match[1])[::-1][:5]
    with open('render/output/freq_by_pixel_count_websites.html', 'w') as out:
        out.write(template.render(data=top, matches=matches))
    logging.debug('Wrote freq_by_pixel_count_websites.html')

if __name__ == '__main__':
    render()
