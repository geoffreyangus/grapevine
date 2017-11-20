'''
Predictor.py
-----------------------
Input: Predictor Class returns the optimal wine that we predict for a user.
Predictor relies on the output of cluster.py, in order to determine the
clusters of wine. The Class then determines the optimal prediction by:
    1) First determining the optimal cluster to sample different wines
    2) Within this cluster finding the optimal wine by a process of linear
    regression to find the wine with best quality for price.
'''

import numpy as np

'''
def run_k_means(Cluster_Data):
    Cluster_Data.load_data()
    Cluster_Data.cluster_data()
    return (Cluster_Data.get_clusters(),Cluster_Data.get_labels())
'''

class Predictor(object):
    def __init__(self,centroids,assignments):
        self.centroids = centroids # a vector with all of the centroids
        self.assignments = assignments # a vector with all of the assingments
        # History of Recommendations
        self.prediction_history = np.zeros(assignments.shape)
        # History of the clusters in which the recommended wine was drawn from
        self.cluster_history = np.zeros(assignments.shape)
        # How the user responded to the recommendations
        self.prediction_response = np.zeros(assignments.shape)


    def new_prediction(self,cluster_assignment):
        opt_cluster = self.find_cluster()
        opt_wine = self.calculate_cost(opt_cluster)
        pass

    # Algorithm that for a set of past wines predict where we will be
    # drawing the new wine from. Looks over the entire history of wine
    # recommendations

    def find_cluster(self):
        a, num_clusters = np.unique(self.cluster_history,return_counts = True)
        cluster_size = np.zeros((num_clusters,1))
        cluster_response = np.zeros((num_clusters,1))
        for i,cluster in enumerate(self.cluster_history):
            cluster_size[cluster] += 1
            cluster_response[cluster] += self.prediction_response[i]
        sum_responses = self.prediction_history.shape[0]
        cluster_probs = cluster_response/cluster_size
        cluster_prop = cluster_size / sum_reponses

        # The probability with which we want to sample from each of the clusters
        sampling_probs = cluster_probs 


# Look over all of the clusters from which we have samples wines
    def calculate_cost(self):
        num_clusters = np.unique(self.cluster_history)
        # Find the cluster and how many times the user liked
        # the output of this cluster, keep a running count of how many
        # elements are within this cluster
        for i in range(num_clusters):
            pass
        pass

    def get_response(self):
