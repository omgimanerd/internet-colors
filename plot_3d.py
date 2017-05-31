#!/usr/bin/env python3

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

from util import norm_rgb
from kmeans import *

import matplotlib.pyplot as plt
import numpy as np

import pickle

FREQ_BY_PIXEL_COUNT_PKL = 'data/freq_by_pixel_count.pkl'
FREQUENCY_THRESHOLD = 20000
MAX_POINT_SIZE = 200

def clamp(x, low, high):
    return max(min(x, high), low)

def get_data():
    with open(FREQ_BY_PIXEL_COUNT_PKL, 'rb') as f:
        data = pickle.load(f)
        colors, frequencies = [], []
        for key in data:
            if data[key] > FREQUENCY_THRESHOLD:
                colors.append(key)
                frequencies.append(data[key])
    return colors, frequencies

def plot_color_frequencies(colors, frequencies):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    r, g, b = zip(*colors)
    m = sorted(frequencies)[-10]
    sizes = list(map(lambda x: clamp(x / m, 0.05, 1) * MAX_POINT_SIZE, frequencies))
    ax.scatter(r, g, b, c=[norm_rgb(color) for color in colors], s=sizes)
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
    return fig, ax

def plot_color_clusters(colors, frequencies):
    centroids, clusters = kmeans(3, colors, frequencies, 0.5)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    r, g, b = zip(*centroids)
    colors = [norm_rgb(color) for color in centroids]
    ax.scatter(r, g, b, c=colors)
    # for cluster in clusters:
    #     r, g, b = zip(*cluster)
    #     ax.scatter(r, g, b, c=colors)
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
    return fig, ax

if __name__ == '__main__':
    colors, frequencies = get_data()
    fig, ax = plot_color_clusters(colors, frequencies)
    plt.show()
    # ax.view_init(30, 0)
    # def update(i):
    #     ax.view_init(30, i)
    # anim = FuncAnimation(fig, update, frames=np.arange(0, 360), interval=5)
    # anim.save('plot_3d_clusters.gif', dpi=80, writer='imagemagick')
    # fig, ax = plot_color_frequencies(colors, frequencies)
    # ax.view_init(30, 0)
    # def update(i):
    #     ax.view_init(30, i)
    # anim = FuncAnimation(fig, update, frames=np.arange(0, 360), interval=5)
    # anim.save('output/plot_3d.gif', dpi=80, writer='imagemagick')
