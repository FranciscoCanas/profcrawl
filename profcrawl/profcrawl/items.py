from scrapy.contrib.loader.processor import TakeFirst
from scrapy.item import Item, Field

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


class Prof(Item):
    name = Field(output_processor=TakeFirst())
    dept = Field(output_processor=TakeFirst())
    ratings = Field(output_processor=TakeFirst())
    avg = Field(output_processor=TakeFirst())
    easy = Field(output_processor=TakeFirst())
    hot = Field(output_processor=TakeFirst())
