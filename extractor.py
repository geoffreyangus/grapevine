import numpy as np

class FeatureExtractor():
	def extract(x):


	def bulkExtract(xList):
		m, n = xList.shape
		results = np.zeros(m, n)
		for i in range(len(xList)):
			results[i] = extract(xList[i])