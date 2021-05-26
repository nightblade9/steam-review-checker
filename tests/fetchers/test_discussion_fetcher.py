import datetime
import unittest

from fetchers import discussion_fetcher
from fetchers.discussion_fetcher import DiscussionFetcher

class TestDicussionFetcher(unittest.TestCase):

    def test_parse_date_converts_empty_string_to_now(self):
        for test_case in ['', '          ']:
            actual = discussion_fetcher.parse_date(test_case)
            self.assertAlmostEqual(actual, datetime.datetime.now(), datetime.timedelta(seconds=1))
    
    def test_parse_date_converts_just_now_to_now(self):
        for test_case in ["just NOW", "Just now", "JuSt NoW"]:
            actual = discussion_fetcher.parse_date(test_case)
            self.assertAlmostEqual(actual, datetime.datetime.now(), datetime.timedelta(seconds=1))

    def test_parse_date_converts_minutes_ago_to_now_with_delta(self):
        for test_case in [8, 38, 1, 59]:
            actual = discussion_fetcher.parse_date("{} minutes ago".format(test_case))
            self.assertAlmostEqual(actual, datetime.datetime.now() + datetime.timedelta(minutes=test_case), datetime.timedelta(seconds=1))
    
    def test_parse_date_converts_hours_ago_to_now_with_delta(self):
        for test_case in [17, 6, 1, 23]:
            actual = discussion_fetcher.parse_date("{} hours ago".format(test_case))
            self.assertAlmostEqual(actual, datetime.datetime.now() + datetime.timedelta(hours=test_case), datetime.timedelta(seconds=1))

    def test_parse_date_converts_yearless_dates_to_current_year(self):
        for test_case in ["29 May", "1 Jan", "31 Dec", "28 Feb", "17 Aug"]:
            expected = datetime.datetime.strptime(test_case, "%d %b")
            actual = discussion_fetcher.parse_date("{} @ 1:23PM".format(test_case))
            self.assertEqual(actual.year, datetime.datetime.now().year)
            self.assertEqual(actual.month, expected.month),
            self.assertEqual(actual.day, expected.day)
    
    def test_parse_date_parses_date_with_year(self):
        for test_case in ["29 Jun, 2021", "1 Jan, 2002", "31 Dec, 1976", "16 Mar, 2015", "4 Oct, 2011"]:
            expected = datetime.datetime.strptime(test_case, "%d %b, %Y")
            actual = discussion_fetcher.parse_date("{} @ 11:59pm".format(test_case))
            self.assertEqual(actual.year, expected.year)
            self.assertEqual(actual.month, expected.month)
            self.assertEqual(actual.day, expected.day)