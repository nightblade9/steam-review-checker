import datetime
import os
import unittest

from fetchers import discussion_fetcher

class TestDicussionFetcher(unittest.TestCase):

    _MAX_DISCUSSIONS_PER_PAGE = 50 # use proper pagination please

    def test_parse_date_converts_empty_string_to_now(self):
        for test_case in ['', '          ']:
            actual = discussion_fetcher._parse_date(test_case)
            now = datetime.datetime.now()
            self.assertEqual(actual.year, now.year)
            self.assertEqual(actual.month, now.month)
            self.assertEqual(actual.day, now.day)
            self.assertEqual(actual.hour, now.hour)
            self.assertEqual(actual.min, now.min)
    
    def test_parse_date_converts_just_now_to_now(self):
        for test_case in ["just NOW", "Just now", "JuSt NoW"]:
            actual = discussion_fetcher._parse_date(test_case)
            now = datetime.datetime.now()
            self.assertEqual(actual.year, now.year)
            self.assertEqual(actual.month, now.month)
            self.assertEqual(actual.day, now.day)
            self.assertEqual(actual.hour, now.hour)
            self.assertEqual(actual.min, now.min)

    def test_parse_date_converts_minutes_ago_to_now_with_delta(self):
        for test_case in [8, 38, 1, 59]:
            actual = discussion_fetcher._parse_date("{} minutes ago".format(test_case))
            expected = datetime.datetime.now() + datetime.timedelta(minutes = test_case)
            self.assertEqual(actual.year, expected.year)
            self.assertEqual(actual.month, expected.month)
            self.assertEqual(actual.day, expected.day)
            self.assertTrue(actual.hour == expected.hour or actual.hour == expected.hour + 1)
            self.assertEqual(actual.min, expected.min)
    
    def test_parse_date_converts_hours_ago_to_now_with_delta(self):
        for test_case in [17, 6, 1, 23]:
            actual = discussion_fetcher._parse_date("{} hours ago".format(test_case))
            expected = datetime.datetime.now() + datetime.timedelta(hours = test_case)
            self.assertEqual(actual.year, expected.year)
            self.assertEqual(actual.month, expected.month)
            self.assertTrue(actual.day == expected.day or actual.day == expected.day + 1)
            # Hour is too tricky to assert with rollover
            self.assertEqual(actual.min, expected.min)

    def test_parse_date_converts_yearless_dates_to_current_year(self):
        for data in ["May 29", "Jan 1", "Dec 31", "Feb 28", "Aug 17"]:
            test_case = "{} @ 9:00am".format(data)
            expected = datetime.datetime.strptime(test_case, "%b %d @ %I:%M%p")
            actual = discussion_fetcher._parse_date(test_case)
            self.assertEqual(actual.year, datetime.datetime.now().year)
            self.assertEqual(actual.month, expected.month),
            self.assertEqual(actual.day, expected.day, "Failed for {}: ex={} act={}".format(test_case, expected, actual))
    
    def test_parse_date_parses_date_with_year(self):
        for data in ["Jun 29, 2021", "Jan 1, 2002", "Dec 31, 1976", "Mar 16, 2015", "Oct 4, 2011"]:
            test_case = "{} @ 1:00am".format(data)
            expected = datetime.datetime.strptime(test_case, "%b %d, %Y @ %I:%M%p")
            actual = discussion_fetcher._parse_date(test_case)
            self.assertEqual(actual.year, expected.year)
            self.assertEqual(actual.month, expected.month, "Failed for {}: ex={} act={}".format(test_case, expected, actual))
            self.assertEqual(actual.day, expected.day)
    
    # For Oneons: detailed parsing for the first discussion; check ALL fields.
    def test_parse_discussions_can_parse_oneons_discussions(self):
        raw_html = ""
        app_id = 1342600
        
        with open(os.path.join("tests", "test_data", "steam_discussions", "2022", "{}.html".format(app_id)), 'r', encoding="utf-8") as file_handle:
            raw_html = file_handle.read()
        
        expected_discussions = 3
        actuals = discussion_fetcher._parse_discussions(raw_html, app_id, "Oneons", "General")

        self.assertEqual(expected_discussions, len(actuals))
        discussion = actuals[-1]
        self.assertEqual(app_id, discussion["app_id"])
        self.assertEqual("A few Suggestions", discussion["title"])
        self.assertEqual("Benjo Kabobble", discussion["author"])
        self.assertEqual("https://steamcommunity.com/app/1342600/discussions/0/2646378342121880438/", discussion["url"])
        self.assertEqual(2, int(discussion["num_replies"]))
        self.assertEqual("Oneons", discussion["game_name"])
    
    # Make sure we get "📌 <title>" discussions correctly, via Feudal Kingdoms
    def test_parse_discussions_gets_emoji_title_for_pinned_discussions(self):
        # Arrange
        raw_html = ""
        app_id = 1349900
        
        for data_directory in [2020, 2021]:
            with open(os.path.join("tests", "test_data", "steam_discussions", str(data_directory), "{}.html".format(app_id)), 'r', encoding="utf-8") as file_handle:
                raw_html = file_handle.read()
            
            # Act
            actual = discussion_fetcher._parse_discussions(raw_html, app_id, "Feudal Kingdoms", "General")

            # Assert
            expected_titles = [
                "📌 Feudal Kingdoms Early Access Release postponed",
                "📌 Feedback",
                "📌 Bugs",
                "📌 Support",
                "Dead",
                "game delayed"
            ]

            self.assertEqual(len(expected_titles), len(actual))

            for i in range(len(expected_titles)):
                expected_title = expected_titles[i]
                actual_discussion = actual[i]
                self.assertEqual(expected_title, actual_discussion["title"])

    def test_parse_discussions_can_parse_pinned_broken_html(self):
        # October 2022: discussion parsing started failing for a pinned post in a subforum
        # Arrange
        raw_html = ""
        app_id = 1858760
        
        with open(os.path.join("tests", "test_data", "steam_discussions", "2022", "{}.html".format(app_id)), 'r', encoding="utf-8") as file_handle:
            raw_html = file_handle.read()
        
        # Act
        actual = discussion_fetcher._parse_discussions(raw_html, app_id, "Gem Worlds", "General Discussions")
        actual_titles = [x["title"] for x in actual]

        # Assert
        expected_titles = [
            "📌 Post demo feedback in the Demo Feedback sub-group!",
            "📌 We're on Discord!"
        ]

        self.assertEqual(len(expected_titles), len(actual))

        for i in range(len(expected_titles)):
            expected_title = expected_titles[i]
            actual_discussion = actual[i]
            self.assertEqual(expected_title, actual_discussion["title"])

    # Make sure we get "✅ <title>" discussions answered, via Frankenstorm TD
    def test_parse_discussions_gets_emoji_title_for_answered_discussions(self):
        # Arrange
        raw_html = ""
        app_id = 1672920
        
        with open(os.path.join("tests", "test_data", "steam_discussions", "2022", "{}.html".format(app_id)), 'r', encoding="utf-8") as file_handle:
            raw_html = file_handle.read()
        
        # Act
        actual = discussion_fetcher._parse_discussions(raw_html, app_id, "Frankenstorm TD", "General")
        actual_titles = [x["title"] for x in actual]

        # Assert
        expected_titles = [
            "✅ Enemy Wave health debuffs stack additively or multiplicatively?",
            "✅ Additional spawns add to total hp pool or not?"
        ]

        for i in range(len(expected_titles)):
            expected_title = expected_titles[i]
            self.assertIn(expected_title, actual_titles, "Didn't see %s in actual titles: %s".format(expected_title, actual_titles))


    # Discussions with an award have the date in a different place.    
    def test_parse_discussions_gets_date_for_awarded_discussions(self):
        # Arrange
        raw_html = ""
        app_id = 1057990
        
        with open(os.path.join("tests", "test_data", "steam_discussions", "2022", "{}.html".format(app_id)), 'r', encoding="utf-8") as file_handle:
            raw_html = file_handle.read()
        
        # Act
        actual = discussion_fetcher._parse_discussions(raw_html, app_id, "Viking Trickshot", "Events and Announcements")

        # Assert
        now = datetime.datetime.now() 

        for i in range(len(actual)):
            actual_discussion = actual[i]
            raw_date = actual_discussion["date"]
            # If parsing failed, the date would be "0 days ago."
            # Since the discussions all predate 2022, it's easy enough to check the year.
            self.assertTrue("2021" in raw_date or "2020" in raw_date or "2019" in raw_date)

    # For other games: discussion count is sufficient.
    def test_parse_discussions_can_parse_up_to_max_discussions(self):
        test_cases = {
            "2020": [
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
                    "expected": 15 # max used when we grabbed this file
                },
                {
                    # BioMutant: page 1 ("8 minutes ago" and "Just now")
                    "game_name": "BioMutant Page 1",
                    "app_id": "597820-page1",
                    "expected": 15 # max used when we grabbed this file
                },
                {
                    "game_name": "BioMutant Last Page",
                    "app_id": "597820-page31",
                    "expected": 15 # max used when we grabbed this file
                }
            ],
            "2021": [
                {
                    "game_name": "Clam Man",
                    "app_id": 1000640,
                    "expected": 12
                },
                {
                    "game_name": "Pixelot",
                    "app_id": 1512860,
                    "expected": 13
                },
                {
                    "game_name": "Cursed: Gems 2",
                    "app_id": 643960,
                    "expected": TestDicussionFetcher._MAX_DISCUSSIONS_PER_PAGE # max
                },
                {
                    # BioMutant: page 1 ("8 minutes ago" and "Just now")
                    "game_name": "BioMutant Page 1",
                    "app_id": "597820-page1",
                    "expected": TestDicussionFetcher._MAX_DISCUSSIONS_PER_PAGE # max
                },
                {
                    "game_name": "BioMutant Last Page",
                    "app_id": "597820-lastpage",
                    "expected": 26
                }
            ],
            "2022": [
                {
                    # Page one had a title that was 11 nodes instead of 7-9, idk why.
                    "game_name": "Viking Trickshot",
                    "app_id": 1057990,
                    "expected": 10
                }
            ]
        }

        for data_directory in test_cases.keys():
            for data in test_cases[data_directory]:
                raw_html = ""
                app_id = data["app_id"]
                expected = data["expected"]
                
                with open(os.path.join("tests", "test_data", "steam_discussions", data_directory, "{}.html".format(app_id)), 'r', encoding="utf-8") as file_handle:
                    raw_html = file_handle.read()
                
                actual = discussion_fetcher._parse_discussions(raw_html, app_id, "Title goes here", "Category goes here")

                self.assertEqual(expected, len(actual), "Failed with {} data on {}".format(data_directory, app_id)) # maxes out at 15 discussions