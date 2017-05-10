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

def load_template():
    with open('render/templates/color_freq.html') as html:
        return Template(html.read())

if __name__ == '__main__':
    template = load_template()
    colors = load_freq_by_pixel_count()
    sorted_rgb_colors = sorted(colors, key=lambda x: colors[x])[-200:][::-1]
    sorted_hex_colors = [rgb_to_hex(color) for color in sorted_rgb_colors]
    sorted_hsv_colors = [rgb_to_hsv(color) for color in sorted_rgb_colors]
    text_colors = [get_foreground_color(color) for color in sorted_rgb_colors]
    d2n = get_dist_to_next(sorted_rgb_colors)
    data = [{
        'rgb': sorted_rgb_colors[i],
        'hex': sorted_hex_colors[i],
        'hsv': sorted_hsv_colors[i],
        'text': text_colors[i],
        'd2n': d2n[i]
    } for i in range(len(sorted_rgb_colors))]
    if not os.path.exists('render/output'):
        os.makedirs('render/output')
    """
    with open('render/output/freq_by_pixel_count.html', 'w') as out:
        out.write(template.render(
            data=data
        ))
    """
    filtered = filter(lambda x: x['d2n'] < D2N_THRESHOLD, data)

    # Take a cut
    cut = itertools.islice(filtered, 3)
    """
    with open('render/output/filtered_freq_by_pixel_count.html', 'w') as out:
        out.write(template.render(
            data=filtered
        ))
    """
    filtered_rgb_colors = list(map(lambda x: list(x['rgb']), cut))
    matches = search_colors(filtered_rgb_colors)
    print(matches)
