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
import os

# data file assumed to be in .npy file format
def load_data(freq_data):
    return(sparse.load_npz(freq_data))

'''
The ClusterEM model stores the actual em model, as well as statistics
derived from the ClusterEM model API.
The model does not return to us the assignment probabilities for each data
point to one of the clusters. So we also create a method to fill in this list.
'''

class ClusterEM(object):
    def __init__(self):
        self.em = None
        self.data_matrix = None
        self.num_components = util.NUM_CLUSTERS
        self.means = None
        self.covariances = None
        self.weights = None
        self.pickle_filename = util.OUTPUT_MODEL_EM
        self.assignments = None

    def run_model(self,data=util.FREQ_DATA):
        self.data_matrix = load_data(data).toarray()
        if os.path.isfile(self.pickle_filename):
            self.em = pickle.load(open(self.pickle_filename, 'rb'))
            self.covariances = self.em.covariances_
            self.means = self.em.means_
            self.weights = self.em.weights_
            self.assignments = self.create_assignments()
            # self.assignments = np.load('em_assignments')
            return
        #data_matrix = data_matrix[0:100,:]
        print('...Running EM Model...')
        start_time = time.time()
        self.em = GaussianMixture(n_components=self.num_components,covariance_type='spherical').fit(self.data_matrix)
        try:
            self.covariances = self.em.covariances_
            self.means = self.em.means_
            self.weights = self.em.weights_
            print('Clustering finished in: ', (time.time() - start_time))
        except:
            print('Data read in error')
        #output_file = 'util.OUTPUT_MODEL_EM' + '_' + string(util.NUM_CLUSTERS)
        pickle.dump(self.em,open('em_model_12.sav','wb'))
        self.assignments = self.create_assignments()

    def get_means(self):
        return self.means

    def get_covariances(self):
        return self.covariances

    def get_weights(self):
        return self.weights

    def predict_probs(self,data_point):
        return self.em.predict_proba(data_point)

    def create_assignments(self):
        # print('...Creating Assignments for EM Model ...')
        # assuming that the data matrix has already been loaded in the run_model()
        # step
        if os.path.isfile('em_assignments.npy'):
            return np.load('em_assignments.npy')

        self.assignments = self.predict_probs(self.data_matrix)
        # --------- Temporary Code -------
        # Storing out matrix also so that we do not need to re-run algorithm
        np.save('em_assignments', self.assignments)
        return self.assignments

    def get_assignments(self):
        return self.create_assignments()
