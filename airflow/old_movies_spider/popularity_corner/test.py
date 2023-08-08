import unittest
from scrapy.utils.test import get_crawler

import sys
import os

# Add the parent directory of popularity_corner to the Python path
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from popularity_corner.spiders.budget_spider_imdb2 import MoviesBudget
from scrapy.http import TextResponse


class TestMoviesBudgetSpider(unittest.TestCase):

    def setUp(self):
        self.crawler = get_crawler(MoviesBudget)
        self.spider = self.crawler.spidercls()

    def test_parse_item(self):
        # Example HTML response for testing
        example_html_response = """
            <html>
                <body>
                    <div class="sc-afe43def-1">Movie Title</div>
                    <div class="sc-bde20123-1">8.0</div>
                    <div class="ipc-chip__text">Action</div>
                    <ul class="sc-afe43def-4">
                        <li><a>2000</a></li>
                        <li><a>All</a></li>
                    </ul>
                    <ul class="ipc-inline-list">
                        <li class="ipc-inline-list__item">2h 30m</li>
                        <li class="ipc-inline-list__item">2h 30m</li>
                        <li class="ipc-inline-list__item">2h 30m</li>
                    </ul>
                    <a class="sc-bfec09a1-1">Actor 1</a>
                    <a class="sc-bfec09a1-1">Actor 2</a>
                    <a class="sc-bfec09a1-1">Actor 3</a>
                    <ul data-testid="title-details-origin">
                        <a>USA</a>
                    </ul>
                    <li class="ipc-metadata-list__item" data-testid="title-boxoffice-budget">
                        <span class="ipc-metadata-list-item__list-content-item">$100 million</span>
                    </li>
                </body>
            </html>
        """

        # Simulate the spider handling the response
        encoding = 'utf-8'  # Assuming the encoding is utf-8, change if necessary
        response = TextResponse(url='http://example.com', body=example_html_response.encode(encoding), encoding=encoding)
        results = list(self.spider.parse_item(response))

        # Verify the results
        expected_result = {
            'Title': 'Movie Title',
            'Score': '8.0',
            'Genre': 'Action',
            'Année': '2000',
            'Durée': '150m',
            'Acteurs': ['Actor 1', 'Actor 2', 'Actor 3'],
            'Public': 'All',
            'Pays': 'USA',
            'Budget': '$100 million'
        }
        self.assertEqual(results, [expected_result])

if __name__ == '__main__':
    unittest.main()

