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

CORPUS_FILE = 'word_corpus.txt'

def read_word_corpus(text_file = CORPUS_FILE):
    with open(text_file) as f:
        return f.readlines(text_file)

class Feature_Extractor(object):
    def __init__(self):
        self.json_list = None
        self.freq_matrix = None
        self.word_corpus = read_word_corpus()

    def parse_reviews(self):
        num_wines = len(self.json_list)
        freq_matrix = np.zeros((num_wines,len(self.word_corpus)))
        print(freq_matrix.size)
        #for i in range(num_wines):
        #    current_json = self.json_list[i]
