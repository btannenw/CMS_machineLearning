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
    return a 3-d array with (x,y,0) where 0 is the label for the data: 0 = normal
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
        pts.append([x,y,0])
    # r, x, y = create_test_data(3, [1, 1], 0.3, 500)
    # plt.plot(x_pts, y_pts, 'ro', markersize=5)
    # plt.plot(x, y, 'bo', markersize=5)
    # plt.show()
    pts = np.asarray(pts)
    return pts


def create_test_data(seed, mean,std, n):
    '''
    create n number of random 2-d gaussian points with a covariance of std with a mean of mean
    return a 3-d array with (x,y,1) where 1 is the label for the data: 1 = anomalous
    '''
    cov = [[std,0],[0,std]]
    numpy.random.seed(seed)
    x, y = numpy.random.multivariate_normal(mean, cov, n).T
    # return np.column_stack((x,y)), x, y
    pts = np.column_stack((x,y))
    labels = np.ones((n, 1))
    pts = np.column_stack((pts, labels))
    return pts




