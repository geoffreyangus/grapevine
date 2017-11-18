'''
Clustering.py
-----------------------
Input: Clustering.py receives a matrix of word frequency counts that have been
normalized by TSIDF (term frequency–inverse document frequency). The algorithm
uses the sklearn package for the K-means clustering algorithm.
'''
from sklearn.cluster import KMeans
import numpy as np
from tempfile import TemporaryFile

DATA_FILE = 'frequency_matrix.npy'
NUM_CLUSTERS = 20

# Class should be able to read in a new input and add it to the current
# history of what has been clustered, should be able to recluster
# and should be able to print out new recommendations for the
# wine types


def main():
    # Freq_Matrix is a matrix containing the normalized frequencies of the
    # words in the wine reviews; each row represents one wine review
    Freq_Matrix = np.load(DATA_FILE)
    kmeans = KMEANS(n_clusters = NUM_CLUSTERS,random_state=0).fit(Freq_Matrix)
    labels = kmeans.labels_ #labels represent the new wine categories that our cluster f

    #kmeans.predict(array of word frequencies)

if __name__ == '__main__':
    main()
