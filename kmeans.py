#!/usr/bin/env python3
# Kmeans clustering algorithm heavily influenced by
# https://gist.github.com/iandanforth/5862470

from util import get_color_distance

import random

def get_centroid(colors, weights):
    for i, weight in enumerate(weights):
        colors[i] = [c * weight for c in colors[i]]
    rgb = zip(*colors)
    return [sum(v) / sum(weights) for v in rgb]

def get_closest_centroid_index(p, points):
    index = 0
    min_distance = get_color_distance(p, points[0])
    for i in range(1, len(points)):
        distance = get_color_distance(p, points[i])
        if distance < min_distance:
            min_distance = distance
            index = i
    return i

def kmeans(k, colors, weights, cutoff):
    centroids = random.sample(colors, k)
    while True:
        clusters = [[] for i in centroids]
        for color in colors:
            index = get_closest_centroid_index(color, centroids)
            clusters[index].append(color)
        biggest_shift = 0
        for i, cluster in enumerate(clusters):
            new_centroid = get_centroid(cluster)
            shift = get_color_distance(new_centroid, centroids[i])
            biggest_shift = max(shift, biggest_shift)
            centroids[i] = new_centroid
        if biggest_shift < cutoff:
            break
    return centroids, clusters
