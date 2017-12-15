from subprocess import call
import sys
import itertools
import random

adjectives = ['licorice', 'raspberry', 'lemon', 'crisp', 'cherry', 'full', 'rich', 'light', 'blackberry', 'simple']
dark =  ['0','1','4','5','6','8']
light = ['2','3','5','6','7','9']

def getKeywordsFromIndices(indices):
	for index in indices:
		print(adjectives[index])

def getCombinations(arr):
	combinationList = list(itertools.combinations(arr, 3))
	combinationList = [','.join(choice) for choice in combinationList]
	return combinationList

def main():
	if len(sys.argv) != 2:
		print('usage: python mechanical_turk_main.py [num_iterations]')
		return

	darkList = getCombinations(dark)
	lightList = getCombinations(light)

	allList = darkList + lightList

	numIterations = int(sys.argv[1])
	for iteration in range(numIterations):
		strIndices = random.choice(allList)
		intIndices = [int(num) for num in strIndices.split(',')]
		# print('--------------------------------ITERATION '+str(iteration + 1)+'--------------------------------')
		# keywords = getKeywordsFromIndices(intIndices)
		call(['python3', 'mechanical_turk_main.py', '-h', 'history.json', strIndices])

if __name__ == '__main__':
	main()