'''
Clustering.py
-----------------------
Input: Cluster Class receives a matrix of word frequency counts that have been
normalized by TSIDF (term frequency–inverse document frequency). The algorithm
uses the sklearn package for the K-means clustering algorithm.
'''
from sklearn.cluster import KMeans
import numpy as np

NUM_CLUSTERS = 20 # number of clusters
DATA_FILE = 'frequency_matrix.npy' # file that contains the matrix

# Read in a new input and add it to the current
# history of what has been clustered, calls on sklearn package
# and can return the cluster assignment for a queuery point

class Cluster(object):
    def __init__(self):
        self.num_clusters = NUM_CLUSTERS
        self.freq_matrix = None
        self.assignments = None
        self.centroids = None
        self.kmeans = None

    # data file assumed to be in .npy file format
    def load_data(self,data_file = DATA_FILE):
        self.freq_matrix = np.load(data_file)

    # Freq_Matrix is a matrix containing the normalized frequencies of the
    # words in the wine reviews; each row represents one wine review
    def cluster_data(self):
        try:
            self.kmeans = KMEANS(n_clusters = NUM_CLUSTERS,random_state=0).fit(self.freq_matrix)
            self.assignments = self.kmeans.labels_
            self.centroids = self.kmeans.cluster_centers_
        except:
            print ("Data read-in error!")

    # labels represents index of the cluster that each sample belongs to
    def get_assignments(self):
        return self.assignments

    # Coordinate position of the cluster
    def get_clusters(self):
        return self.centroids

    # Coordinate position of the cluster nearest to the data point passed in
    def cluster_assignment(self,data_file):
        new_data = np.load(data_file)
        return self.kmeans.predict(new_data)
