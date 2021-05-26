import datetime
import unittest

from fetchers import game_fetcher

class TestGameFetcher(unittest.TestCase):

    def test_parse_title_parses_title(self):
        html = "<html><head><title>Oneons on Steam</title><script type='text/javascript'>alert('!')</script></head><body><p>hi!</p></body></html>"
        actual = game_fetcher._parse_title(html)
        self.assertEqual("Oneons", actual)