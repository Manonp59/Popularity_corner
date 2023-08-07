import unittest
from scrapy.http import HtmlResponse
from unittest.mock import patch
from incoming_movies_spider.spiders.incoming_movies_scrap import AllocineSpider  # Assurez-vous d'importer correctement votre spider
from incoming_movies_spider.items import IncomingMovieItem

class TestIncomingMoviesSpider(unittest.TestCase):

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='<html><body>...</body></html>')
    @patch('scrapy.http.HtmlResponse', side_effect=HtmlResponse)
    def test_parse_movie(self, mock_response, mock_open):
        spider = AllocineSpider()
        url = 'http://example.com/movie'
        
        # Appel de la méthode de parsing et vérification du résultat
        parsed_item = next(spider.parse_item(mock_response(url=url)))
        
        # Assertions pour la structure IncomingMovieItem correspondant à la table de base de données
        self.assertIsInstance(parsed_item, IncomingMovieItem)
        self.assertIn('title', parsed_item)
        self.assertIsInstance(parsed_item['title'], str)
        
        self.assertIn('release_date', parsed_item)
        self.assertIsInstance(parsed_item['release_date'], str)
        
        self.assertIn('genres', parsed_item)
        self.assertIsInstance(parsed_item['genres'], str)
        
        self.assertIn('director', parsed_item)
        self.assertIsInstance(parsed_item['director'], str)
        
        self.assertIn('cast', parsed_item)
        self.assertIsInstance(parsed_item['cast'], str)
        
        self.assertIn('duration', parsed_item)
        self.assertIsInstance(parsed_item['duration'], str)
        
        self.assertIn('views', parsed_item)
        self.assertIsInstance(parsed_item['views'], int)
        
        self.assertIn('nationality', parsed_item)
        self.assertIsInstance(parsed_item['nationality'], str)
        
        self.assertIn('distributor', parsed_item)
        self.assertIsInstance(parsed_item['distributor'], str)
        
        self.assertIn('prediction', parsed_item)
        self.assertIsInstance(parsed_item['prediction'], float)
        
        self.assertIn('prediction_cinema', parsed_item)
        self.assertIsInstance(parsed_item['prediction_cinema'], float)
        
        self.assertIn('image_url', parsed_item)
        self.assertIsInstance(parsed_item['image_url'], str)

if __name__ == '__main__':
    unittest.main()
