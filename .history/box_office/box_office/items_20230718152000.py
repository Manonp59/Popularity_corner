# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BoxOfficeItem(scrapy.Item):
    title = scrapy.Field()
    # date_release = scrapy.Field()
    # entrance = scrapy.Field()
    pass

class EntranceItem(scrapy.Item):
    date_release = scrapy.Field()
    entrance = scrapy.Field()
    pass
