#!/usr/bin/env python3
# Kmeans clustering algorithm heavily influenced by
# https://gist.github.com/iandanforth/5862470

import numpy as np

def _get_centroid(colors, weights):
    return (colors * weights).sum(axis=0) / weights.sum()

def _get_index_closest(p, centroids):
    """
    Given a point p and list of centroids, this function returns the index
    of the centroid in the list that p is closest to.
    """
    return np.argmin(((centroids - p) ** 2).sum(axis=1))

def kmeans(k, colors, weights, cutoff):
    """
    Given a k value, a list of colors, a parallel list containing the weights
    of those colors, and a centroid shift cutoff value, this function will
    return k centroids
    """
    # Multiply the colors by their weights
    colors = np.array(colors)
    weights = np.array(weights).reshape(len(weights), 1)
    # Pick k random colors as starting centroids
    centroids = colors[np.random.randint(colors.shape[0], size=k),:]
    biggest_shift = cutoff + 1
    while biggest_shift > cutoff:
        # Calculate which centroid each color is closest to. This generates an
        # array of indices representing which centroid the point is closest to.
        # This array is parallel to the points array.
        closest = np.array([_get_index_closest(c, centroids) for c in colors])
        # Cluster the points by grouping them according to which centroid
        # they're closest to. We will also cluster the weights of the points
        # for recalculation of the centroid later.
        clusters = np.array([colors[closest == i] for i in range(k)])
        cluster_weights = np.array([weights[closest == i] for i in range(k)])
        # Recalculate the locations of the centroids.
        new_centroids = np.array([
            _get_centroid(c, w) for c, w in zip(clusters, cluster_weights)])
        # Calculate the amount that the new centroids shifted. When this amount
        # is lower than a specified threshold, then we stop the algorithm.
        biggest_shift = ((new_centroids - centroids) ** 2).sum(axis=0).min()
        centroids = new_centroids
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
    p, l = make_blobs(n_samples=20, centers=centers, cluster_std=10,
                      random_state=0)
    weights = np.ones(100)
    centroids, clusters = kmeans(3, list(p), weights, 1)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    cr, cg, cb = zip(*centroids)
    ax.scatter(cr, cg, cb, c='green', s=100)
    for cluster in clusters:
        r, g, b = zip(*cluster)
        ax.scatter(r, g, b, c='red', s=10)
    plt.show()
