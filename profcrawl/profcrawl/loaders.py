import nltk
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose

__author__ = 'fcanas'

class ProfLoader(ItemLoader):
    default_input_processor = MapCompose(nltk.clean_html)
