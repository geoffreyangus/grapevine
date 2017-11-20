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
Initialize the Predictor with:
1) centroid positions / number of centroids
2) the assignment of all of the wines to one of the clusters
3) the history of wine predictions
4) the history of cluster assignments
5) the history of prediction responses (1: good, 0: bad )
'''

ALPHA, BETA, GAMMA = 1.0 #Currently Hyper-parameters aren't tuned

class Predictor(object):
    def __init__(self,centroids,assignments):
        self.centroids = centroids
        self.num_centroids = len(centroids)
        self.assignments = assignments # Matrix needs to also contain the price and the quality of the wine
        self.prediction_history = np.zeros(assignments.shape)
        self.cluster_history = np.zeros(assignments.shape)
        self.prediction_response = np.zeros(assignments.shape)

    def new_prediction(self,cluster_assignment):
        opt_cluster = self.find_cluster() #returns the index of cluster assignment
        opt_wine = self.calculate_cost(opt_cluster)
        #NOTE: code below not implemented yet
        reponse = self.get_response() # Get a response from the user whether they liked it
        pass

'''
Algorithm that for a set of past wines predict where we will be
drawing the new wine from. Looks over the entire history of wine
recommendations

NOTE: Commented out original suggestion for finding cluster
# cluster_probs = cluster_response/cluster_size
# cluster_prop = cluster_size / sum_reponses
# delta = (1 - np.dot(cluster_probs,cluster_prop))/num_clusters
# The probability with which we want to sample from each of the clusters
# sampling_probs = delta * np.multiply(cluster_probs, cluster_prop)
'''

    def find_cluster(self):
        cluster_size = np.zeros((self.num_centroids,1))
        cluster_response = np.zeros((self.num_centroids,1))
        for i,cluster in enumerate(self.cluster_history):
            cluster_size[cluster] += 1
            cluster_response[cluster] += self.prediction_response[i]
        sum_responses = self.prediction_history.shape[0]
        epsilon = sum_responses/2 # arbitrarily selected biar
        # multiplication of each cluster probability with the size of the cluster
        denominator = np.multiply(cluster_size, cluster_response)
        sampling_probs = [(i+(epsilon/num_clusters))/(np.sum(denominator)+epsilon) for i in denominator]
        return np.random.choice(num_clusters,1,sampling_probs)

'''
Find the cluster and how many times the user liked
the output of this cluster, keep a running count of how many
elements are within this cluster
'''

    def calculate_cost(self,opt_cluster):
        wine_group = self.assignments[np.where(opt_cluster == self.centroids[:])]
        # find all of the wines from the past recommendations nd put them in
        # here too
        for i in range(wine_group.shape[0]):
            # put the cost and the quality and the past recommendations in
            # some sort of gradient descent step. 
        pass

    def get_response(self):
        pass
