import scrapy
from fake_useragent import UserAgent
from .

class BoxOfficeSpider(scrapy.Spider):
    name = "boxoffice"
    allowed_domains = ["allocine.fr"]
    start_urls = ["https://www.allocine.fr/top/bo/"]

    def parse(self, response):
        movies = response.xpath("//div[@class='box-office']/div/div")
        for movie in movies:
            item = BoxOfficeItem()
            item["title"] = movie.xpath(".//div[@class='movie-title']/a/text()").extract_first()
            item["date_release"] = movie.xpath(".//div[@class='movie-release-date']/text()").extract_first()
            item["entrance"] = movie.xpath(".//div[@class='movie-entrance']/text()").extract_first()
            yield item

    def start_requests(self):
        # Use fake user agent to avoid getting blocked
        user_agent = UserAgent()
        request = scrapy.Request(self.start_urls[0], headers={'User-Agent': user_agent.random})
        yield request
