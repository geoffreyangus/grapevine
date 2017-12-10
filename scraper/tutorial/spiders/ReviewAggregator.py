import os
import sys
import json
from subprocess import call

def aggregateReviews(reviewFile, superAggregation):

	if not superAggregation:
		reviews = []
		for filename in os.listdir('./'):
		    if reviewFile + 'T' in filename: 
		        with open(filename) as f:
		        	reviews += json.load(f)

		with open(reviewFile + '.json', 'w') as f:
			json.dump(reviews, f, indent=4)
	else:
		reviews = []
		for filename in os.listdir('./reviews'):
			if reviewFile in filename:
				with open('./reviews/' + filename) as f:
					print 'adding', filename
					reviews += json.load(f)

		with open('reviews.json', 'w') as f:
			json.dump(reviews, f, indent=4)

def main():
	if len(sys.argv) < 2:
		print 'Usage: python2.7 ReviewScraper reviewPrefix [--all]'
		return

	reviewFile = sys.argv[1]

	if len(sys.argv) == 3:
		aggregateReviews(reviewFile, True)
		return

	aggregateReviews(reviewFile, False)

	open('reviews/' + reviewFile + '.json', 'w').close()
	os.rename(os.getcwd() + '/' + reviewFile + '.json', os.getcwd() + '/reviews/' + reviewFile + '.json')

if __name__== "__main__":
	main()