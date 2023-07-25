import scrapy

class BoxOfficeSpider(scrapy.Spider):
    name = 'box_office'
    allowed_domains = ['allocine.fr']
    start_urls = ['https://www.allocine.fr/films/box-office/']

    def parse(self, response):
        films = response.xpath('//div[@class="film"]')
        for film in films:
            title = film.xpath('//h2//a/text()').get()
            date = film.xpath('//span[@class="date"]/text()').get()
            entries = film.xpath('//span[@class="entries"]/text()').get()

            yield {
                'title': title,
                'date': date,
                'entries': entries,
            }

        next_page_url = response.xpath('//a[@class="next"]/@href').get()
        if next_page_url is not None:
            yield scrapy.Request(next_page_url, callback=self.parse)
