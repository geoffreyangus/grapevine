import collections
import json
import re
import urllib

def main():
	wineries = []
	with open('wineries.json') as f:
		wineries = json.load(f)

	wineryDict = collections.defaultdict(list)

	urlIndex = wineries[0]['url'].rfind('=') + 1
	for winery in wineries:
		wineryDict[winery['url'][urlIndex:urlIndex + 2].upper().replace('.', '%')].append(winery)

	print sorted(wineryDict.keys())

	for key in wineryDict.keys():
		with open('wineries/' + key + '.json', 'w') as f:
			json.dump(wineryDict[key], f, indent=4)

if __name__== "__main__":
	main()