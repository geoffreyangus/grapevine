'''
Code to cluster data using the EM model.
'''

import numpy as np
from sklearn.mixture import GaussianMixture
import json
import util
import pickle
import time

class ClusterEM(object):
    def __init__(self):
        self.em = None
        self.num_components = util.NUM_CLUSTERS
        self.means = None
        self.covariances = None
        self.weights = None

    def run_model(self,data):
        try:
            print('...Running EM Model ...')
            start_time = time.time()
            self.em = GaussianMixture(n_components = self.num_components).fit(data)
            self.covariances = self.em.covariances_
            self.means = self.em.means_
            self.weights = self.em.weights_
            print('Clustering finished in: ', (time.time() - start_time))
        except:
            print('Data read in error')
        pickle.dump(self.kmeans,open(util.OUTPUT_MODEL_EM,'wb'))

    def get_means(self):
        return self.means

    def get_covariances(self):
        return self.covariances

    def get_weights(self):
        return self.weights

    def predict_probs(self,data_point):
        return self.em.predict_proba()
