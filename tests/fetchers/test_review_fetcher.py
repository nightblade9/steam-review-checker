import json
import os
import unittest

from fetchers import review_fetcher

class TestDicussionFetcher(unittest.TestCase):
    
    # Review count is sufficient. This covers: non-English reviews, free-key-redeemed reviews, etc.
    # This also covers cursor parsing - I manually combined them into a single JSON blob
    def test_parse_reviews_gets_all_types_and_languages_of_reviews(self):
        test_cases = [
            {
                "game_name": "Clam Man",
                "app_id": 1000640,
                "expected": 100 # Yes, exactly 100.
            },
            {
                "game_name": "Pixelot",
                "app_id": 1512860,
                "expected": 17
            },
            {
                "game_name": "Oneons: Prisoners",
                "app_id": 1346200,
                "expected": 6
            },
            {
                "game_name": "Cursed: Gems 2",
                "app_id": 643960,
                "expected": 324 # 4 pages worth
            }
        ]

        saw_non_paid_review = False
        saw_non_english_review = False

        for data in test_cases:
            raw_reviews = []
            app_id = data["app_id"]
            expected = data["expected"]

            with open(os.path.join("tests", "test_data", "steam_reviews", "{}.json".format(app_id)), 'r', encoding="utf-8") as file_handle:
                raw_reviews = json.loads(file_handle.read())["reviews"]
            
            actual = review_fetcher._process_reviews(raw_reviews, app_id, data["game_name"])

            # Assert
            # No per-field parsing necessary, we're just consuming a  JSON API call, minimal processing
            self.assertEqual(expected, len(actual), "Failed for {}".format(app_id))

            first = actual[0]
            self.assertEqual(app_id, first["app_id"])
            self.assertEqual(data["game_name"], first["game_name"])

            for review in actual:
                if review["language"] != "english": saw_non_english_review = True
                if review["received_for_free"] == True: saw_non_paid_review = True
            
            self.assertTrue(saw_non_paid_review)
            self.assertTrue(saw_non_english_review)