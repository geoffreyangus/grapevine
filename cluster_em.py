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

        self.assignments = None

    def run_model(self,data=util.FREQ_DATA):
        self.data_matrix = load_data(data).toarray()
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

    def create_assignments(self,data=util.FREQ_DATA):
        print('...Creating Assignments for EM Model ...')
        # assuming that the data matrix has already been loaded in the run_model()
        # step
        self.assignments = np.zeros(self.data_matrix.shape)
        for i in range(self.data_matrix.shape[0]):
            self.assignments[i,:] = self.predict_probs(self.data_matrix[i,:])

        # --------- Temporary Code -------
        # Storing out matrix also so that we do not need to re-run algorithm
        sparse.save_npz('em_assignments.npz',self.assignments)
