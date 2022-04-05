#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import xgboost as xgb
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn import metrics
import time
np.random.seed(0)

def run_kmean(df, batch_size=15, n_clusters=3):

    # #############################################################################
    # Compute clustering with Means
    k_means = KMeans(init='k-means++', n_clusters=n_clusters, n_init=10)
    t0 = time.time()
    k_means.fit(df)
    t_batch = time.time() - t0

    # #############################################################################
    # Compute clustering with MiniBatchKMeans
    mbk = MiniBatchKMeans(init='k-means++', n_clusters=n_clusters, batch_size=batch_size,
                      n_init=10, max_no_improvement=10, verbose=0)
    t0 = time.time()
    mbk.fit(df)
    t_mini_batch = time.time() - t0

    # #############################################################################
    X = df.values
    fig = plt.figure(figsize=(20, 5))
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)

    colors = ['grey', 'yellow', 'red']
    # We want to have the same colors for the same cluster from the
    # MiniBatchKMeans and the KMeans algorithm. Let's pair the cluster centers per
    # closest one.
    k_means_cluster_centers = k_means.cluster_centers_
    order = pairwise_distances_argmin(k_means.cluster_centers_, mbk.cluster_centers_)
    mbk_means_cluster_centers = mbk.cluster_centers_[order]

    k_means_labels = pairwise_distances_argmin(X, k_means_cluster_centers)
    mbk_means_labels = pairwise_distances_argmin(X, mbk_means_cluster_centers)

    # KMeans
    ax = fig.add_subplot(1, 3, 1)
    for k, col in zip(range(n_clusters), colors):
        my_members = k_means_labels == k
        cluster_center = k_means_cluster_centers[k]
        ax.plot(X[my_members, 0], X[my_members, 1], 'w',markerfacecolor=col, marker='.', markersize=20)
        ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,markeredgecolor='k', markersize=20)
        ax.set_title('KMeans')
        ax.set_xticks(())
        ax.set_yticks(())
        plt.text(-3.5, 1.8,  'train time: %.2fs\ninertia: %f' % (t_batch, k_means.inertia_))

    # MiniBatchKMeans
    ax = fig.add_subplot(1, 3, 2)
    for k, col in zip(range(n_clusters), colors):
        my_members = mbk_means_labels == k
        cluster_center = mbk_means_cluster_centers[k]
        ax.plot(X[my_members, 0], X[my_members, 1], 'w',markerfacecolor=col, marker='.', markersize=20)
        ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
            markeredgecolor='k', markersize=20)
    ax.set_title('MiniBatchKMeans')
    ax.set_xticks(())
    ax.set_yticks(())
    plt.text(-3.5, 1.8, 'train time: %.2fs\ninertia: %f' %(t_mini_batch, mbk.inertia_))


    # Initialise the different array to all False
    different = (mbk_means_labels == 4)
    ax = fig.add_subplot(1, 3, 3)

    for k in range(n_clusters):
        different += ((k_means_labels == k) != (mbk_means_labels == k))

    identic = np.logical_not(different)
    ax.plot(X[identic, 0], X[identic, 1], 'w',markerfacecolor='#bbbbbb', marker='.', markersize=20)
    ax.plot(X[different, 0], X[different, 1], 'w',
        markerfacecolor='m', marker='.', markersize=20)
    ax.set_title('Difference')
    ax.set_xticks(())
    ax.set_yticks(())

    #plt.show()

    scr_kmean, scr_mini_kmean, k_means_class, k_mbk_class = get_cluster(df, n_clusters, batch_size)

    return scr_kmean, scr_mini_kmean, k_means_class, k_mbk_class

def get_cluster(X, n_clusters, batch_size):
    # #############################################################################
    # Compute clustering with Means
    k_means = KMeans(init='k-means++', n_clusters=n_clusters, n_init=10)
    t0 = time.time()
    k_means.fit(X)
    k_means_class=k_means.predict(X)
    t_batch = time.time() - t0
    
    labels = k_means.labels_
    score_kmean = metrics.silhouette_score(X, labels, metric='euclidean')

    # #############################################################################
    # Compute clustering with MiniBatchKMeans

    mbk = MiniBatchKMeans(init='k-means++', n_clusters=n_clusters, batch_size=batch_size,
                      n_init=10, max_no_improvement=10, verbose=0)
    t0 = time.time()
    mbk.fit(X)
    k_mbk_class=mbk.predict(X)
    t_mini_batch = time.time() - t0
    
    labels = mbk.labels_
    score_mini_kmean = metrics.silhouette_score(X, labels, metric='euclidean')
    
    return score_kmean, score_mini_kmean, k_means_class, k_mbk_class
