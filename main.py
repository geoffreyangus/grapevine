'''
main.py: main program that calls on cluster and predictor classes to recommend
a user wine.
'''

from cluster import Cluster
from predictor import Predictor
from feature_extraction import FeatureExtractor
import os.path
import pickle
import json
import numpy as np
import util
import collections

def unpickle():
	model = pickle.load(open(util.PICKLE_FILE, 'rb'))
	return model

def print_performance(model, vocabulary):
	centroids = model.get_clusters()
	assignment_indices = model.get_assignments()
	assignments = collections.defaultdict(int)
	for index in assignment_indices:
		assignments[index] += 1
	numWords = 25
	for i in range(len(centroids)):
		tfidfIndices = [(centroids[i][j], j) for j in range(centroids[i].shape[0])] # list of (score, index in centroid vector)
		tfidfIndices = sorted(tfidfIndices, key=lambda x: x[0], reverse=True)
		print('top '+ str(numWords) + ' words in centroid ' + str(i) + ' with size ' + str(assignments[i]))
		numPrinted = 0
		k = -1
		while numPrinted < numWords:
			k += 1
			if vocabulary[tfidfIndices[k][1]] in util.getStopwords() or vocabulary[tfidfIndices[k][1]].isdigit(): continue
			print(vocabulary[tfidfIndices[k][1]])#, tfidfIndices[k][0])
			numPrinted += 1

def cluster_data():
	print('...Clustering Data...')
	# cluster_model = Cluster()
	cluster_model = Cluster()
	cluster_model.cluster_data()
	return cluster_model

def extract_data(file = util.JSON_FILE):
	vocabulary = {}
	if(not (os.path.isfile('word_freq.npz') and os.path.isfile('raw_features.npz') and os.path.isfile('./data/review_vocabulary.npy'))):
		print(10 * '.',' Extracting Features',10 * '.')
		features = FeatureExtractor()
		features.extract(file)
		vocabulary = features.get_review_vocabulary()
	else:
		vocabulary = np.load('./data/review_vocabulary.npy')[()]
		
	vocabulary = dict((v,k) for k,v in vocabulary.items())
	print(10 * '.','Finished Extracting Features',10 * '.')
	return vocabulary

def main():
	vocabulary = extract_data(file=util.SAMPLE_REVIEWS_FILE)
	model = cluster_data()
	print_performance(model, vocabulary)

if __name__ == '__main__':
	main()
