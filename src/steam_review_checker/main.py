import datetime
from .fetchers.steam_fetcher import SteamFetcher
from .fetchers.discussion_fetcher import DiscussionFetcher
from .fetchers.game_fetcher import GameFetcher
from .fetchers.review_fetcher import ReviewFetcher
import http.server
import json
import os
import re
import socketserver
from threading import Thread
import time

REFRESH_INTERVAL_CONFIG_KEY = "refreshDataIntervalMinutes"
REFRESH_INTERVAL_DEFAULT_MINUTES = 60

PORT = 8000
WEB_DIR = os.path.join(os.path.dirname(__file__), "web")
WEB_DATA_DIR = os.path.join(WEB_DIR, "data")

class App:
    def __init__(self):
        self.data_ready = False
        self.data_json = {
            "metadata": "{}",
            "reviews": "[]",
            "discussions": "[]"
        }

    def run(self):
        config = SteamFetcher()._read_config_json()
        refresh_minutes = REFRESH_INTERVAL_DEFAULT_MINUTES

        if REFRESH_INTERVAL_CONFIG_KEY in config:
            refresh_minutes = int(config[REFRESH_INTERVAL_CONFIG_KEY])

        data_thread = Thread(target=self._poll_data, args=(refresh_minutes,))
        data_thread.start()

        self._wait_for_data()

        # Start web server
        with socketserver.TCPServer(("", PORT), WebHandler) as httpd:
            print("Web server running on http://localhost:{}. Data is refreshed every {} minutes.".format(PORT, refresh_minutes))
            httpd.serve_forever()
    
    def _poll_data(self, refresh_minutes):
        while True:
            self._fetch_all_data()
            time.sleep(refresh_minutes * 60)
    
    def _fetch_all_data(self):
        start_time = time.time()

        metadata = GameFetcher().get_game_metadata() # metadata like titles
        self.data_json["metadata"] = json.dumps(metadata)

        all_reviews = ReviewFetcher().get_reviews(metadata)
        self.data_json["reviews"] = json.dumps(all_reviews)

        all_discussions = DiscussionFetcher().get_discussions(metadata)
        self.data_json["discussions"] = json.dumps(all_discussions)

        stop_time = time.time()
        elapsed_time = stop_time - start_time
        print("{0} | Fetched data in {1:g}s".format(datetime.datetime.now(), elapsed_time))

        self.data_ready = True
    
    def _wait_for_data(self):
        while True:
            if self.data_ready:
                return
            time.sleep(1)

app = App()

class WebHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.data_regex = re.compile("/data/([^\.]+)\.json$")

        super().__init__(*args, directory=WEB_DIR, **kwargs)
    
    def do_GET(self):
        # Intercept data requests and return whatever's been fetched
        pattern_match = self.data_regex.match(self.path)
        if pattern_match:
            data_type = pattern_match.group(1)
            if data_type in app.data_json:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                response_bytes = bytes(app.data_json[data_type], "utf8")
                self.wfile.write(response_bytes)
                return

        # Fall back to static files if it's not a data request
        super().do_GET()

def run_app():
    app.run()

if __name__ == "__main__":
    run_app()
