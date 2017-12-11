CORPUS_FILE = 'data/word_corpus.txt'
FILTERED_REVIEWS_FILE = './data/filtered_reviews.json'
REVIEW_VOCABULARY_FILE = './data/review_vocabulary'
FILTERED_FEATURE_DICT_FILE = './data/filtered_feat_dict.json'
NUM_CLUSTERS = 5 # number of clusters
FREQ_DATA = 'word_freq.npz' # file that contains the matrix
FEAT_DATA = 'raw_features.npz'
OUTPUT_MODEL = 'k_means_model.sav'
OUTPUT_MODEL_EM = 'em_model.sav'
JSON_FILE = 'data/reviews.json'
PICKLE_FILE = 'k_means_model.sav'
SAMPLE_REVIEWS_FILE = './data/sample_reviews.json'
SAMPLE_FEATURE_DICT_FILE = './data/sample_feat_dict.json'

def getStopwords():
	STOPWORDS = set()
	with open('stopwords.txt') as f:
		STOPWORDS = f.readlines();
		STOPWORDS = set([s[:-1] for s in STOPWORDS])
	return STOPWORDS
