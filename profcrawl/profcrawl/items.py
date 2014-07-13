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
    url = Field(output_processor=TakeFirst())

class Rating(Item):
    date = Field(output_processor=TakeFirst())
    course = Field(output_processor=TakeFirst())
    comment = Field(output_processor=TakeFirst())
    quality = Field(output_processor=TakeFirst())
    easiness = Field(output_processor=TakeFirst())
    helpfulness = Field(output_processor=TakeFirst())
    clarity = Field(output_processor=TakeFirst())
    interest = Field(output_processor=TakeFirst())
    grade = Field(output_processor=TakeFirst())
