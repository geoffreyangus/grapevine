'''
Clustering.py
-----------------------
Input: Cluster Class receives a matrix of word frequency counts that have been
normalized by TSIDF (term frequency–inverse document frequency). The algorithm
uses the sklearn package for the K-means clustering algorithm.
'''
from sklearn.cluster import KMeans
import numpy as np
from tempfile import TemporaryFile

NUM_CLUSTERS = 20

# Read in a new input and add it to the current
# history of what has been clustered, should be able to recluster
# and should be able to print out new recommendations for the
wine types

class Cluster(object):
    def __init__(self):
        self.num_clusters = NUM_CLUSTERS
        self.freq_matrix = None
        self.labels = None

    def load_data(self,data_file):
        self.freq_matrix = np.load(data_file)

    def create_clusters(self):
        # Freq_Matrix is a matrix containing the normalized frequencies of the
        # words in the wine reviews; each row represents one wine review
        try:
            kmeans = KMEANS(n_clusters = NUM_CLUSTERS,random_state=0).fit(self.freq_matrix)
            self.labels = kmeans.labels_
        except:
            print "Data read-in error!"

    def get_labels(self):
        return self.labels

    def cluster_assignment(self,new_data):
        return kmeans.predict(new_data)
