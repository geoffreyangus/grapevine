import util
import json
import numpy as np

def read_json(json_file):
    print('...Loading in JSON...')
    with open(json_file,'r') as f:
        dictionary = json.load(f)
    print('...Done...')
    return dictionary

def main():
	dictionary = read_json(util.FILTERED_REVIEWS_FILE)
	m = len(dictionary)
	sample = np.random.choice(range(m), size=int(m / 5), replace=False)
	sample_reviews = []
	with open(util.JSON_FILE, 'r') as f:
		reviews = json.load(f)
		for i in sample:
			sample_reviews.append(reviews[i])

	with open(util.SAMPLE_REVIEWS_FILE, 'w+') as f:
		json.dump(sample_reviews, f, indent=4)

if __name__ == '__main__':
	main()