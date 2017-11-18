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

CORPUS_FILE = 'word_corpus.txt'
JSON_FILE = 'json.txt'

# reads in a corpus of english words
def read_word_corpus(text_file = CORPUS_FILE):
    with open(text_file,'r') as f:
        return [x.strip() for x in f.readlines()]

# Assumign that the Json object is stored as a list of strings, where each
# string can be parsed out to be a dcionatry
def read_json(text_file = JSON_FILE):
    dictionaries = []
    with open(text_file,'r') as f:
        dic_str_list = f.readlines()
        for dic_str in dic_str_list:
            dictionaries.append(json.loads(dic_str))
    return dictionaries

class Feature_Extractor(object):
    def __init__(self):
        self.json_list = read_json()
        self.word_corpus = read_word_corpus()
        self.freq_matrix = np.zeros((len(self.json_list),len(self.word_corpus)))

    def count_freq(review):
        len_words = len(review)
        freq_array = np.zeros((1,len_words))
        for i, word in enumerate(review):
            index = self.word_corpus.index(word)
            freq_array[index] += 1
        return freq_array/len_words

    def parse_reviews(self):
        num_wines = len(self.json_list)
        for i in range(num_wines):
            current_json = self.json_list[i]
            review_str = current_json[review] #review is the key of the review content
            self.freq_matrix[i,:] = count_freq(review_str)

    def save_matrix(self):
        np.save('frequency_matrix.npy',self.freq_matrix)
