#!/bin/python3
import json
import urllib.request
import time

class DataFetcher:
    _CONFIG_JSON_FILENAME = "config.json"

    # Not used, use it to get the app title
    _STEAM_APP_URL = "https://store.steampowered.com/app/" # append app_id

    # Sort by newest-first, up to the max (100 per page). See: https://partner.steamgames.com/doc/store/getreviews
    _STEAM_BASE_URL = "https://store.steampowered.com/appreviews/{}?json=1&filter=recent&num_per_page=100"
    
    def get_reviews(self):
        config_json = self._read_config_json()
        app_ids = config_json["appIds"]
        all_reviews = []

        for app_id in app_ids:
            reviews = self._get_steam_reviews(app_id)
            # Amend import data ...
            # TODO: fetch/amend title
            for review in reviews:
                review["app_id"] = app_id
                elapsed_seconds = time.time() - review["timestamp_created"]
                days_ago = round(elapsed_seconds / (60 * 60 * 24))
                review["days_ago"] = days_ago
                all_reviews.append(review)
        
        return all_reviews

    def _read_config_json(self):
        config_json = ""
        with open(DataFetcher._CONFIG_JSON_FILENAME) as file_handle:
            config_json = file_handle.read()
        config = json.loads(config_json)
        return config
    
    def _get_steam_reviews(self, app_id):
        # Call the API for each app and get reviews
        url = DataFetcher._STEAM_BASE_URL.format(app_id)
        response = urllib.request.urlopen(url).read()
        json_response = json.loads(response.decode('utf-8'))

        if json_response["success"] != 1:
            print("Error: failed to fetch API for app {}; response was: success={})".format(app_id, json_response["success"]))
        
        return json_response["reviews"]
