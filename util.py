#!/usr/bin/env python3
# Helper functions for color and file manipulations
# Author: Alvin Lin (alvin@omgimanerd.tech)

import colorsys
import json

COLORS_FILE = 'data/colors.txt'

def chunk(l, n):
    """
    Given a list and an integer n, this splits the list in n evenly sized
    chunks.
    """
    return [l[i::n] for i in range(n)]

def get_color_distance(rgb1, rgb2):
    """
    Given two RGB color values, this returns the squared euclidean distance
    between the two colors.
    """
    return sum([(rgb1[i] + rgb2[i]) ** 2 for i in range(3)])

def get_foreground_color(rgb):
    """
    Given an RGB color value as a background color, this calculates its
    perceived luminance and returns either black or white as a foreground
    color (as a hex code).
    """
    p_lum = 1 - (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255
    if p_lum < 0.5:
        return "#000000"
    return "#FFFFFF"

def iter_colors(fn):
    """
    Given a callback function, this returns a list of the return values when
    the callback has been run on each entry in the colors data file.
    """
    def map_fn(line):
        data = line.split('_')
        return fn(data[0], json.loads(data[1]))
    with open(COLORS_FILE) as f:
        return list(map(map_fn, f))

def norm_rgb(rgb):
    """
    Given an RGB color value, this returns the same RGB color value with the
    colors scaled from 0-255 to 0-1.
    """
    return list(map(lambda x: x / 255, rgb))
    
def rgb_to_hex(rgb):
    """
    Given an RGB color value, this returns the hex code corresponding to the
    color value. Assumes the color values in rgb are from 0 to 255.
    """
    return '#{0:02x}{1:02x}{2:02x}'.format(*rgb)

def rgb_to_hsv(rgb):
    """
    Given an RGB color value, this returns the color value converted to HSV.
    Assumes the color values in rgb are from 0 to 255.
    """
    return colorsys.rgb_to_hsv(*list(map(lambda x: x / 255, rgb)))

if __name__ == '__main__':
    c = [0, 13, 57]
    d = [1, 13, 58]
    print(rgb_to_hex(c))
    print(rgb_to_hsv(d))
    print(get_color_distance(c, d))
    d = []
    def p(url, colors):
        d.append(url)
    iter_colors(p)
    print(d)
