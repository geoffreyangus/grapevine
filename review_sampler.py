import util
import json
import numpy as np

def select_review_samples():
	dictionary = util.read_json(util.FILTERED_REVIEWS_FILE)
	m = len(dictionary)
	sample = np.random.choice(range(m), size=int(m / 5), replace=False)
	sample_reviews = []
	with open(util.JSON_FILE, 'r') as f:
		reviews = json.load(f)
		for i in sample:
			sample_reviews.append(reviews[i])

	with open(util.SAMPLE_REVIEWS_FILE, 'w+') as f:
		json.dump(sample_reviews, f, indent=4)

def main():
	select_review_samples()

if __name__ == '__main__':
	main()