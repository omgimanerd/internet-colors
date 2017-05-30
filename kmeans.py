#!/usr/bin/env python3
# Kmeans clustering algorithm heavily influenced by
# https://gist.github.com/iandanforth/5862470

import numpy as np

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
    colors = np.array(colors) * np.array(weights).reshape(len(weights), 1)
    # Pick k random colors as starting centroids
    centroids = colors[np.random.randint(colors.shape[0], size=k),:]
    biggest_shift = cutoff + 1
    while biggest_shift > cutoff:
        # Calculate which centroid each color is closest to. This generates an
        # array of indices representing which centroid the point is closest to.
        # This array is parallel to the points array.
        closest = np.array([_get_index_closest(c, centroids) for c in colors])
        # Get the new centroids by calculating the centroid of the point cluster
        # for each centroid.
        clusters = np.array([colors[closest == i] for i in range(k)])
        new_centroids = np.array([cluster.mean(axis=0) for cluster in clusters])
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
    p, l = make_blobs(n_samples=100, centers=centers, cluster_std=5,
                      random_state=0)
    centroids, clusters = kmeans(3, list(p), np.ones(100), 2)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    r, g, b = zip(*p)
    cr, cg, cb = zip(*centroids)
    ax.scatter(r, g, b, c='red')
    ax.scatter(cr, cg, cb, c='green', s=100)
    plt.show()
