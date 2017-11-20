from subprocess import call
import sys

def main():
	if len(sys.argv) != 2:
		print 'Usage: python2.7 ReviewScraper [wineries]'
		return

	open('test_reviews.json', 'w').close()
	commands = [
		'scrapy', 
		'crawl', 
		'reviews', 
		'-a', 
		'wineries=' + sys.argv[1], 
		'-o', 
		'test_reviews.json']
	call(commands)

if __name__== "__main__":
	main()