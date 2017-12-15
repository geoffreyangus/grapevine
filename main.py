# coding: utf8
'''
 ██████╗ ██████╗  █████╗ ██████╗ ███████╗██╗   ██╗██╗███╗   ██╗███████╗
██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██╔════╝██║   ██║██║████╗  ██║██╔════╝
██║  ███╗██████╔╝███████║██████╔╝█████╗  ██║   ██║██║██╔██╗ ██║█████╗  
██║   ██║██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ╚██╗ ██╔╝██║██║╚██╗██║██╔══╝  
╚██████╔╝██║  ██║██║  ██║██║     ███████╗ ╚████╔╝ ██║██║ ╚████║███████╗
 ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝  ╚═══╝  ╚═╝╚═╝  ╚═══╝╚══════╝
 
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

def should_extract_features():
    review_matrix_exists = os.path.isfile(util.REVIEW_MATRIX)
    raw_features_exist = os.path.isfile('raw_features.npz')
    vocabulary_exists = os.path.isfile(util.REVIEW_VOCABULARY_FILE)
    return not(review_matrix_exists and raw_features_exist and vocabulary_exists)

def extract_data(file = util.JSON_FILE):
	vocabulary = {}
	if(should_extract_features()):
		print(10 * '.',' Extracting Features', 10 * '.')
		features = FeatureExtractor()
		features.extract(file)
		vocabulary = features.get_review_vocabulary()
	else:
		vocabulary = np.load(util.REVIEW_VOCABULARY_FILE)[()]
		
	print("Vocabulary shape: ", vocabulary.shape)
	vocabulary = {v:k for k,v in enumerate(vocabulary)}
	# print(10 * '.','Finished Extracting Features',10 * '.')
	return vocabulary

def hasValidFlags():
	if sys.argv[1] == '-h' or sys.argv[1] == '--history':
		return True 
	return False

def find_nearest_neighbors(k, cluster, centriod):
	if len(cluster) < k:
		return cluster
		
	k_nearest = [[] for i in range(k)]
	k_distances = [float("inf") for i in range(k)]
	for vector in cluster:
		dist = np.linalg.norm(centriod-vector)
		for i in range(k):
			k_min_dist = k_distances[i]
			if dist < k_min_dist:
				k_nearest.insert(i, vector)
				k_distances.insert(i, dist)
				k_nearest.pop()
				k_distances.pop()
				break
	return k_nearest

def main():
	if not ((len(sys.argv) == 3 and hasValidFlags()) or len(sys.argv) == 1):
		print('usage python2.7 main.py [--history | -h] [history.json]')
		return

	vocabulary = extract_data(file=util.SAMPLE_REVIEWS_FILE)
	model = run_km()
	assignments = model.get_assignments()
	centriods = model.get_clusters()

	examples = util.read_json(util.UNPROCESSED_FILTERED_REVIEWS_FILE)
	cleaned_examples = util.read_json(util.FILTERED_REVIEWS_FILE)[:45000]
	example_features = util.load_features(util.REVIEW_MATRIX)
	
	if util.USE_GLOVE_VECTORS:
		clusters = [[] for i in range(len(centriods))]
		for vector, assignment in enumerate(assignments):
			clusters[assignment].append(vector)
		
		for index, cluster in enumerate(clusters):
			print("There are ", len(cluster), " wines in cluster ", index,".")
		
		for index, cluster in enumerate(clusters):
			print("== Cluster ", index, "====")
			print("There are ", len(cluster), " wines in this cluster.")
			k_nearest = find_nearest_neighbors(5, cluster, centriods[index])
			for r in k_nearest:
				print(examples[r]["review"])
				print(" ")
			print("=======================")
		return	
	 
			
	adjectives = ['dark', 'red', 'citrus', 'white', 'cherry', 'full', 'rich', 'fruity', 'plum', 'apple']
	
	if sys.argv[1] == '-h':
		history = History(sys.argv[2])
		flipped_vocabulary = dict((v,k) for k,v in vocabulary.items())
		print('\nWelcome to Grapevine! Please fill out this short form in order to calibrate our recommender.')
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
