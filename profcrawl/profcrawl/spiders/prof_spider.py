from scrapy.selector import Selector
from scrapy.spider import Spider
from scrapy.http.request import Request
from ..loaders import ProfLoader, RatingLoader
from ..items import Prof, Rating

__author__ = 'fcanas'

class ProfQuerySpider(Spider):
    prof_query = 'div[class~="vertical-center"]'
    rating_query = 'div[id="ratingTable"] > div[class~="entry"]'

    queries = {
        'name': 'div[class="profName"] > a::text',
        'dept': 'div[class="profDept"]::text',
        'ratings': 'div[class="profRatings"]::text',
        'avg': 'div[class="profAvg"]::text',
        'easy': 'div[class="profEasy"]::text',
        'hot': 'div[class="profHot notHot"]::text',
        'url': 'div[class="profName"] > a::attr(href)'
    }

    rating_queries = {
        'date': 'div[class="date"]::text',
        'course': 'div[class="class"] > p::text',
        'comment': 'div[class="comment"] > p[class="commentText"]::text',
        'quality': 'div[class="rating"] > p[class*="Quality"]::text',
        'easiness': 'div[class="rating"] > p[class~="rEasy"] > span::text',
        'helpfulness': 'div[class="rating"] > p[class~="rHelpful"] > span::text',
        'clarity': 'div[class="rating"] > p[class~="rClarity"] > span::text',
        'interest': 'div[class="rating"] > p[class~="rInterest"] > span::text',
        'grade': 'div[class="rating"] > p[class~="rGrade"] > span::text'
    }

    url_base = "http://ratemyprofessors.com/"
    name = "query.profs"
    allowed_domains = []
    start_urls = []

    def __init__(self, query, *args, **kwargs):
        """
        Query: A file containing a domain and query to start scrape from.
        """
        self.init_query(query)
        super(ProfQuerySpider, self).__init__(*args, **kwargs)

    def init_query(self, path):
        """
        Given the path to a query file, obtain the domain and start_urls.
        """
        with open(path, 'r') as qfile:
            lines = qfile.readlines()
            self.allowed_domains = [lines[0].strip()]
            for line in lines[1:]:
                self.start_urls.append(line.strip())

    def parse(self, response):
        """
        Parse initial search query page.
        """
        sel = Selector(response)
        next_page = sel.xpath('//a[@id="next"]/@href').extract()
        print next_page
        if next_page:
            yield Request(self.url_base + next_page[0], self.parse)

        self.profs = self.parse_profs(response)

        for prof in self.profs:
            url = self.url_base + prof['url']
            yield Request(url, meta={'item':prof}, callback=self.parse_prof_record)


    def parse_profs(self, response):
        """
        Parse all of the profs in the response.
        """
        prof_list = []
        sel = Selector(response)
        profs = sel.css(self.prof_query)
        for prof in profs:
            loader = ProfLoader(item=Prof(), selector = prof, response=response)
            for key, value in self.queries.items():
                loader.add_css(key, value)
            prof_list.append(loader.load_item())
        return prof_list


    def parse_prof_record(self, response):
        """
        Parse an individual prof's record.
        """
        prof = response.request.meta['item']
        ratings = []
        sel = Selector(response)
        entries = sel.css(self.rating_query)
        for entry in entries:
            loader = RatingLoader(item=Rating(), selector = entry, response = response)
            for key, value in self.rating_queries.items():
                loader.add_css(key, value)
            ratings.append(loader.load_item())
        prof['ratings'] = ratings
        yield prof

