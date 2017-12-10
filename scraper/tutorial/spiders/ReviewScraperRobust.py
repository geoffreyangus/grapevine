from subprocess import call
import sys
import datetime
import json
import re
import os
import time

TIME_SLEEP = 300

def updateWineryIndex(wineryUrls, reviewIterationFile):
	newReviews = []
	with open(reviewIterationFile, 'r') as f:
		newReviews = json.load(f)

	lastReview = newReviews[-1]['url']
	if lastReview in wineryUrls:
		return wineryUrls.index(lastReview) + 1
	return -1

def main():
	if len(sys.argv) != 3:
		print 'Usage: python2.7 ReviewScraper [wineries] [reviewFilename]'
		return

	masterWineryJSONFile = sys.argv[1]
	wineryFilename = sys.argv[1][:-5]
	reviewFilename = sys.argv[2][:-5]

	wineries = []
	with open(masterWineryJSONFile) as f:
		wineries = json.load(f)

	# One time copy of the winery names, in order to make search faster
	wineryUrls = [wineries[i]['url'] for i in range(len(wineries))]
	t = 1
	wineryIterationFile = wineryFilename + 'T' + str(t) + '.json'

	# Write a copy of the full set of wineries to the first file iteration
	with open(wineryIterationFile, 'w+') as f:
		json.dump(wineries, f, indent=4)

	attempts = 1
	wineryIndex = 0
	while wineryIndex != -1:

		reviewIterationFile = reviewFilename + 'T' + str(t) + '.json'
		open(reviewIterationFile, 'w').close()
		commands = [
			'scrapy', 
			'crawl', 
			'reviews', 
			'-a', 
			'wineries=' + wineryIterationFile, 
			'-o', 
			reviewIterationFile
		]
		call(commands)

		attempts += 1
		if os.path.getsize('./' + reviewIterationFile) > 0:
			print 'Scrapy failure. Rebooting at iteration ' + str(t)
			# Updates the winery index to the first unprocessed wine
			wineryIndex = updateWineryIndex(wineryUrls, reviewIterationFile)
			t += 1
			wineryIterationFile = wineryFilename + 'T' + str(t) + '.json'

			# Write a file with the unprocessed wineries
			with open(wineryIterationFile, 'w+') as f:
				if len(wineries[wineryIndex:]) == 0:
					break
				json.dump(wineries[wineryIndex:], f, indent=4)
		else:
			numMinutes = TIME_SLEEP / 60
			print 'Consecutive Scrapy failures. Reattempting iteration ' + str(t) + ' in ' + str(numMinutes) + ' minutes.'
			time.sleep(TIME_SLEEP)

	print 'Scraping completed. ' + str(t) + ' successful scrapes. ' + str(attempts) + ' attempted scrapes.'

if __name__== "__main__":
	main()