import os
import unittest

from fetchers import game_fetcher

class TestGameFetcher(unittest.TestCase):

    def test_parse_title_parses_title(self):
        # Arrange

        # This file is from when <title>Save 20% on Gem Worlds on Steam</title> was the title.
        # We use a better method of determining the title now.
        test_data_file = "1858760-sale"
        with open(os.path.join("tests", "test_data", "{}.html".format(test_data_file)), 'r', encoding="utf-8") as file_handle:
            raw_html = file_handle.read()

        # Act
        actual = game_fetcher._parse_title(raw_html)
        
        # Assert
        self.assertEqual("Gem Worlds", actual)