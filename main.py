from fetchers.discussion_fetcher import DiscussionFetcher
from fetchers.game_fetcher import GameFetcher
from fetchers.review_fetcher import ReviewFetcher
import http.server
import json
import os
import socketserver
import time

PORT = 8000
WEB_DIR = os.path.join(os.path.dirname(__file__), "web")
WEB_DATA_DIR = os.path.join(WEB_DIR, "data")

class Main:
    def main(self):
        # Start web server.  This nukes build/data, so we have to wait for it to finish.
        self._ensure_output_directory_exists()
        self._fetch_all_data()

        # Start web server
        os.chdir(WEB_DIR)
        with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
            print("Web server running on http://localhost:{}".format(PORT))
            httpd.serve_forever()

    def _fetch_all_data(self):
        start_time = time.time()

        metadata = GameFetcher().get_game_metadata() # metadata like titles
        all_metadata_json = json.dumps(metadata)
        with open(os.path.join(WEB_DATA_DIR, "metadata.json"), "w") as file_handle:
            file_handle.write(all_metadata_json)

        all_reviews = ReviewFetcher().get_reviews(metadata)
        all_reviews_json = json.dumps(all_reviews)
        with open(os.path.join(WEB_DATA_DIR, "reviews.json"), "w") as file_handle:
            file_handle.write(all_reviews_json)

        all_discussions = DiscussionFetcher().get_discussions(metadata)
        all_discussions_json = json.dumps(all_discussions)
        with open(os.path.join(WEB_DATA_DIR, "discussions.json"), "w") as file_handle:
            file_handle.write(all_discussions_json)

        stop_time = time.time()
        elapsed_time = stop_time - start_time
        print("*** Fetched data in {0:g}s ***".format(elapsed_time))
    
    def _ensure_output_directory_exists(self):
        if not os.path.isdir(WEB_DATA_DIR):
            os.mkdir(WEB_DATA_DIR)

Main().main()
