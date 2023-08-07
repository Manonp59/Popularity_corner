import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_fake_useragent.middleware import RandomUserAgentMiddleware
from ..items import IncomingMovieItem
from .utils import clean_date, clean_views, list_to_str
from datetime import date, datetime
from ..pipelines import AzureSqlPipeline


class AllocineSpider(CrawlSpider):
    name = 'incomingmovies'
    allowed_domains = ['allocine.fr']
    start_urls = ['https://www.allocine.fr/film/agenda/']


    custom_settings = {
            'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        },
        'ITEM_PIPELINES': {
            'incoming_movies_spider.pipelines.AzureSqlPipeline': 300,
        }
    }

    rules = (
        Rule(LinkExtractor(restrict_css=".meta-title-link"), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        release_date = clean_date(response.css('.date::text').extract())
        if release_date >= date.today():
            original_title = response.css("div.meta-body-item:nth-of-type(5)::text").extract()
            genres = response.css('div.meta-body-item.meta-body-info span::text').getall()
            evaluations = response.css("div.rating-item-content span.stareval-note::text").extract()
            if not evaluations:
                evaluations = [None, None]

            if original_title:
                final_title = original_title[1][1:-1]
            else:
                final_title = response.css('.titlebar-title-lg::text').extract()[0]
            genres=[genre.strip() for genre in genres[3:]],
            genres = list_to_str(genres)

            director=list(set(response.css(".meta-body-direction span.blue-link::text").extract())),
            director = list_to_str(director)
            
            cast = response.css(".meta-body-actor span::text").extract()[1:]
            cast = list_to_str(cast)

            item = IncomingMovieItem(
                release_date=clean_date(response.css('.date::text').extract()),
                title=final_title,
                genres = genres,
                director = director,
                cast = cast,
                duration=response.css(".meta-body-item.meta-body-info::text").extract()[3].replace('\n', ''),
                views=clean_views(response.css("div.meta-sub.light > span::text").extract()),
                nationality=response.css('span.nationality::text').get().strip(),
                distributor=response.css('span.that.blue-link::text').get().strip() if response.css('span.that.blue-link::text').get() else None,
                image_url = response.css('.thumbnail img::attr(src)').get(),
            )

            if all(item.values()):
                yield item
            else:
                self.logger.warning("Skipping item with missing data: %s", item)
