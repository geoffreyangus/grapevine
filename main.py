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
import sys
import gv_view
from history_manager import History

def cluster_data():
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
	print(10 * '.','Finished Extracting Features',10 * '.')
	return vocabulary

def hasValidFlags():
	if sys.argv[1] == '-h' or sys.argv[1] == '--history':
		return True 
	return False

def main():
	if not ((len(sys.argv) == 3 and hasValidFlags()) or len(sys.argv) == 1):
		print('usage python2.7 main.py [--history | -h] [history.json]')
		return

	examples = util.read_json(util.SAMPLE_REVIEWS_FILE)
	example_features = util.load_features(util.FREQ_DATA)
	default_wines = [(examples[i], i) for i in range(len(examples[:10]))]
	if len(sys.argv) == 3:
		gv_view.display_greeting()
		history = History(sys.argv[2])
		if history.length() == 0:
			gv_view.display_no_history_message(default_wines)
			indices = input('').split(',')
			for index in indices:
				index = int(index)
				if index in range(1, len(default_wines) + 1):
					true_index = default_wines[index-1][1]
					history.add_wine(true_index, [0] * 10 + [1], 1)
				else:
					print('invalid index')

		history.save_state()
		# predictor = Predictor(model, history)
		return

	vocabulary = extract_data(file=util.SAMPLE_REVIEWS_FILE)
	model = cluster_data()
	# quantify success
	util.print_performance(model, vocabulary)
	sse = util.output_sse(model, example_features)
	print(sse)
	print(sum(sse.values()))
if __name__ == '__main__':
	main()
