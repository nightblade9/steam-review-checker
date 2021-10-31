#!/bin/python3
from fetchers.game_fetcher import GameFetcher
import json
from fetchers.steam_fetcher import SteamFetcher
import time
import urllib.parse
import urllib.request

class ReviewFetcher(SteamFetcher):

    # Sort by newest-first, up to the max (100 per page). See: https://partner.steamgames.com/doc/store/getreviews
    # language=all: ALL languages, not just English/default
    # purchase_type=all: ALL reviews, paid (buyers) and non-paid (free key, etc.)
    _STEAM_REVIEWS_URL = "https://store.steampowered.com/appreviews/{}?json=1&filter=recent&purchase_type=all&language=all&num_per_page=100&cursor={}"
    
    # Metadata is a dictionary of app_id => data
    def get_reviews(self, metadata):
        config_json = self._read_config_json()
        app_ids = config_json["appIds"]
        all_reviews = []

        for app_id in app_ids:
            game_reviews = []
            game_name = metadata[app_id]["game_name"]

            # Fetch the first page, specifying a cursor; if we get 100 reviews back
            # (the max requested), then request the next page, until we don't get 100.

            cursor = "*" # first/default cursor
            data = _get_steam_reviews(app_id, cursor)
            game_reviews.extend(data["reviews"])
            cursor = urllib.parse.quote_plus(data["cursor"])

            # More than one page of reviews!
            while len(data["reviews"]) == 100:
                data = _get_steam_reviews(app_id, cursor)
                game_reviews.extend(data["reviews"])
                cursor = urllib.parse.quote_plus(data["cursor"])
            
            print("Fetched {} reviews for {}".format(len(game_reviews), game_name))
        
            game_reviews = _process_reviews(game_reviews, app_id, game_name)
            all_reviews.extend(game_reviews)
        
        # Sort by time descending, order of games isn't important
        all_reviews.sort(key=lambda x: x["timestamp_created"], reverse=True)

        return all_reviews

def _get_steam_reviews(app_id, cursor):
    # Call the API for each app and get reviews
    url = ReviewFetcher._STEAM_REVIEWS_URL.format(app_id, cursor)
    response = urllib.request.urlopen(url).read()
    json_response = json.loads(response.decode('utf-8'))

    if json_response["success"] != 1:
        print("Error: failed to fetch API for app {}; response was: success={})".format(app_id, json_response["success"]))
    
    return {"reviews": json_response["reviews"], "cursor": json_response["cursor"]}

def _process_reviews(reviews, app_id, game_name):
    all_reviews = []
    # Amend import data ...
    # TODO: fetch/amend title
    for review in reviews:
        # Amend data
        review["app_id"] = app_id
        elapsed_seconds = time.time() - review["timestamp_created"]
        days_ago = round(elapsed_seconds / (60 * 60 * 24))
        review["days_ago"] = days_ago
        review["game_name"] = game_name
        review["url"] = GameFetcher._STEAM_APP_URL.format(app_id)
        review["paid_review"] = not review["received_for_free"]

        all_reviews.append(review)
    
    return all_reviews