#!/usr/bin/env python3

from mpl_toolkits.mplot3d import Axes3D

from util import norm_rgb

import matplotlib.pyplot as plt
import numpy as np

import pickle

FREQ_BY_PIXEL_COUNT_PKL = 'freq_by_pixel_count.pkl'
MAX_POINT_SIZE = 100

def get_data():
    with open(FREQ_BY_PIXEL_COUNT_PKL, 'rb') as f:
        data = pickle.load(f)
    return zip(*data.items())

def plot(colors, frequencies):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    r, g, b = zip(*colors)
    m = max(frequencies)
    sizes = list(map(lambda x: (x / m) * MAX_POINT_SIZE, frequencies))
    colors = list(map(norm_rgb, colors))
    ax.scatter(r, g, b, c=colors, s=sizes)
    ax.set_xlabel('R')
    ax.xaxis.label.set_color('red')
    ax.set_ylabel('G')
    ax.yaxis.label.set_color('green')
    ax.set_zlabel('B')
    ax.zaxis.label.set_color('blue')
    ax.set_xlim(0, 256)
    ax.set_xticks(range(0, 257, 32))
    ax.tick_params(axis='x', colors='red')
    ax.set_ylim(0, 256)
    ax.set_yticks(range(0, 257, 32))
    ax.tick_params(axis='y', colors='green')
    ax.set_zlim(0, 256)
    ax.set_zticks(range(0, 257, 32))
    ax.tick_params(axis='z', colors='blue')
    plt.show()

if __name__ == '__main__':
    plot([(16, 140, 57), (28, 45, 199)], [10, 40])
