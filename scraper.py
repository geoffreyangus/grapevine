from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import Rule

class WineSpider(InitSpider):
    name = 'wine'
    allowed_domains = ['winespectator.com']
    login_page = 'https://www.winespectator.com/auth/login'
    start_urls = ['http://www.winespectator.com/wine/search?submitted=Y&page=1&text_search_flag=winery&search_by=exact&winery=G.+Bartet']

    def init_request(self):
    	print '=============INITIALIZING==============='
        """This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        """Generate a login request."""
        return FormRequest.from_response(response,
                    formdata={'userid': 'gdlangus@gmail.com', 'passwd': 'cs22wine'},
                    callback=self.check_login_response)

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        if "Welcome, Geoffrey Angus" in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            # Now the crawling can begin..
            return self.initialized()
        else:
            self.log("Bad times :(")
            # Something went wrong, we couldn't log in, so nothing happens.

    def parse(self, response):
    	page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)