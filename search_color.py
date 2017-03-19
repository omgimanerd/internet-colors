#!/usr/bin/env python3

import json
import sys

def clamp(x):
    return max(0, min(x, 255))

def rgb_to_hex(rgb):
    return '#{0:02x}{1:02x}{2:02x}'.format(
        clamp(rgb[0]), clamp(rgb[1]), clamp(rgb[2]))

def get_colors(line):
    data = line.split('_')
    return data[0], json.loads(data[1])

def has_color(colors, match):
    for entry in colors:
        if entry[1] == match:
            return True

if __name__ == '__main__':
    try:
        color = list(map(int, sys.argv[1:4]))
    except:
        print('Usage: python search_color.py <r> <g> <b>')
    print('Searching for {} - {}'.format(color, rgb_to_hex(color)))
    with open('data/colors.txt') as data:
        for line in data:
            url, colors = get_colors(line)
            if has_color(colors, color):
                print(url)
