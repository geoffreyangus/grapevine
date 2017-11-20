from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy_splash import SplashRequest
from scrapy_splash import SplashFormRequest

import re
import json

script = """
	function main(splash)
		splash:init_cookies(splash.args.cookies)
		assert(splash:go{
			splash.args.url,
			headers=splash.args.headers,
			http_method=splash.args.http_method,
			body=splash.args.body,
		})
		
		local entries = splash:history()
		local last_response = entries[#entries].response
		return {
			url = splash:url(),
			headers = last_response.headers,
			http_status = last_response.status,
			cookies = splash:get_cookies(),
			html = splash:html(),
		}
	end
"""

class ReviewSpider(InitSpider):
	name = 'reviews'
	allowed_domains = ['winespectator.com']
	login_page = 'https://www.winespectator.com/auth/login'
	start_urls = ['http://www.winespectator.com/wines/browse']

	def __init__(self, *args, **kwargs):
		super(ReviewSpider, self).__init__(*args, **kwargs) 

		wineries_file = kwargs.get('wineries')
		if not wineries_file:
			raise ValueError('No wineries given')

		with open(wineries_file) as json_data:
			self.wineries = json.load(json_data)

	def init_request(self):
		print '=============INITIALIZING==============='
		"""This function is called before the scraping starts."""
		return Request(url=self.login_page, callback=self.login)

	def login(self, response):
		# print '============LOGGING IN============'
		# print response.headers
		"""Generate a login request."""
		return FormRequest.from_response(response,
					formdata={'userid': 'gdlangus@gmail.com', 'passwd': 'cs22wine'},
					callback=self.check_login_response)

	def check_login_response(self, response):
		"""Check the response returned by a login request to see if we are
		successfully in the mainframe.
		"""
		# print '============CHECKING LOGIN============'
		# print response.headers

		if 'Welcome, Geoffrey Angus' in response.body:
			self.log("Successfully logged in. Let's start crawling!")
			# Now the scraping can begin..
			return self.initialized()
		else:
			self.log('Bad times :(')

	def parse(self, response):
		index = 0
		request = SplashRequest(
				'http://www.winespectator.com/%s' % self.wineries[index]['url'],
				self.parse_single,
				endpoint='execute',
			 	cache_args=['lua_source'],
				args={'lua_source': script},
			)
		request.meta['index'] = 0
		request.meta['page'] = 1
		yield request

	def parse_single(self, response):
		index = response.meta['index']
		page = response.meta['page']

		reviews = response.css('table')
		print '==============PARSING ('+self.wineries[index]['name']+')=============='
		if reviews:
			tbody = response.css('table').css('tbody')
			reviews = self.parseReviewTable(tbody)
			for review in reviews:
				yield review
		else:
			container = response.css('div.mod-container')
			yield self.parseReviewPage(container)

		num_pages = response.css('div.pagination a')
		if (num_pages and page < len(num_pages)):
			page += 1
			request = SplashRequest(
				'http://www.winespectator.com/%s' % self.new_page_url(self.wineries[index]['url'], page),
				self.parse_single,
				endpoint='execute',
			 	cache_args=['lua_source'],
				args={'lua_source': script},
			)
			request.meta['index'] = index
			request.meta['page'] = page
			yield request
		
		else:
			index += 1
			page = 1
			if (index < len(self.wineries)):
				request = SplashRequest(
					'http://www.winespectator.com/%s' % self.wineries[index]['url'],
					self.parse_single,
					endpoint='execute',
				 	cache_args=['lua_source'],
					args={'lua_source': script},
				)
				request.meta['index'] = index
				request.meta['page'] = page
				yield request

	def new_page_url(self, url, page):
		first = 29
		last = 29 + (url[29:].index('&'))
		return url[:first] + str(page) + url[last:]

	def cleanTableReview(self, rawReview):
		return {
			'name': re.search(r'<\/strong>([^<]*)', rawReview['name']).groups()[0].replace(u'\xa0', u''),
			'winery': re.search(r'>([^<]*)<', rawReview['winery']).groups()[0],
			'review': re.search(r'>(.+?(?=<em>))', rawReview['review']).groups()[0].replace(u'\xa0', u'').strip(),
			'vintage': rawReview['vintage'].replace('<td>', '').replace('</td>', ''),
			'score': rawReview['score'].replace('<td>', '').replace('</td>', ''),
			'price:': rawReview['price'].replace('<td>', '').replace('</td>', ''),
			'country': re.search(r'Country:</strong> ([^<]*)', rawReview['country']).groups()[0].replace(u'\xa0', u'').replace(u'\u2022', u''),
			'region': re.search(r'Region:</strong> ([^<]*)', rawReview['region']).groups()[0].replace(u'\xa0', u'').replace(u'\u2022', u'')
		}

	def parseReviewTable(self, tbody):
		processedReviews = []

		reviews = tbody.css('tr')
		for review in reviews:
			rawReview = {}

			descriptor = review.css('td:nth-child(1)')[0]
			rawReview['name'] = descriptor.css('h6 a').extract()[0]
			rawReview['winery'] = descriptor.css('h6 a strong').extract()[0]
			rawReview['review'] = descriptor.css('div.collapse').extract()[0]

			rawReview['vintage'] = review.css('td:nth-child(2)').extract()[0]	# same as year
			rawReview['score'] = review.css('td:nth-child(3)').extract()[0]
			rawReview['price'] = review.css('td:nth-child(4)').extract()[0]

			location = review.css('div.collapse .paragraph').extract()[0]
			rawReview['country'] = location
			rawReview['region'] = location

			processedReview = self.cleanTableReview(rawReview)
			processedReviews.append(processedReview)
		return processedReviews

	def cleanPageReview(self, rawReview):
		return {
			'name': rawReview['name'].replace('<h4>', '').replace('</h4>', '')[:-5],
			'winery': re.search(r'">([^<]*)', rawReview['winery']).groups()[0],
			'review': re.search(r'\t([^\t]*)<', rawReview['review']).groups()[0].strip(),
			'vintage': rawReview['vintage'].replace('<h4>', '').replace('</h4>', '')[-4:],
			'score': re.search(r'Score: ([^<]*)', rawReview['score']).groups()[0],
			'price': re.search(r'<\/strong>([^<]*)', rawReview['price']).groups()[0][1:],
			'country': re.search(r'<\/strong>([^<]*)', rawReview['country']).groups()[0][1:],
			'region': re.search(r'<\/strong>([^<]*)', rawReview['region']).groups()[0][1:]
		}

	def parseReviewPage(self, container):
		paragraphs = container.css('div.paragraph').extract()
		rawReview = {
			'name': container.css('h4').extract()[0],
			'winery': container.css('h1 a').extract()[0],
			'review': container.css('#bt-body').extract()[0],
			'vintage': container.css('h4').extract()[0],
			'score': container.css('h5').extract()[0],
			'price': paragraphs[0],
			'country': paragraphs[1],
			'region': paragraphs[2]
		}
		processedReview = self.cleanPageReview(rawReview)
		return processedReview






