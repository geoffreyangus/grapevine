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
import json
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

CORPUS_FILE = 'data/word_corpus.txt'

# reads in a corpus of english words
def read_word_corpus(text_file = CORPUS_FILE):
    with open(text_file,'r') as f:
        return [x.strip() for x in f.readlines()]

def read_json(json_file):
    print('...Loading in JSON...')
    with open(json_file,'r') as f:
        dictionary = json.load(f)
    print('...Done...')
    return dictionary

class Feature_Extractor(object):
    '''
    Json List, Reviews, Word_Freq, Data_Features
    Models: v (Dict Vetorizer), w (TfidfVectorizer)
    '''
    def __init__(self,json_file):
        self.json_list = read_json(json_file)
        self.reviews = []
        print('...Cleaning Data...')
        for json in self.json_list:
            self.reviews.append(json['review'])
            try:
                del json['url']
                del json['name']
            except KeyError:
                pass
        print('...Parsing Data...')
        self.v = DictVectorizer(sparse=True)
        self.w = TfidfVectorizer(input='content')
        self.word_freq = self.w.fit(self.reviews)
        self.data_features = self.v.fit(self.json_list)
        print('...Saving Data...')
        self.save_matrix()

    def save_matrix(self):
        np.save('raw_features.npy',self.data_features)
        np.save('word_freq.npy',self.word_freq)
        pass

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
