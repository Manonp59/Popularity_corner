# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IncomingMovieItem(scrapy.Item):
    title = scrapy.Field()
    release_date = scrapy.Field()
    genres = scrapy.Field()
    director = scrapy.Field()
    main_actors = scrapy.Field()
    viewers_eval = scrapy.Field()
    press_eval = scrapy.Field()
    duration = scrapy.Field()
    views = scrapy.Field()
    nationality = scrapy.Field()
    distributor = scrapy.Field()