import matplotlib.pyplot as plt
import math
import random
import numpy.random
import numpy as np

'''
sources: https://blogs.sas.com/content/iml/2016/03/30/generate-uniform-2d-ball.html

'''

def create_train_data(seed, radius, n):
    '''
    create n number of uniformly random data points in a circle of given radius
    '''
    x_pts = []
    y_pts = []
    pts = []
    numpy.random.seed(seed)
    for i in range(0, n):
        theta = 2 * math.pi * numpy.random.uniform(0, 1, 1)
        r = radius * math.sqrt(numpy.random.uniform(0, 1, 1))
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        x_pts.append(x)
        y_pts.append(y)
        pts.append([x,y])
    x_pts = np.asarray(x_pts)
    y_pts = np.asarray(y_pts)
    pts = np.asarray(pts)
    return pts


def create_test_data(seed, mean,std, n):
    '''
    create n number of random 2-d gaussian points with a covariance of std with a mean of mean
    '''
    cov = [[std,0],[0,std]]
    numpy.random.seed(seed)
    x, y = numpy.random.multivariate_normal(mean, cov, n).T
    return np.column_stack((x,y))


def draw_plots(xtrain, ytrain, xtest, ytest):
    '''
    draw the data points created by create_test_data and create_train_data
    '''
    plt.plot(xtrain, ytrain, 'ro', markersize=5)
    plt.plot(xtest, ytest, 'bo', markersize=5)
    plt.show()


