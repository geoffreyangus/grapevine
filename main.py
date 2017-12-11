'''
main.py: main program that calls on cluster and predictor classes to recommend
a user wine.
'''

from cluster import Cluster
from predictor import Predictor
from feature_extraction import Feature_Extractor
import os.path

JSON_FILE = 'data/reviews.json'

def extract_data(file = JSON_FILE):
    if(not os.path.isfile('word_freq.npz') & os.path.isfile('raw_features.npz')):
        print(10 * '.',' Extracing Features',10 * '.')
        features = FeatureExtractor(JSON_FILE)

    print(10 * '.','Finished Extracing Features',10 * '.')
    print('...Clustering Data...')
    cluster_model = Cluster()
    cluster_model.cluster_data()
    print(cluster_model.get_clusters())

if __name__ == '__main__':
    extract_data()
