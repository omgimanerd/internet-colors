#!/usr/bin/env python3

from collections import defaultdict

from util import iter_colors, rgb_to_hex

import json
import sys

def search_color(color_match):
    """
    Searches for a given RGB color in the data file and returns a dictionary
    of containing the websites that have that color and the frequency of
    color. color_match must be of the form [red, green, blue]
    """
    matches = {}
    def cb(url, colors):
        for entry in colors:
            if entry[1] == color_match:
                matches[url] = entry[0]
    iter_colors(cb)
    return matches

def search_colors(colors_match):
    """
    Seaches for a list of RGB colors in the data file and returns a dictionary
    containing the searched colors and the websites with those colors and the
    frequencies of each color per website. colors_match must be of the form
    [[red, green, blue], ... , [red, green, blue]]
    """
    matches = defaultdict(list)
    def cb(url, colors):
        for entry in colors:
            if entry[1] in colors_match:
                matches[tuple(entry[1])].append([url, entry[0]])
    iter_colors(cb)
    return dict(matches)

def main():
    if len(sys.argv) != 4:
        print('Usage: python search_color.py <r> <g> <b>')
        return 1
    color = list(map(int, sys.argv[1:4]))
    print('Searching for {} - {}'.format(color, rgb_to_hex(color)))
    for url, count in search_color(color).items():
        print(url, count)
    return 0

if __name__ == '__main__':
    main()
