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
from matplotlib import pyplot as plt

def run_em():
	print('...Running EM Algorithm...')
	em_model = ClusterEM()
	em_model.run_model()
	return em_model

def run_km():
	print('...Clustering Data...')
	cluster_model = Cluster()
	cluster_model.cluster_data()
	return cluster_model

def extract_data(file = util.JSON_FILE):
	vocabulary = {}
	if(not (os.path.isfile('word_freq.npz') and os.path.isfile('raw_features.npz') and os.path.isfile('./data/review_vocabulary.npy'))):
		print(10 * '.',' Extracting Features', 10 * '.')
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
	if not ((len(sys.argv) == 3 and hasValidFlags()) or len(sys.argv) == 1):
		print('usage: python main.py [--history | -h] [history.json]')
		return

	vocabulary = extract_data(file=util.SAMPLE_REVIEWS_FILE)
	model = run_em()
	assignments = model.get_assignments()

	examples = util.read_json(util.UNPROCESSED_FILTERED_REVIEWS_FILE)
	cleaned_examples = util.read_json(util.FILTERED_REVIEWS_FILE)
	example_features = util.load_features(util.FREQ_DATA)

	# top clusters, 6 (plum) and 8 (lemon)
	# x-axis is plum
	# y-axis is lemon
	# means = model.em.means_

	# mean = means[6,:]
	# plum_index = np.argmax(mean)

	# mean = means[8,:]
	# lemon_index = np.argmax(mean)
	# plum1 = []
	# lemon1 = []

	# plum2 = []
	# lemon2 = []
	# for true_index in range(len(assignments)):
	# 	if np.argmax(assignments[true_index]) == 6:
	# 		example = example_features[true_index].toarray()[0]
	# 		plum1.append(example[plum_index])
	# 		lemon1.append(example[lemon_index])
	# 	if np.argmax(assignments[true_index]) == 8:
	# 		example = example_features[true_index].toarray()[0]
	# 		plum2.append(example[plum_index])
	# 		lemon2.append(example[lemon_index])

	# sample1 = list(zip(plum1, lemon1))
	# sample2 = list(zip(plum2, lemon2))


	# plum1 = [i for i in plum1 if i != 0]
	# plum2 = [i for i in plum2 if i != 0]

	# lemon1 = [i for i in lemon1 if i != 0]
	# lemon2 = [i for i in lemon2 if i != 0]

	# sampleIndices = np.random.choice(range(len(sample1)), 2000)
	# sample1 = [sample1[i] for i in range(len(sample1)) if i in sampleIndices]
	# sampleIndices = np.random.choice(range(len(sample2)), 2000)
	# sample2 = [sample2[i] for i in range(len(sample1)) if i in sampleIndices]

	# plum1 = list(zip(*sample1))[0]
	# # plum1 = [float(i) for i in plum1]
	# lemon1 = list(zip(*sample1))[1]
	# # lemon1 = [float(i) for i in lemon1]

	# plum2 = list(zip(*sample2))[0]
	# # plum2 = [float(i) for i in plum2]
	# lemon2 = list(zip(*sample2))[1]
	# # lemon2 = [float(i) for i in lemon2]

	# print (plum1)
	# plt.hist(plum1, 100, facecolor='b', label='Cluster 6') # plotting t, a separately 
	# plt.hist(plum2, 100, facecolor='r', label='Cluster 8')
	# plt.xlabel('TF-IDF Value')
	# plt.ylabel('Frequency')
	# plt.title('Non-Zero TF-IDFs of the Word \"Plum\"')
	# plt.legend()
	# # plt.hist(plum2, lemon2, facecolor='b', label='Cluster 6') # plotting t, b separately 
	# plt.show()

	# plt.hist(lemon1, 100, facecolor='b', label='Cluster 6') # plotting t, a separately 
	# plt.hist(lemon2, 100, facecolor='r', label='Cluster 8')
	# plt.xlabel('TF-IDF Value')
	# plt.ylabel('Frequency')
	# plt.title('Non-Zero TF-IDFs of the Word \"Lemon\"')
	# plt.legend()
	# # plt.hist(plum2, lemon2, c='b') # plotting t, b separately 
	# plt.show()


	# return

	adjectives = ['licorice', 'raspberry', 'lemon', 'crisp', 'cherry', 'full', 'rich', 'light', 'blackberry', 'simple']
	if sys.argv[1] == '-h':
		history = History(sys.argv[2])
		flipped_vocabulary = dict((v,k) for k,v in vocabulary.items())
		print('\nWelcome to Grapevine. Please fill out this short form in order to calibrate our recommender.')
		print('\nWhat are the top three adjectives you would use to describe your ideal wine? Please answer as if you are tasting a single wine.\n')
		for i in range(len('adjectives')):
			print(i, adjectives[i])
		indices = [int(index_str) for index_str in input('\n').split(',')]
		cluster_counts = collections.defaultdict(int)
		with open('top_em_words.json') as f:
			word_to_cluster = json.load(f)
			for index in indices:
				possible_clusters = word_to_cluster[adjectives[index]]
				for candidate in possible_clusters:
					cluster_counts[candidate] += 1
		
		demo_clusters = possible_clusters
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

if __name__ == '__main__':
	main()
