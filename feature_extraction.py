'''
Feature_extraction.py
-----------------------
Input: Feature Extractor Class reads in a list of over 100,000 reviews from
wine spectator and extracts features. The class then calls on methods to
extract features from this list of json objects.
Edit(Nov 18, 2017): Currently the Extractor only reads in the json list and
parses out the individual reviews, couting the frequencies and then placing
these into the frequency matrix.
'''

import numpy as np
from scipy import sparse
from scipy.sparse import csr_matrix
import json
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import util

# reads in a corpus of english words
def read_word_corpus(text_file = util.CORPUS_FILE):
    with open(text_file,'r') as f:
        return [x.strip() for x in f.readlines()]

def read_json(json_file):
    print('...Loading in JSON...')
    with open(json_file,'r') as f:
        dictionary = json.load(f)
    print('...Done...')
    return dictionary

class FeatureExtractor(object):
    '''
    Json List, Reviews, Word_Freq, Data_Features
    Models: v (Dict Vetorizer), w (TfidfVectorizer)
    '''
    def __init__(self):
        self.reviews = []
        self.feat_dic = []
        self.v = DictVectorizer(sparse=True)
        self.w = TfidfVectorizer(input='content')

    def filter_reviews(self, json_list):
        self.json_list = read_json(json_list)
        print('...Cleaning Data...')
        for json in self.json_list:
            # removing wine reviews that have a score less than 80
            try:
                if (int(json['score']) < 80):
                    self.json_list.remove(json)
                    continue
            except:
                self.json_list.remove(json)
                continue
            # Adding only the relevant features that we want to
            # analyze to the feature dictionary (feat_dic)
            json_feat = {}
            try:
                json_feat['country'] = json['country']
                json_feat['winery'] = json['winery']
                json_feat['region'] = json['region']
                json_feat['vintage'] =json['vintage']
            except KeyError:
                pass
            self.feat_dic.append(json_feat)
            reviewTokens = json['review'].replace('.','').replace(',', '').split(' ')
            filteredTokens = []
            STOPWORDS = util.getStopwords()
            for token in reviewTokens:
                loweredToken = token.lower() # lol
                if token.isdigit() or loweredToken in STOPWORDS:
                    continue
                filteredTokens.append(loweredToken)
            self.reviews.append(' '.join(filteredTokens))
        self.save_filtered_reviews()

    def process_reviews(self):
        print('...Parsing Data...')
        self.word_freq = csr_matrix(self.w.fit_transform(self.reviews).toarray())
        self.data_features = csr_matrix(self.v.fit_transform(self.feat_dic).toarray())
        print('size word freq', self.word_freq.shape)
        print('data feats freq', self.data_features.shape)

    def save_data(self):
        print('...Saving Data...')
        self.save_vocabulary()
        self.save_matrix()

    def extract(self, json_file):
        if not (os.path.isfile(util.FILTERED_REVIEWS_FILE) and os.path.isfile(util.FILTERED_FEATURE_DICT_FILE)):
            self.filter_reviews(json_file)
        else:
            with open(util.FILTERED_REVIEWS_FILE, 'r') as f:
                self.reviews = json.load(f)
            with open(util.FILTERED_FEATURE_DICT_FILE, 'r') as f:
                self.feat_dic = json.load(f)
        self.process_reviews()
        self.save_data()

    def save_filtered_reviews(self):
        with open(util.FILTERED_REVIEWS_FILE, 'w+') as f:
            json.dump(self.reviews, f, indent=4)
        with open(util.FILTERED_FEATURE_DICT_FILE, 'w+') as f:
            json.dump(self.feat_dic, f, indent=4)

    def save_vocabulary(self):
        np.save(util.REVIEW_VOCABULARY_FILE, self.w.vocabulary_)

    def get_review_vocabulary(self):
        result = {}
        if os.path.isfile(util.REVIEW_VOCABULARY_FILE):
            result = np.load(util.REVIEW_VOCABULARY_FILE + '.npy')
        else:
            result = self.w.vocabulary_
        return result

    def save_matrix(self):
        sparse.save_npz('raw_features.npz',self.data_features)
        sparse.save_npz('word_freq.npz',self.word_freq)
        return

    def get_feature_names(self):
        return self.v.get_feature_names()

    def get_word_names(self):
        return self.w.get_feature_names()

    '''
    def count_freq(self,review):
        freq_array = np.zeros((1,len(self.word_corpus)))
        for i, word in enumerate(review):
            try:
                index = self.word_corpus.index(word)
                freq_array[index] += 1
            except:
                continue
        return freq_array/len(review)

    Old CODE

    def parse_reviews(self):
        for i,current_json in enumerate(self.json_list):
            review_str = current_json['review'] #review is the key of the review content
            if (i%5000 == 0):
                print('Status: ', i)
            if(len(review_str) > 0):
                self.freq_matrix[i,:] = self.count_freq(review_str)

    def parse_features(self):
        for i,current_json in enumerate(self.json_list):
            price = int(current_json[price])
            rating = int(current_json[rating])
            self.wine_features[i,:] = [price,rating
    '''
