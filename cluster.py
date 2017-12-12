'''
Clustering.py
-----------------------
Input: Cluster Class receives a matrix of word frequency counts that have been
normalized by TFIDF (term frequency–inverse document frequency). The algorithm
uses the sklearn package for the K-means clustering algorithm.
'''
from sklearn.cluster import KMeans
import numpy as np
from scipy import sparse
from scipy.sparse import csr_matrix
import pickle
import time
import util
import os

'''
num_clusters: number of clusters
freq_matrix: tfidf matrix of the word frequency in the data set
feature_matrix: loads in the remaining feature matrix
assignments,centroids,kmeans: parameters related to the clustering library

Read in a new input and add it to the current
history of what has been clustered, calls on sklearn package
and can return the cluster assignment for a queuery point
'''

class Cluster(object):
    def __init__(self, freq_data=util.FREQ_DATA, features_data=util.FEAT_DATA, num_clusters=util.NUM_CLUSTERS):
        self.num_clusters = num_clusters
        print('...Initializing Cluster...')
        compressed_freq = util.load_features(freq_data)
        compressed_feature = util.load_features(features_data)
        self.freq_matrix = compressed_freq
        self.feature_matrix = compressed_feature

        self.assignments = None
        self.centroids = None
        self.kmeans = None
        self.pickle_filename = util.PICKLE_NAME + str(self.num_clusters) + '.sav'

    # Freq_Matrix is a matrix containing the normalized frequencies of the
    # words in the wine reviews; each row represents one wine review
    def cluster_data(self):
        if os.path.isfile(self.pickle_filename):
            self.kmeans = pickle.load(open(self.pickle_filename, 'rb'))
            self.assignments = self.kmeans.labels_
            self.centroids = self.kmeans.cluster_centers_
            return
        try:
            print('...Clustering...')
            start_time = time.time()
            self.kmeans = KMeans(n_clusters = util.NUM_CLUSTERS).fit(self.freq_matrix)
            self.assignments = self.kmeans.labels_
            self.centroids = self.kmeans.cluster_centers_
            print('Clustering finished in: ', (time.time() - start_time))
        except:
            print ("Data read-in error!")
        pickle.dump(self.kmeans,open(self.pickle_filename,'wb'))

    # labels represents index of the cluster that each sample belongs to
    def get_assignments(self):
        return self.assignments

    # Coordinate position of the cluster
    def get_clusters(self):
        return self.centroids

    # Coordinate position of the cluster nearest to the data point passed in
    def cluster_assignment(self, data_file):
        new_data = np.load(data_file)
        return self.kmeans.predict(new_data)
