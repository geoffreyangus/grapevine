'''
Clustering.py
-----------------------
Input: Clustering.py receives a matrix of word frequency counts that have been
normalized by TSIDF (term frequency–inverse document frequency).
'''
from sklearn.cluster import KMeans
import numpy as np
from tempfile import TemporaryFile

DATA_FILE = 'frequency_matrix.npy'
NUM_CLUSTERS = 20

def main():
    # Freq_Matrix is a matrix containing the normalized frequencies of the
    # words in the wine reviews; each row represents one wine review
    Freq_Matrix = np.load(DATA_FILE)
    kmeans = KMEANS(n_clusters = NUM_CLUSTERS,random_state=0).fit(Freq_Matrix)
    labels = kmeans.labels_

if __name__ == '__main__':
    main()
