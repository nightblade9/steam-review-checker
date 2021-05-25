from fetchers.discussion_fetcher import DiscussionFetcher
from fetchers.game_fetcher import GameFetcher
from fetchers.review_fetcher import ReviewFetcher
import json
import os
import shutil
import subprocess
import time

class Main:
    def main(self):
        # Start web server.  This nukes build/data, so we have to wait for it to finish.
        self._build_web_app()

        self._ensure_output_directory_exists()
        self._fetch_all_data()

        # Copy data to public/data. Makes local development easier
        if os.path.exists(os.path.join("web", "public", "data")):
            shutil.rmtree(os.path.join("web", "public", "data"))
        shutil.copytree(os.path.join("web", "build", "data"), os.path.join("web", "public", "data"))

        # Start web server
        subprocess.Popen(["python", "-m", "http.server"], cwd=os.path.join("web", "build"), shell=True)

    def _build_web_app(self):
        # Build the self-hostable version of the app
        subprocess.run(["npm", "run", "build"], cwd="web", shell=True)

    def _fetch_all_data(self):
        start_time = time.time()

        metadata = GameFetcher().get_game_metadata() # metadata like titles
        all_metadata_json = json.dumps(metadata)
        with open(os.path.join("web", "build", "data", "metadata.json"), "w") as file_handle:
            file_handle.write(all_metadata_json)

        all_reviews = ReviewFetcher().get_reviews(metadata)
        all_reviews_json = json.dumps(all_reviews)
        with open(os.path.join("web", "build", "data", "reviews.json"), "w") as file_handle:
            file_handle.write(all_reviews_json)

        all_discussions = DiscussionFetcher().get_discussions(metadata)
        all_discussions_json = json.dumps(all_discussions)
        with open(os.path.join("web", "build", "data", "discussions.json"), "w") as file_handle:
            file_handle.write(all_discussions_json)

        stop_time = time.time()
        elapsed_time = stop_time - start_time
        print("*** Fetched data in {0:g}s ***".format(elapsed_time))
    
    def _ensure_output_directory_exists(self):
        if not os.path.isdir(os.path.join("web", "build")):
            os.mkdir(os.path.join("web", "build"))

        if not os.path.isdir(os.path.join("web", "build", "data")):
            os.mkdir(os.path.join("web", "build", "data"))

Main().main()