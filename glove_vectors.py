import numpy as np
from scipy import sparse
from scipy.sparse import csr_matrix
from scipy.sparse import lil_matrix
from scipy.sparse import vstack
import os
import codecs
import util

class GloveVectors(object):
	'''
	Extracts GLoVE vectors and vocabulary from a pre-trained file, and
	generates the review matrix for a given set of reviews.
	'''
	def extract_glove_vectors(self):
		vocabulary = []
		glove_vectors = []
		with codecs.open(util.GLOVE_PRETRAINED_VECTORS, 'r', 'utf-8') as f:
		    for index, line in enumerate(f):
		        line = line.split()
		        word = line[0]
		        vector = np.array([float(i) for i in line[1:]]) 
		        vocabulary.append(word)
		        glove_vectors.append(vector)
		return vocabulary, glove_vectors
		
	def generate_review_matrix(self, reviews, vocabulary, glove_vectors):
		vocabulary_size = len(vocabulary)
		glove_vector_size = len(glove_vectors[0])
		review_vector_size = glove_vector_size * vocabulary_size
		
		num_reviews = len(reviews)
		block_size = 5000
		num_blocks = int(round((1.0 * num_reviews)/block_size))
		
		review_matrix = csr_matrix((0, review_vector_size))
		
        # review_matrix = _matrix((len(reviews),review_vector_size))
		review_block = np.empty((block_size, review_vector_size))
		current_block = 0
		review_count = 0
		for review in reviews:
			review_vector = np.zeros(review_vector_size)
			for index, word in enumerate(vocabulary):
				# print("Index:",index," with Word: ",word)
				base_index = glove_vector_size * index
				if word in review:
					for local_index in range(glove_vector_size):
						actual_index = base_index + local_index
						review_vector[actual_index] = glove_vectors[index][local_index]
			# print(review_vector)
		    #if review_matrix is None:
		    #    review_matrix = csr_matrix(review_vector)
		    #else:
		    #    review_matrix = vstack([review_matrix,review_vector])
			block_index = review_count % block_size
			review_block[block_index] = review_vector
		    #review_matrix[review_count] = lil_matrix(review_vector)
			review_count += 1
			if(review_count % 1000 == 0):
				print("Finished ", review_count, " reviews!")
			
			if(review_count % block_size == 0 or review_count == (num_reviews - 1)): 	
				print("Finished block ", review_count/block_size, ", repacking.")
				review_matrix = vstack([review_matrix, csr_matrix(review_block)])
				review_block = np.empty((block_size, review_vector_size))
				current_block += 1
		return review_matrix
		
	def get_review_matrix(self, reviews):
		print("...Retrieving GLoVE Review Matrix...")
		# Extract GLoVE vectors from pre-trained file
		vocabulary, glove_vectors = self.extract_glove_vectors()
		# Generate corresponding review matrix, and save it
		review_matrix = self.generate_review_matrix(reviews, vocabulary, glove_vectors)    
		return vocabulary, review_matrix