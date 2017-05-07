#!/usr/bin/env python3
# Kmeans clustering algorithm heavily influenced by
# https://gist.github.com/iandanforth/5862470

from util import get_color_distance

import random

def get_centroid(colors, weights):
    """
    Given a list of colors and a parallel list of weights, this function
    returns the centroid of the points.
    """
    for i, weight in enumerate(weights):
        colors[i] = [c * weight for c in colors[i]]
    rgb = zip(*colors)
    wsum = sum(weights)
    return [sum(v) / wsum for v in rgb]

def get_closest_centroid_index(p, centroids):
    """
    Given a point p and list of centroids, this function returns the index
    of the centroid in the list that p is closest to.
    """
    index = 0
    min_distance = get_color_distance(p, centroids[0])
    for i in range(1, len(centroids)):
        distance = get_color_distance(p, centroids[i])
        if distance < min_distance:
            min_distance = distance
            index = i
    return index

def kmeans(k, colors, weights, cutoff):
    """
    Given a k value, a list of colors, a parallel containing the weights
    of those colors, and a centroid shift cutoff value, this function will
    return k centroids
    """
    centroids = random.sample(colors, k)
    biggest_shift = cutoff + 1
    j = 0
    while biggest_shift > cutoff:
        clusters = [[] for i in centroids]
        cluster_weights = [[] for i in centroids]
        shifts = [[] for i in centroids]
        for color, weight in zip(colors, weights):
            index = get_closest_centroid_index(color, centroids)
            clusters[index].append(color)
            cluster_weights[index].append(weight)
        for i, cluster in enumerate(clusters):
            new_centroid = centroids[i]
            if len(cluster) > 0:
                new_centroid = get_centroid(cluster, cluster_weights[i])
            shifts[i] = get_color_distance(new_centroid, centroids[i])
            centroids[i] = new_centroid
        biggest_shift = max(shifts)
    return centroids, clusters

if __name__ == '__main__':
    """
    Generating some randomly distributed clusters to test the algorithm
    $ python kmeans.py
    to test, must have scipy and sklearn installed.
    """
    from mpl_toolkits.mplot3d import Axes3D
    from sklearn.datasets.samples_generator import make_blobs
    import matplotlib.pyplot as plt

    centers = [[25, 25, 25], [100, 100, 100], [2, 57, 20]]
    p, l = make_blobs(n_samples=100, centers=centers, cluster_std=5, random_state=0)
    w = [1 for i in range(100)]
    centroids, clusters = kmeans(3, list(p), w, 2)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    r, g, b = zip(*p)
    cr, cg, cb = zip(*centroids)
    ax.scatter(r, g, b, c='red')
    ax.scatter(cr, cg, cb, c='green', s=100)
    plt.show()
