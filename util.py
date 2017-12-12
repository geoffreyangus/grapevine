from scipy import sparse
import json
from scipy.spatial import distance
import collections
import hashlib

CORPUS_FILE = 'data/word_corpus.txt'
FILTERED_REVIEWS_FILE = './data/filtered_reviews.json'
REVIEW_VOCABULARY_FILE = './data/review_vocabulary'
FILTERED_FEAT_DICT_FILE = './data/filtered_feat_dict.json'
NUM_CLUSTERS = 12 # number of clusters
FREQ_DATA = 'word_freq.npz' # file that contains the matrix
FEAT_DATA = 'raw_features.npz'
OUTPUT_MODEL = 'k_means_model.sav'
OUTPUT_MODEL_EM = 'em_model_12.sav'
JSON_FILE = 'data/reviews.json'
PICKLE_NAME = 'k_means_model'
SAMPLE_REVIEWS_FILE = './data/sample_reviews.json'
SAMPLE_FEAT_DICT_FILE = './data/sample_feat_dict.json'

def compute_MD5_hash(my_string):
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()

def getStopwords():
	STOPWORDS = set()
	with open('stopwords.txt') as f:
		STOPWORDS = f.readlines();
		STOPWORDS = set([s[:-1] for s in STOPWORDS])
	return STOPWORDS

def read_json(json_file):
    print('...Loading in JSON...')
    with open(json_file,'r') as f:
        dictionary = json.load(f)
    print('...Done...')
    return dictionary

def print_performance_em(model,vocabulary):
	max_words = 10
	means = model.means_
	for i in range(means.shape[0]):
		mean = means[i,:]
		max_indices = np.argsort(mean)[-max_words:]
		top_words = []
	for j in range(max_words):
		top_words.append(vocabulary[max_indices[-j]])
	print('Cluster,', i+1, 'top words: ', top_words)

def print_performance_km(model, vocabulary):
	centroids = model.get_clusters()
	assignment_indices = model.get_assignments()
	assignments = collections.defaultdict(int)
	for index in assignment_indices:
		assignments[index] += 1
	numWords = 10
	for i in range(len(centroids)):
		tfidfIndices = [(centroids[i][j], j) for j in range(centroids[i].shape[0])] # list of (score, index in centroid vector)
		tfidfIndices = sorted(tfidfIndices, key=lambda x: x[0], reverse=True)
		print('top '+ str(numWords) + ' words in centroid ' + str(i) + ' with size ' + str(assignments[i]))
		numPrinted = 0
		k = -1
		while numPrinted < numWords:
			k += 1
			if vocabulary[tfidfIndices[k][1]] in getStopwords() or vocabulary[tfidfIndices[k][1]].isdigit(): continue
			print(vocabulary[tfidfIndices[k][1]])#, tfidfIndices[k][0])
			numPrinted += 1

def output_sse(model, examples):
	centroids = model.get_clusters()
	assignment_indices = model.get_assignments()
	sse = collections.defaultdict(float)
	for i in range(len(assignment_indices)):
		k = assignment_indices[i]
		sse[k] += distance.sqeuclidean(centroids[k], examples[i].todense())
	return sse

# data file assumed to be in .npy file format
def load_features(data):
    return sparse.load_npz(data)

# reads in a corpus of english words
def read_word_corpus(text_file = CORPUS_FILE):
    with open(text_file,'r') as f:
        return [x.strip() for x in f.readlines()]
