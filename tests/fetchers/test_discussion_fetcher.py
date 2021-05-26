import datetime
import os
import unittest

from fetchers import discussion_fetcher

class TestDicussionFetcher(unittest.TestCase):

    def test_parse_date_converts_empty_string_to_now(self):
        for test_case in ['', '          ']:
            actual = discussion_fetcher._parse_date(test_case)
            self.assertAlmostEqual(actual, datetime.datetime.now(), datetime.timedelta(seconds=1))
    
    def test_parse_date_converts_just_now_to_now(self):
        for test_case in ["just NOW", "Just now", "JuSt NoW"]:
            actual = discussion_fetcher._parse_date(test_case)
            self.assertAlmostEqual(actual, datetime.datetime.now(), datetime.timedelta(seconds=1))

    def test_parse_date_converts_minutes_ago_to_now_with_delta(self):
        for test_case in [8, 38, 1, 59]:
            actual = discussion_fetcher._parse_date("{} minutes ago".format(test_case))
            self.assertAlmostEqual(actual, datetime.datetime.now() + datetime.timedelta(minutes=test_case), datetime.timedelta(seconds=1))
    
    def test_parse_date_converts_hours_ago_to_now_with_delta(self):
        for test_case in [17, 6, 1, 23]:
            actual = discussion_fetcher._parse_date("{} hours ago".format(test_case))
            self.assertAlmostEqual(actual, datetime.datetime.now() + datetime.timedelta(hours=test_case), datetime.timedelta(seconds=1))

    def test_parse_date_converts_yearless_dates_to_current_year(self):
        for test_case in ["29 May", "1 Jan", "31 Dec", "28 Feb", "17 Aug"]:
            expected = datetime.datetime.strptime(test_case, "%d %b")
            actual = discussion_fetcher._parse_date("{} @ 1:23PM".format(test_case))
            self.assertEqual(actual.year, datetime.datetime.now().year)
            self.assertEqual(actual.month, expected.month),
            self.assertEqual(actual.day, expected.day, "Failed for {}: ex={} act={}".format(test_case, expected, actual))
    
    def test_parse_date_parses_date_with_year(self):
        for test_case in ["29 Jun, 2021", "1 Jan, 2002", "31 Dec, 1976", "16 Mar, 2015", "4 Oct, 2011"]:
            expected = datetime.datetime.strptime(test_case, "%d %b, %Y")
            actual = discussion_fetcher._parse_date("{} @ 11:59pm".format(test_case))
            self.assertEqual(actual.year, expected.year)
            self.assertEqual(actual.month, expected.month, "Failed for {}: ex={} act={}".format(test_case, expected, actual))
            self.assertEqual(actual.day, expected.day)
    
    # For Oneons: detailed parsing since it's just one discussion, check ALL fields.
    def test_parse_discussions_can_parse_oneons_discussions(self):
        raw_html = ""
        app_id = 1342600
        
        with open(os.path.join("tests", "test_data", "steam_discussions", "{}.html".format(app_id)), 'r', encoding="utf-8") as file_handle:
            raw_html = file_handle.read()
        
        actual = discussion_fetcher._parse_discussions(raw_html, app_id, "Oneons")

        self.assertEqual(1, len(actual))
        discussion = actual[0]
        self.assertEqual(app_id, discussion["app_id"])
        self.assertEqual("A few Suggestions", discussion["title"])
        self.assertEqual("Benjo Bobbington", discussion["author"])
        self.assertEqual("https://steamcommunity.com/app/1342600/discussions/0/2646378342121880438/", discussion["url"])
        self.assertEqual(2, int(discussion["num_replies"]))
        self.assertEqual("Oneons", discussion["game_name"])
    
    # For other games: discussion count is sufficient.
    def test_parse_discussions_can_parse_up_to_15_discussions(self):
        test_cases = [
            {
                "game_name": "Clam Man",
                "app_id": 1000640,
                "expected": 11
            },
            {
                "game_name": "Pixelot",
                "app_id": 1512860,
                "expected": 12
            },
            {
                "game_name": "Cursed: Gems 2",
                "app_id": 643960,
                "expected": 15 # max
            },
            {
                # BioMutant: page 1 ("8 minutes ago" and "Just now")
                "game_name": "BioMutant Page 1",
                "app_id": "597820-page1",
                "expected": 15 # max
            },
            {
                # BioMutant: page 1 ("23 hours ago" and "May 25")
                "game_name": "BioMutant Page 31",
                "app_id": "597820-page31",
                "expected": 15 # max
            }
        ]

        for data in test_cases:
            raw_html = ""
            app_id = data["app_id"]
            expected = data["expected"]
            
            with open(os.path.join("tests", "test_data", "steam_discussions", "{}.html".format(app_id)), 'r', encoding="utf-8") as file_handle:
                raw_html = file_handle.read()
            
            actual = discussion_fetcher._parse_discussions(raw_html, app_id, "Title goes here")

            self.assertEqual(expected, len(actual), "BURN {}".format(app_id)) # maxes out at 15 discussions