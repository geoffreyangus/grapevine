'''
Predictor.py
-----------------------
Input: Predictor Class returns the optimal wine that we predict for a user.
Predictor takes in a history of past wine recommendations as well as the
unsupervised learning algorithm that clustered the wines. The algorithm
then first hard clusters data (followed by soft-cluster depending on if
EM algorithm was used as the unsupervised learning algorithm). Afterwards,
the optimal wine is selected by maximizing a cost function.
'''

import numpy as np
import random
from scipy import sparse
from scipy.sparse import csr_matrix

'''
History brought in as a File of JSON obects in the form of:

{
user_feedback: -1 | 1,
cluster: [0, k]
confidence: # always 1 if k-means, if EM prob returned
features: [...]
score: R
price: R
wine_id: MD5 hash
}

'''
'''
extra_cluster: returns the index of the cluster in which we want to begin
our analysis of the ideal wine selection.s
'''

def extra_cluster(history,model):
    num_clusters = model.num_clusters()

    probs = np.zeros(num_clusters) #Final probabilities that we will return (multinomial)
    pos = np.zeros(num_clusters)
    neg = np.zeros(num_clusters)
    num_wines = np.zeros(num_clusters)
    denominator = 0
    for wine in history:
        cluster_assignment = wine['cluster']
        if(user_feedback == 1):
            pos[cluster_assignment] += 1
        else
            neg[cluster_assignment] += 1
        num_wines[cluster_assignment] += 1

        pos_total = np.sum(pos)
        neg_total = np.sum(neg)
        num_total = np.sum(num_wines)

    probs = [num[k]*(pos[k]/pos_total)*(1-neg[k]/neg_total) for k in num_clusters]
    probs = probs/sum(probs)
    return random.choices(range(num_clusters),weights=probs, k=1)


class Predictor(object):
    def __init__(self):
        pass

    def predict(self,model,history):
        cluster_index = extra_cluster(history)
        wine_options = [] # Selecting the wine options from which we will
                          # optimize to find the ideal wine
        if(type(model) == ClusterEM):

        else:
            #NOTE: EM doesn't have assignments!
            for i in range(len(model.assignments)):
                if(model_assignments[i] == cluster_index):
                    wine_options.append(i)



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

    # Algorithm that for a set ofpast wines predict where we will be
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
        epsilon = sum_responses/2 # arbitrarily selected biar
        # multiplication of each cluster probability with the size of the cluster
        denominator = np.multiply(cluster_size, cluster_response)
        sampling_probs = [(i+(epsilon/num_clusters))/(np.sum(denominator)+epsilon) for i in denominator]
        return np.random.choice(k,1,sampling_probs)
        # NOTE: Commented out original suggestion for finding cluster
        # cluster_probs = cluster_response / cluster_size
        # cluster_prop = cluster_size / sum_reponses
        # delta = (1 - np.dot(cluster_probs,cluster_prop))/num_clusters
        # The probability with which we want to sample from each of the clusters
        # sampling_probs = delta * np.multiply(cluster_probs, cluster_prop)

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
        pass
