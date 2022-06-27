import datetime
from fetchers.steam_fetcher import SteamFetcher
from fetchers.discussion_fetcher import DiscussionFetcher
from fetchers.game_fetcher import GameFetcher
from fetchers.review_fetcher import ReviewFetcher
import http.server
import json
import os
import socketserver
from threading import Thread
import time

REFRESH_INTERVAL_CONFIG_KEY = "refreshDataIntervalMinutes"
REFRESH_INTERVAL_DEFAULT_MINUTES = 60

ENABLE_PAGING_CONFIG_KEY = "enablePaging"

PORT = 8000
WEB_DIR = os.path.join(os.path.dirname(__file__), "web")
WEB_DATA_DIR = os.path.join(WEB_DIR, "data")

class WebHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

class Main:
    def main(self):
        # Start web server.  This nukes build/data, so we have to wait for it to finish.
        self._ensure_output_directory_exists()

        config = SteamFetcher()._read_config_json()

        refresh_minutes = REFRESH_INTERVAL_DEFAULT_MINUTES
        if REFRESH_INTERVAL_CONFIG_KEY in config:
            refresh_minutes = int(config[REFRESH_INTERVAL_CONFIG_KEY])
        
        enable_paging = True
        if ENABLE_PAGING_CONFIG_KEY in config:
            enable_paging = bool(config[ENABLE_PAGING_CONFIG_KEY])
            if not enable_paging:
                print("Paging of results is disabled; you will only see 50 discussions (per forum) and 100 reviews per game.")

        # Thread is never joined because you have to terminate the Python process
        data_thread = Thread(target=self._poll_data, args=(refresh_minutes, enable_paging, ))
        data_thread.start()

        self._wait_for_data()

        # Start web server
        with socketserver.TCPServer(("", PORT), WebHandler) as httpd:
            print("Web server running on http://localhost:{}. Data is refreshed every {} minutes.".format(PORT, refresh_minutes))
            httpd.serve_forever()
    
    def _poll_data(self, refresh_minutes, enable_paging):
        while True:
            try:
                self._fetch_all_data(enable_paging)
            except:
                print("Error fetching data")
            finally:
                time.sleep(refresh_minutes * 60)
    
    def _fetch_all_data(self, enable_paging):
        start_time = time.time()

        metadata = GameFetcher().get_game_metadata() # metadata like titles
        all_metadata_json = json.dumps(metadata)

        with open(os.path.join(WEB_DATA_DIR, "metadata.json"), "w") as file_handle:
            file_handle.write(all_metadata_json)

        all_reviews = ReviewFetcher().get_reviews(metadata, enable_paging)
        all_reviews_json = json.dumps(all_reviews)
        with open(os.path.join(WEB_DATA_DIR, "reviews.json"), "w") as file_handle:
            file_handle.write(all_reviews_json)

        all_discussions = DiscussionFetcher().get_discussions(metadata, enable_paging)
        all_discussions_json = json.dumps(all_discussions)
        with open(os.path.join(WEB_DATA_DIR, "discussions.json"), "w") as file_handle:
            file_handle.write(all_discussions_json)

        stop_time = time.time()
        elapsed_time = stop_time - start_time

        num_posts = len(all_discussions) + sum([d["num_replies"] for d in all_discussions])
        
        print(f"\nFetched {len(all_discussions)} threads with {num_posts} posts, and {len(all_reviews)} reviews")
        print("{0} | Fetched data in {1:g}s".format(datetime.datetime.now(), elapsed_time))
    
    def _wait_for_data(self):
        required_files = ["discussions.json", "metadata.json", "reviews.json"]
        
        for filename in required_files:
            while not os.path.exists(os.path.join(WEB_DATA_DIR, filename)):
                time.sleep(1)

    def _ensure_output_directory_exists(self):
        if not os.path.isdir(WEB_DATA_DIR):
            os.mkdir(WEB_DATA_DIR)

Main().main()
