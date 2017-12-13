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
		print('usage python2.7 main.py [--history | -h] [history.json]')
		return

	vocabulary = extract_data(file=util.SAMPLE_REVIEWS_FILE)
	model = run_em()
	assignments = model.get_assignments()

	examples = util.read_json(util.UNPROCESSED_FILTERED_REVIEWS_FILE)
	cleaned_examples = util.read_json(util.FILTERED_REVIEWS_FILE)
	example_features = util.load_features(util.FREQ_DATA)

	adjectives = ['dark', 'red', 'citrus', 'white', 'cherry', 'full', 'rich', 'fruity', 'plum', 'apple']
	if sys.argv[1] == '-h':
		history = History(sys.argv[2])
		flipped_vocabulary = dict((v,k) for k,v in vocabulary.items())
		print('\nWelcome to Grapevine. Please fill out this short form in order to calibrate our recommender.')
		print('\nWhat are the top three adjectives you would use to describe your ideal wine? Please answer as if you are tasting a single wine.\n')
		for i in range(len('adjectives')):
			print(i, adjectives[i])
		indices = [int(index_str) for index_str in input('\n').split(',')]
		selected_wines = []
		for index in indices:
			word_scores = example_features[:, flipped_vocabulary[adjectives[index]]].toarray().reshape(1,-1)[0]
			true_indices = np.argpartition(word_scores, -10)[-10:]
			selected_wines += [int(true_indices[i]) for i in range(len(true_indices))]

		new_history = []
		for true_index in selected_wines:
			new_history.append((true_index, list(assignments[true_index]), 1))
		history.set_history(new_history)
		history.save_state()
	
	# util.print_performance_em(model.em, vocabulary)

	# print(example_features[15854])
	# print(cleaned_examples[15854])

	# default_wines = [(examples[i], i) for i in range(len(examples[:10]))]
	if len(sys.argv) == 3:
		# gv_view.display_greeting()
		# history = History(sys.argv[2])
		# if history.length() == 0:
		# 	gv_view.display_no_history_message(default_wines)
		# 	indices = input('').split(',')
		# 	for index in indices:
		# 		index = int(index)
		# 		if index in range(1, len(default_wines) + 1):
		# 			true_index = default_wines[index - 1][1]
		# 			history.add_wine(true_index, list(assignments[true_index]), 1)
		# 		else:
		# 			print('invalid index')

		# else:
		# 	history_max = 0
		# 	new_history = []
		# 	for i in range(len(assignments)):
		# 		true_index = i
		# 		assignment = assignments[i]
		# 		if np.argmax(assignment) == 8:
		# 			history_max += 1
		# 			new_history.append((true_index, list(assignment), 1))
		# 			if history_max == 20:
		# 				break
		# 	history.set_history(new_history)
		# history.save_state()
		# return
		predictor = Predictor(examples, example_features)
		recommendations = predictor.predict(model, history, examples, example_features)
		# print('-------HISTORY-------')
		# for wine in history.get_history():
		# 	print('--',cleaned_examples[wine['true_index']])
		print('---RECOMMENDATIONS---\n')
		for true_index in recommendations:
			if true_index == recommendations[-1]:
				print('------WILDCARD-------\n')
			print('--', examples[true_index]['review'],'\n')
		return

	# util.print_performance_km(model, vocabulary)
	# quantify success
	# util.print_performance(model, vocabulary)
	# sse = util.output_sse(model, example_features)
	# print(sse)
	# print(sum(sse.values()))

if __name__ == '__main__':
	main()
