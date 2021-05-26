import datetime
import unittest

from fetchers import discussion_fetcher
from fetchers.discussion_fetcher import DiscussionFetcher

class TestDicussionFetcher(unittest.TestCase):

    def test_parse_date_converts_empty_string_to_nw(self):
        for test_case in ['', '          ']:
            actual = discussion_fetcher.parse_date(test_case)
            self.assertAlmostEqual(actual, datetime.datetime.now(), datetime.timedelta(seconds=1))