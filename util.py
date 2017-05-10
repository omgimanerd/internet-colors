#!/usr/bin/env python3
# Helper functions for color and file manipulations
# Author: Alvin Lin (alvin@omgimanerd.tech)

from multiprocessing import JoinableQueue, Process

import colorsys
import json

NUM_THREADS = 8

def chunk(a, n):
    """
    Given a list and an integer n, this splits the list in n evenly sized
    chunks.
    """
    k, m = divmod(len(a), n)
    return list(a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)]
                for i in range(n))

def get_color_distance(rgb1, rgb2):
    """
    Given two RGB color values, this returns the squared euclidean distance
    between the two colors.
    """
    assert len(rgb1) == 3 and len(rgb2) == 3
    return sum([(rgb1[i] - rgb2[i]) ** 2 for i in range(3)])

def get_foreground_color(rgb):
    """
    Given an RGB color value as a background color, this calculates its
    perceived luminance and returns either black or white as a foreground
    color (as a hex code).
    """
    assert len(rgb) == 3
    p_lum = 1 - (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255
    if p_lum < 0.5:
        return "#000000"
    return "#FFFFFF"

def map_colors(fn):
    """
    Given a callback function, this will run the callback function on
    each entry in the colors data file.
    """
    queue = JoinableQueue()
    def thread_fn(queue):
        while True:
            line = queue.get()
            if line is None:
                queue.task_done()
                break
            data = line.split('_')
            fn(data[0], json.loads(data[1]))
            queue.task_done()
    processes = [
        Process(target=thread_fn, args=(queue,))
        for i in range(NUM_THREADS)
    ]
    [p.start() for p in processes]
    with open('data/colors.txt') as f:
        for line in f:
            queue.put(line)
    [queue.put(None) for i in range(NUM_THREADS)]
    queue.join()

def norm_rgb(rgb):
    """
    Given an RGB color value, this returns the same RGB color value with the
    colors scaled from 0-255 to 0-1.
    """
    assert len(rgb) == 3
    return [v / 255 for v in rgb]

def rgb_to_hex(rgb):
    """
    Given an RGB color value, this returns the hex code corresponding to the
    color value. Assumes the color values in rgb are from 0 to 255.
    """
    assert len(rgb) == 3
    return '#{0:02x}{1:02x}{2:02x}'.format(*rgb)

def rgb_to_hsv(rgb):
    """
    Given an RGB color value, this returns the color value converted to HSV.
    Assumes the color values in rgb are from 0 to 255.
    """
    assert len(rgb) == 3
    return colorsys.rgb_to_hsv(*norm_rgb(rgb))

if __name__ == '__main__':
    print(norm_rgb([255, 230, 45]))
    print(rgb_to_hsv([255, 230, 22]))
    from search_color import search_colors
    print(search_colors([[224, 191, 154], [24, 35, 97]]))
