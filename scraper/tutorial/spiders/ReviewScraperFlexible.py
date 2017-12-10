from subprocess import call
import sys
import datetime
import json
import re
import os
import time

TIME_SLEEP = 300

def aggregateWineries(letters):
	wineries = []
	for filename in os.listdir('wineries'):
	    if filename[0] in letters: 
	        with open('wineries/' + filename) as f:
	        	wineries += json.load(f)
	return wineries

def main():
	if len(sys.argv) != 3:
		print 'Usage: python2.7 ReviewScraper wineryLetters reviewPrefix'
		return

	reviewFile = sys.argv[2] + '_' + sys.argv[1].replace('%', 'misc') + '.json'

	wineries = aggregateWineries(sys.argv[1])
	wineryFile = 'flexibleWineries.json'

	# Write a copy of the full set of wineries to the first file iteration
	with open(wineryFile, 'w') as f:
		json.dump(wineries, f, indent=4)

	commands = [
		'python2.7',
		'ReviewScraperRobust.py',
		wineryFile,
		reviewFile
	]
	call(commands)

	commands = [
		'python2.7',
		'ReviewAggregator.py',
		reviewFile[:-5]
	]
	call(commands)


if __name__== "__main__":
	main()