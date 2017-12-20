import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from ipywidgets import *


class GradientDescentPlotter(object):

    def __init__(self, x=None, y=None, beta0=0.01, beta1=0.01,
                 step_size=0.000005, figsize=(18,7)):

        if (x == None) and (y == None):
            self.x = np.arange(1,51,1)+np.random.normal(0,0.3,size=50)
            self.y = (self.x * np.random.normal(0,1)) + \
            np.random.normal(0,3,size=50) + np.random.normal(0,20)
        elif x == None:
            self.y = y
            self.x = y+np.random.normal(0,np.std(y)/2.,size=len(y))
        elif y == None:
            self.x = x
            self.y = x+np.random.normal(0,np.std(x)/2.,size=len(x))

        self.x = (self.x - np.mean(self.x)) / np.std(self.x)

        self.N = len(self.x)

        self.figsize = figsize

        self.beta0 = beta0
        self.beta1 = beta1
        self.beta0s = [self.beta0]
        self.beta1s = [self.beta1]

        self.step_size = step_size

        self.colors = dict(blue='#1F77B4',
                           orange='#FF7F0E',
                           green='#2CA02C',
                           red='#D62728',
                           purple='#9467BD',
                           brown='#8C564B',
                           pink='#E377C2',
                           grey='#7F7F7F',
                           yellow='#BCBD22',
                           teal='#17BECF')


    def mean_squared_error(self):
        y_pred = self.beta0 + (self.x * self.beta1)
        mean_sq_err = np.mean((self.y - y_pred)**2)
        return mean_sq_err


    def _beta0_gradient_update(self, i):

        # add to the beta0 gradient for each x,y using the
        # partial derivative with respect to beta0
        return -(2./self.N) * (self.y[i] - ((self.beta1 * self.x[i]) + self.beta0))


    def _beta1_gradient_update(self, i):

        # add to the beta1 gradient for each x,y using the
        # partial derivative with respect to beta1
        return -(2./self.N) * self.x[i] * (self.y[i] - ((self.beta1 * self.x[i]) + self.beta0))


    def run_gradient_descent(self, iterations=500):

        self.iterations = iterations

        self.mses = []
        self.mses.append(self.mean_squared_error())

        self.X = np.array([np.ones(self.N), self.x]).T
        theta = np.array([self.beta0, self.beta1])
        Xt = self.X.transpose()

        for i in range(self.iterations):
            y_hat = np.dot(self.X, theta)
            loss = y_hat - self.y
            J = np.sum(loss ** 2) / (2 * self.N)  # cost
            gradient = np.dot(Xt, loss) / self.N
            theta = theta - self.step_size * gradient  # update
            mse = mean_squared_error(self.y, y_hat)
            self.mses.append(mse)
            self.beta0s.append(theta[0])
            self.beta1s.append(theta[1])


        lr = LinearRegression().fit(self.x[:, np.newaxis], self.y)
        self.optimal_b0 = lr.intercept_
        self.optimal_b1 = lr.coef_[0]
        self.optimal_mse = mean_squared_error(self.y,
                                              lr.predict(self.x[:, np.newaxis]))


    def gradient_descent_plotter(self, i):

        fig, axarr = plt.subplots(1, 3, figsize=self.figsize,
                                  sharex=False, sharey=False)

        ax1 = axarr[0]

        ax1.scatter(self.x, self.y, color=self.colors['blue'],
                    alpha=0.7, s=70)

        y_pred = self.beta0s[i] + (self.x * self.beta1s[i])

        ax1.plot(self.x, y_pred, lw=3.5, color=self.colors['red'],
                 label='MSE = %0.2f' % self.mses[i])

        ax1.set_title('gradient descent regression line', fontsize=20)
        ax1.set_ylabel('y', fontsize=16)
        ax1.set_xlabel('x', fontsize=16)
        ax1.legend(loc='lower right', fontsize=16)

        iters= range(1, i+1)

        ax2 = axarr[1]

        if len(iters) > 0:
            ax2.scatter(self.beta0s[:i], self.beta1s[:i], s=70, alpha=0.025,
                     color=self.colors['grey'])
        ax2.scatter(self.beta0s[i], self.beta1s[i],
                    s=120, color=self.colors['purple'],
                    label='betas path')
        ax2.scatter(self.optimal_b0, self.optimal_b1,
                    s=120, color=self.colors['green'],
                    label='optimal betas')


        ax2.set_title('beta0, beta1 across iterations', fontsize=16)
        ax2.set_xlabel('beta0', fontsize=16)
        ax2.set_ylabel('beta1', fontsize=16)
        ax2.legend(loc='lower right', fontsize=16)

        ax3 = axarr[2]

        if len(iters) > 0:
            ax3.plot(iters, self.mses[:i], lw=4, color=self.colors['yellow'],
                     label='MSE')
        ax3.axhline(self.optimal_mse, lw=4, color=self.colors['green'],
                    label='Optimal MSE', alpha=0.6, ls='dashed')


        ax3.set_title('MSE by iteration', fontsize=20)
        ax3.set_xlabel('iteration', fontsize=16)
        ax3.set_ylabel('MSE', fontsize=16)
        ax3.legend(loc='lower right', fontsize=16)

        ax3.set_xlim([0, self.iterations+1])

        plt.tight_layout()
        plt.show()


    def gradient_slider(self, iteration=0):
        self.gradient_descent_plotter(iteration)


    def gradient_interact(self):

        iw = widgets.IntSlider(min=0, max=self.iterations, step=1, value=0)
        iw.width = '600px'
        iw.description = 'Iteration:'

        widgets.interact(self.gradient_slider,
                         iteration=iw)
