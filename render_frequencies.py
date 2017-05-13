#!/usr/bin/env python3

from jinja2 import Template

from frequencies import load_freq_by_pixel_count, load_freq_by_occurrence
from search_color import search_colors
from util import *

import itertools
import pickle
import os

D2N_THRESHOLD = 500000

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
        'rgb': sorted_rgb_colors[i],
        'hex': sorted_hex_colors[i],
        'text': text_colors[i],
        'd2n': d2n[i]
    } for i in range(len(sorted_rgb_colors))]

def render():
    template = get_template('render/templates/color_freq.html')
    colors = get_color_objects(load_freq_by_pixel_count())
    # with open('output/freq_by_pixel_count.html', 'w') as out:
    #     out.write(template.render(data=data))
    filtered = filter(lambda x: x['d2n'] < D2N_THRESHOLD, colors)
    # with open('output/filtered_freq_by_pixel_count.html', 'w') as out:
    #     out.write(template.render(data=filtered))
    top20 = itertools.islice(filtered, 20)
    rgb = [list(data['rgb']) for data in top20]
    template = get_template('render/templates/color_freq_websites.html')
    matches = search_colors(rgb)
    with open('output/freq_by_pixel_count_websites.html', 'w') as out:
        out.write(template.render(data=top20, matches=matches))

if __name__ == '__main__':
    if not os.path.exists('output'):
        os.makedirs('output')
    render()
