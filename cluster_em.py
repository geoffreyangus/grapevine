'''
Code to cluster data using the EM model.
'''

import numpy as np
from sklearn.mixture import GaussianMixture
from scipy import sparse
from scipy.sparse import csr_matrix
import json
import util
import pickle
import time

# data file assumed to be in .npy file format
def load_data(freq_data):
    return(sparse.load_npz(freq_data))

class ClusterEM(object):
    def __init__(self):
        self.em = None
        self.num_components = util.NUM_CLUSTERS
        self.means = None
        self.covariances = None
        self.weights = None

    def run_model(self,data=util.FREQ_DATA):
        data_matrix = load_data(data).toarray()
        #data_matrix = data_matrix[0:100,:]
        print('...Running EM Model...')
        start_time = time.time()
        self.em = GaussianMixture(n_components=self.num_components,covariance_type='spherical').fit(data_matrix)
        try:
            self.covariances = self.em.covariances_
            self.means = self.em.means_
            self.weights = self.em.weights_
            print('Clustering finished in: ', (time.time() - start_time))
        except:
            print('Data read in error')
        output_file = 'util.OUTPUT_MODEL_EM' + '_' + util.NUM_CLUSTERS
        pickle.dump(self.em,open(output_file,'wb'))

    def get_means(self):
        return self.means

    def get_covariances(self):
        return self.covariances

    def get_weights(self):
        return self.weights

    def predict_probs(self,data_point):
        return self.em.predict_proba()
