import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.cm as cm
import matplotlib.colors as cl

from sklearn.neighbors import KNeighborsClassifier

from ipywidgets import *


class KNNBoundaryPlotter(object):

    def __init__(self, df, var1, var2, classvar,
                 nn_range=range(1,101),
                 granularity=50.,
                 buffer_denom=15.,
                 figsize=(9,7),
                 dotsize=70,
                 point_colors=sns.xkcd_palette(['windows blue', 'amber']),
                 mesh_colors=['#8FCCFF', '#FFED79']):

        self.df = df
        self.var1 = var1
        self.var2 = var2
        self.classvar = classvar
        self.nn_range = nn_range
        self.granularity = granularity
        self.buffer_denom = buffer_denom
        self.figsize = figsize
        self.dotsize = dotsize
        self.point_colors = point_colors
        self.mesh_colors = mesh_colors

    def knn_mesh_fitter(self):

        # get the minimum and maximum values for each of the predictor variables
        v1_min, v1_max = np.min(self.X[:,0]), np.max(self.X[:,0])
        v2_min, v2_max = np.min(self.X[:,1]), np.max(self.X[:,1])

        # get the range of each variable
        v1_range = v1_max - v1_min
        v2_range = v2_max - v2_min

        # set up the min and max ranges of the axes of the plot
        # I add a buffer here (1/15th of the range) so no points are on the axes
        self.x_min = v1_min - (v1_range/self.buffer_denom)
        self.x_max = v1_max + (v1_range/self.buffer_denom)

        self.y_min = v2_min - (v2_min/self.buffer_denom)
        self.y_max = v2_max + (v2_range/self.buffer_denom)

        # use the numpy meshgrid function to make a bunch of points across the range
        # of values.

        self.xx, self.yy = np.meshgrid(np.linspace(self.x_min, self.x_max,
                                                   self.granularity),
                                       np.linspace(self.y_min, self.y_max,
                                                   self.granularity))

        # meshgrids:
        self.Zs = {'uniform':{},
                   'distance':{}}

        for nn in self.nn_range:
            # fit a knn on the data with the nearest neighbors number passed into the function
            knn_mod_euc = KNeighborsClassifier(n_neighbors=nn, weights='uniform')
            knn_mod_euc.fit(self.X, self.y)

            knn_mod_w = KNeighborsClassifier(n_neighbors=nn, weights='distance')
            knn_mod_w.fit(self.X, self.y)

            # Predict using the knn model on all the meshgrid points. This will let us see
            # the knn boundary of where it predicts between one class and another!
            Z = knn_mod_euc.predict(np.c_[self.xx.ravel(), self.yy.ravel()])
            Z = Z.reshape(self.xx.shape)
            self.Zs['uniform'][nn] = Z

            Z = knn_mod_w.predict(np.c_[self.xx.ravel(), self.yy.ravel()])
            Z = Z.reshape(self.xx.shape)
            self.Zs['distance'][nn] = Z

        if len(np.unique(self.X[:,0]))+50 < self.X.shape[0]:
            self.v1_points = self.rand_jitter(self.X[:,0])
        else:
            self.v1_points = self.X[:,0]

        if len(np.unique(self.X[:,1]))+50 < self.X.shape[0]:
            self.v2_points = self.rand_jitter(self.X[:,1])
        else:
            self.v2_points = self.X[:,1]


    def knn_mesh_runner(self):

        # make X, y
        self.X = self.df[[self.var1, self.var2]].values
        self.y = self.df[self.classvar].values

        self.knn_mesh_fitter()

    def rand_jitter(self, array):
        stdev = .03*(np.max(array)-np.min(array))
        return array + np.random.randn(len(array)) * stdev

    # MOST OF THIS FUNCTION STUFF LIFTED FROM SCIKIT-LEARN EXAMPLE!
    # see:
    # http://scikit-learn.org/stable/auto_examples/neighbors/plot_classification.html#example-neighbors-plot-classification-py

    def knn_boundary_plotter(self, nn, weights):

        # the 'pcolormesh' matplotlib function requires we convert the mesh colors into a
        # 'colormap'
        colormap = ListedColormap(self.mesh_colors)

        # Predict using the knn model on all the meshgrid points. This will let us see
        # the knn boundary of where it predicts between one class and another!
        Z = self.Zs[weights][nn]

        point_colors = [self.point_colors[y_] for y_ in self.y]

        # Set the figure size to be big enough to see stuff
        plt.figure(figsize=self.figsize)

        # Plot the background colormesh colors, showing the decision boundary
        # of the fit k nearest neighbors algorithm:
        plt.pcolormesh(self.xx, self.yy, Z, cmap=colormap)

        # Plot the actual points of the 2 predictor variables
        plt.scatter(self.v1_points, self.v2_points, c=point_colors, s=self.dotsize)

        # set the axis limits:
        plt.xlim(self.x_min, self.x_max)
        plt.ylim(self.y_min, self.y_max)

        # Add the labels corresponding to the variables and a title
        # (I remembered this time, Sam!)
        plt.xlabel(self.var1, fontsize=20)
        plt.ylabel(self.var2, fontsize=20)
        plt.title('kNN='+str(nn)+', weights='+weights+' predicting '+self.classvar+ \
                  ' with '+self.var1+' & '+self.var2+'\n',
                  fontsize=20)


    def knn_area_symmetry_slider(self, nn=1, weights='uniform'):
        self.knn_boundary_plotter(nn, weights)


    def knn_interact(self):

        widgets.interact(self.knn_area_symmetry_slider,
                         nn=widgets.IntSlider(min=np.min(self.nn_range),
                                              max=np.max(self.nn_range),
                                              step=1, value=1),
                         weights=('uniform','distance'))
