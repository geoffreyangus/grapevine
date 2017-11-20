from subprocess import call
import sys

def main():
	if len(sys.argv) != 2:
		print 'Usage: python2.7 WineryScraper.py [location]'
		return
	open('wineries.json', 'w').close()
	commands = [
		'scrapy', 
		'crawl', 
		'wineries', 
		'-a', 
		'locations=' + sys.argv[1], 
		'-o', 
		'wineries.json']
	call(commands)

if __name__== "__main__":
	main()