#!/bin/python3
import json
import os
import time
import urllib.request

class Main:
    _CONFIG_JSON_FILENAME = "config.json"
    _LAST_SEEN_FILE = "last_seen_timestamp.txt"
    _STEAM_APP_URL = "https://store.steampowered.com/app/" # append app_id

    # Sort by newest-first, up to the max (100 per page). See: https://partner.steamgames.com/doc/store/getreviews
    _STEAM_BASE_URL = "https://store.steampowered.com/appreviews/{}?json=1&filter=recent&num_per_page=100"
    

    def main(self):
        new_reviews = []

        config_json = self._read_config_json()
        app_ids = config_json["appIds"]
        last_timestamp = self._get_last_review_time()

        for app_id in app_ids:
            reviews = self._get_app_reviews(app_id)
            for review in reviews:
                if review["timestamp_created"] >= last_timestamp:
                    new_reviews.append(review)
                    review["app_id"] = app_id

        if len(new_reviews) == 0:
            print("No new reviews, sorry.")
            return
        
        print("***** {} new reviews! ****".format(len(new_reviews)))
        previous_app_id = 0

        for i in range(len(new_reviews)):
            review = new_reviews[i]
            if review["app_id"] != previous_app_id:
                print("================ For app #{}: {}/{} ================".format(app_id, Main._STEAM_APP_URL, app_id))
                previous_app_id = review["app_id"]
                review_number = 1
            else:
                review_number += 1
            
            # Pretty-print, e.g. 3 days ago
            review_date = review["timestamp_created"]
            elapsed_seconds = time.time() - review_date
            days_ago = round(elapsed_seconds / (60 * 60 * 24))

            print("[Review #{} ({} days ago)]: {}\n--------------------".format(review_number, days_ago, review["review"]))

        self._write_current_time()

    def _read_config_json(self):
        config_json = ""
        with open(Main._CONFIG_JSON_FILENAME) as file_handle:
            config_json = file_handle.read()
        config = json.loads(config_json)
        return config
    
    def _get_last_review_time(self):
        # Check when's the last time we looked at reviews
        last_timestamp = 0
        if os.path.isfile(Main._LAST_SEEN_FILE):
            with open(Main._LAST_SEEN_FILE, 'r') as file_handle:
                last_timestamp = float(file_handle.read())
                print("Read last timestamp {}".format(last_timestamp))

        return last_timestamp

    def _write_current_time(self):
        # Write current time so we get newer reviews next time we run
        with open(Main._LAST_SEEN_FILE, 'w') as file_handle:
            file_handle.write(str(time.time()))
        
    def _get_app_reviews(self, app_id):
        # Call the API for each app and get reviews
        url = Main._STEAM_BASE_URL.format(app_id)
        response = urllib.request.urlopen(url).read()
        json_response = json.loads(response.decode('utf-8'))

        if json_response["success"] != 1:
            print("Error: failed to fetch API for app {}; response was: success={})".format(app_id, json_response["success"]))
        
        return json_response["reviews"]

Main().main()