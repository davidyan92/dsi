# Author: Joseph Nelson (DC)

import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn import datasets, linear_model, metrics
import matplotlib.pyplot as plt

# load the data
iris = datasets.load_iris()

# identify target and features
X, y = iris.data, iris.target

# Standardize X
X = StandardScaler().fit_transform(X)

# Explore our data to look or potential clusters - see any?
plt.scatter(X[:,0], X[:,1])

plt.scatter(X[:,1], X[:,2])

plt.scatter(X[:,2], X[:,3])

# setup DBSCAN
dbscn = DBSCAN(eps = .5, min_samples = 5).fit(X)

# set labels
labels = dbscn.labels_
print(labels) # comprehension: what do these mean? How many are there?

# identify core samples
core_samples = np.zeros_like(labels, dtype = bool)
core_samples[dbscn.core_sample_indices_] = True
print(core_samples)


# declare number of clusters
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

# Now, we can use a handy chunk of code from the Scitkit documentation to measure the performance of our model
print('Estimated number of clusters: %d' % n_clusters_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(y, labels))
print("Completeness: %0.3f" % metrics.completeness_score(y, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(y, labels))
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, labels))

# homogeneity: each cluster contains only members of a single class.
# completeness: all members of a given class are assigned to the same cluster.
# The V-measure is the harmonic mean between homogeneity and completeness:
# Silhouette Coefficient - The best value is 1 and the worst value is -1. Values near 0 indicate overlapping clusters. Negative values generally indicate that a sample has been assigned to the wrong cluster, as a different cluster is more similar.

# plot our clusters
unique_labels = np.unique(labels)
colors = plt.cm.Spectral(np.linspace(0,1, len(unique_labels)))

for (label, color) in zip(unique_labels, colors):
    class_member_mask = (labels == label)
    n = X[class_member_mask & core_samples]
    plt.plot(n[:,0],n[:,1], 'o', markerfacecolor = color, markersize = 10)

    n = X[class_member_mask & ~core_samples]
    plt.plot(n[:,0],n[:,1], 'o', markerfacecolor = color, markersize = 5)
