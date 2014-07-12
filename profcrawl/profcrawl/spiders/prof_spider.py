from scrapy.selector import Selector
from scrapy.spider import Spider
from scrapy.http.request import Request
from ..loaders import ProfLoader
from ..items import Prof

__author__ = 'fcanas'

class ProfQuerySpider(Spider):
    prof_query = 'div[class~="vertical-center"]'

    queries = {
        'name': 'div[class="profName"] > a::text',
        'dept': 'div[class="profDept"]::text',
        'ratings': 'div[class="profRatings"]::text',
        'avg': 'div[class="profAvg"]::text',
        'easy': 'div[class="profEasy"]::text',
        'hot': 'div[class="profHot notHot"]::text',
        'url': 'div[class="profName"] > a::attr(href)'
    }

    url_base = "http://ratemyprofessors.com/"
    name = "query.profs"
    allowed_domains = ["ratemyprofessors.com"]
    start_urls = ["http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=All&sid=1484"]

    def parse(self, response):
        """
        Parse initial search query page.
        """
        sel = Selector(response)
        next_page = sel.xpath('//a[@id="next"]/@href').extract()
        print next_page
        # if next_page:
        #     yield Request(self.url_base + next_page[0], self.parse)

        self.profs = self.parse_profs(response)

        for prof in self.profs:
            yield prof


    def parse_profs(self, response):
        """
        Parse all of the profs in the response.
        """
        prof_list = []
        sel = Selector(response)
        profs = sel.css(self.prof_query)
        for prof in profs:
            url = self.url_base + prof.css(self.queries['url']).extract()[0]
            loader = ProfLoader(item=Prof(), selector = prof, response=response)
            for key, value in self.queries.items():
                loader.add_css(key, value)
            prof_list.append(loader.load_item())
            yield Request(url, meta={'item':prof}, callback=self.parse_prof_record)


    def parse_prof_record(self, response):
        """
        Parse an individual prof's record.
        """
        pass