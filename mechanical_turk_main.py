'''
main.py: main program that calls on cluster and predictor classes to recommend
a user wine.
'''

from cluster import Cluster
from cluster_em import ClusterEM
from predictor import Predictor
from feature_extraction import FeatureExtractor
import os.path
import pickle
import json
import numpy as np
import util
import collections
import sys
import gv_view
from history_manager import History
import operator 

def run_em():
	# print('...Running EM Algorithm...')
	em_model = ClusterEM()
	em_model.run_model()
	return em_model

def run_km():
	# print('...Clustering Data...')
	cluster_model = Cluster()
	cluster_model.cluster_data()
	return cluster_model

def extract_data(file = util.JSON_FILE):
	vocabulary = {}
	if(not (os.path.isfile('word_freq.npz') and os.path.isfile('raw_features.npz') and os.path.isfile('./data/review_vocabulary.npy'))):
		# print(10 * '.',' Extracting Features', 10 * '.')
		features = FeatureExtractor()
		features.extract(file)
		vocabulary = features.get_review_vocabulary()
	else:
		vocabulary = np.load('./data/review_vocabulary.npy')[()]

	vocabulary = dict((v,k) for k,v in vocabulary.items())
	# print(10 * '.','Finished Extracting Features',10 * '.')
	return vocabulary

def hasValidFlags():
	if sys.argv[1] == '-h' or sys.argv[1] == '--history':
		return True 
	return False

def main():
	vocabulary = extract_data(file=util.SAMPLE_REVIEWS_FILE)
	model = run_em()
	assignments = model.get_assignments()

	examples = util.read_json(util.UNPROCESSED_FILTERED_REVIEWS_FILE)
	cleaned_examples = util.read_json(util.FILTERED_REVIEWS_FILE)
	example_features = util.load_features(util.FREQ_DATA)

	adjectives = ['licorice', 'raspberry', 'lemon', 'crisp', 'cherry', 'full', 'rich', 'light', 'blackberry', 'simple']
	if len(sys.argv) == 4:
		history = History(sys.argv[2])
		# flipped_vocabulary = dict((v,k) for k,v in vocabulary.items())
		# print('\nWelcome to Grapevine. Please fill out this short form in order to calibrate our recommender.')
		# print('\nWhat are the top three adjectives you would use to describe your ideal wine? Please answer as if you are tasting a single wine.\n')
		# for i in range(len('adjectives')):
		# 	print(i, adjectives[i])
		# indices = [int(index_str) for index_str in input('\n').split(',')]
		strIndices = sys.argv[3].split(',')
		indices = [int(index) for index in strIndices]
		print('\nYou have selected the following words:\n')
		for i in indices:
			print(adjectives[i])
		print('\nLoading recommendations...\n')
		cluster_counts = collections.defaultdict(int)
		with open('top_em_words.json') as f:
			word_to_cluster = json.load(f)
			for index in indices:
				possible_clusters = word_to_cluster[adjectives[index]]
				for candidate in possible_clusters:
					cluster_counts[candidate] += 1
		
		# demo_clusters = [max(cluster_counts.items(), key=operator.itemgetter(1))[0]]
		demo_clusters = possible_clusters
		print('Choosing from cluster:', demo_clusters)
		predictor = Predictor(examples, example_features)
		recommendations = predictor.predict(model, history, examples, example_features, demo_clusters)
		# print('-------HISTORY-------')
		# for wine in history.get_history():
		# 	print('--',cleaned_examples[wine['true_index']])
		print('---RECOMMENDATIONS---\n')
		for true_index in recommendations:
			if true_index == recommendations[-1]:
				print('------WILDCARD-------\n')
			examples[true_index].pop('url', None)
			examples[true_index].pop('region', None)
			examples[true_index].pop('country', None)
			examples[true_index].pop('winery', None)
			examples[true_index]['name'] = examples[true_index]['name'] + ' ' + examples[true_index]['vintage']
			examples[true_index].pop('vintage', None)
			print(json.dumps(examples[true_index], indent=4),'\n')
		return

	# util.print_performance_km(model, vocabulary)
	# quantify success
	# util.print_performance(model, vocabulary)
	# sse = util.output_sse(model, example_features)
	# print(sse)
	# print(sum(sse.values()))

if __name__ == '__main__':
	main()
