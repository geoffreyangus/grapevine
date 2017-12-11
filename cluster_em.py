'''
Code to cluster data using the EM model.
'''

import numpy as np
from sklearn.mixture import GaussianMixture
import json
import util

class ClusterEM(object):
    def __init__(self):
        self.em = None
        self.num_components = util.NUM_CLUSTERS
        self.means = None
        self.covariances = None
        self.weights = None

    def run_model(data):
        self.em = GaussianMixture(n_components = self.num_components).fit(data)
        self.covariances = self.em.covariances_
        self.means = self.em.means_
        self.weights = self.em.weights_

        
