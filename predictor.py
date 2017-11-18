'''
Predictor.py
-----------------------
Input: Predictor Class returns the optimal wine that we predict for a user.
Predictor relies on the output of cluster, in order to determine the
clusters of wine.
'''

from cluster import Cluster
import numpy as np

'''
def run_k_means(Cluster_Data):
    Cluster_Data.load_data()
    Cluster_Data.cluster_data()
    return (Cluster_Data.get_clusters(),Cluster_Data.get_labels())
'''

class Predictor(object):
    def __init__(self,centroids,assignments):
        self.centroids = centroids
        self.assignments = assignments
        self.prediction_history = [] # History of Recommendations

    def new_input():
        pass

    def find_cluster:
        pass

    def calculate_cost:
        pass
