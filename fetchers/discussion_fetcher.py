#!/bin/python3
import time
from fetchers.steam_fetcher import SteamFetcher

# Scrapes Steam's discussion forums to get you the latest greatest data.
class DiscussionFetcher(SteamFetcher):
    
    def get_discussions(self):
        config_json = self._read_config_json()
        app_ids = config_json["appIds"]
        all_reviews = []

        for app_id in app_ids:
            title = self._get_steam_game_title(app_id)
            reviews = self._get_steam_reviews(app_id)

            # Amend import data ...
            # TODO: fetch/amend title
            for review in reviews:
                # Amend data
                review["app_id"] = app_id
                review["title"] = title
                elapsed_seconds = time.time() - review["timestamp_created"]
                days_ago = round(elapsed_seconds / (60 * 60 * 24))
                review["days_ago"] = days_ago
                
                all_reviews.append(review)
        
        # Sort by time descending, order of games isn't important
        all_reviews.sort(key=lambda x: x["timestamp_created"], reverse=True)

        return all_reviews
