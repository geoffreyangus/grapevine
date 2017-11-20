from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy_splash import SplashRequest
from scrapy_splash import SplashFormRequest

import re

class WinerySpider(InitSpider):
	name = 'wineries'
	allowed_domains = ['winespectator.com']
	login_page = 'https://www.winespectator.com/auth/login'
	start_urls = ['http://www.winespectator.com/wines/browse']

	def __init__(self, *args, **kwargs):
		super(WinerySpider, self).__init__(*args, **kwargs) 

		self.locations = kwargs.get('locations')
		if not self.locations:
			raise ValueError('No locations given')

	def init_request(self):
		print '=============INITIALIZING==============='
		"""This function is called before the scraping starts."""
		return Request(url=self.login_page, callback=self.login)

	def login(self, response):
		"""Generate a login request."""
		return SplashFormRequest.from_response(response,
					formdata={'userid': 'gdlangus@gmail.com', 'passwd': 'cs22wine'},
					callback=self.check_login_response)

	def check_login_response(self, response):
		"""Check the response returned by a login request to see if we are
		successfully in the mainframe.
		"""
		if 'Welcome, Geoffrey Angus' in response.body:
			self.log("Successfully logged in. Let's start crawling!")
			# Now the scraping can begin..
			return self.initialized()
		else:
			self.log('Bad times :(')

	def next_location(self, location):
		index  = self.locations.index(location[0])
		return self.locations[index + 1] if index < len(self.locations) - 1 else '-1'

	def iterate_location(self, location, change_category):
		if(change_category):
			location = self.next_location(location)
			return (location, 1) if location != '-1' else None
		
		return (location[0], location[1] + 1)

	def parse(self, response):
		location = (self.locations[0], 1)
		request = SplashRequest(
				'http://winespectator.com/wines/getwineries?b=%s&page=%s' % location,
				self.parse_single,
				endpoint='render.html',
				args={
					'http_method': 'GET'
				}
			)
		request.meta['location'] = location
		yield request

	def parse_single(self, response):
		location = response.meta['location']
		wineries = response.css('table tr td>a:first-child')
		M = len(wineries)

		for i in range(M):
			winery = wineries[i].extract()
			print winery
			url, name = re.match(r'<a href="%5C\/(.*)">(.+?(?=&lt;))', winery).groups()
			url = url.replace('%5C', '').replace('&amp;', '&')
			yield {'name':  name, 'url': url}			
		
		location = self.iterate_location(location, M == 0)
		if (location is not None):

			request = SplashRequest(
				'http://winespectator.com/wines/getwineries?b=%s&page=%s' % location,
				self.parse_single,
				endpoint='render.html',
				args={
					'http_method': 'GET'
				}
			)
			request.meta['location'] = location
			yield request