# from subprocess import call
# import sys
# import datetime

# def updateWineries(wineries, masterWineryJSONFile, masterReviewJSONFile, t):
# 	reviewIterationFile = 'reviewsT' + t + '.json'
# 	wineryIterationFile = 'wineriesT' + t + '.json'

# 	newReviews = []
# 	with open(reviewIterationFile, 'r') as f:
# 		newReviews = json.load(f)

# 	with open(masterReviewJSONFile, "r+") as f:
# 	    oldReviews = json.load(f)
# 		oldReviews.append(newReviews)
# 	    f.seek(0)
# 	    json.dump(oldReviews, f, indent=4)
# 	    f.truncate()

# 	lastWineryName = newReviews[-1]['winery']
# 	wineryIndex = wineries.index()
# 	wineries = wineries[]

# def main():
# 	if len(sys.argv) != 3:
# 		print 'Usage: python2.7 ReviewScraper [wineries] [reviews]'
# 		return

# 	masterWineryJSONFile = sys.argv[1]
# 	masterReviewJSONFile = sys.argv[2]

# 	wineries = []
# 	with open(masterWineryJSONFile) as f:
# 		wineries = json.load(f)

# 	t = 1
# 	wineryIterationFile = 'wineriesT' + t + '.json'
# 	with open(wineryIterationFile, 'w+') as f:
# 		json.dump(wineries, f, indent=4)

# 	while len(wineries) > 0:
# 		reviewIterationFile = 'reviewsT' + t + '.json'
# 		open(reviewIterationFile, 'w').close()
# 		commands = [
# 			'scrapy', 
# 			'crawl', 
# 			'reviews', 
# 			'-a', 
# 			'wineries=' + wineryIterationFile, 
# 			'-o', 
# 			reviewIterationFile]
# 		call(commands)
# 		wineries = updateWineries(wineries, masterWineryJSONFile, masterReviewJSONFile, t)
# 		t += 1
# 	print 'Scraping completed in ' + str(t) + ' iterations.'

# if __name__== "__main__":
# 	main()