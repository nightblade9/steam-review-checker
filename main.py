from data_fetcher import DataFetcher
import json
import os
import subprocess

class Main:
    def main(self):
        # Start web server.  This nukes build/data, so we have to wait for it to finish.
        self._build_web_app()

        self._ensure_output_directory_exists()
        self._fetch_all_data()

        # Start web server
        subprocess.Popen(["python", "-m", "http.server"], cwd=os.path.join("web", "build"), shell=True)

    def _build_web_app(self):
        # Build the self-hostable version of the app
        subprocess.run(["npm", "run", "build"], cwd="web", shell=True)

    def _fetch_all_data(self):
        fetcher = DataFetcher()
        all_reviews = fetcher.get_reviews()
        all_reviews_json = json.dumps(all_reviews)

        with open(os.path.join("web", "build", "data", "reviews.json"), "w") as file_handle:
            file_handle.write(all_reviews_json)
    
    def _ensure_output_directory_exists(self):
        if not os.path.isdir(os.path.join("web", "build")):
            os.mkdir(os.path.join("web", "build"))

        if not os.path.isdir(os.path.join("web", "build", "data")):
            os.mkdir(os.path.join("web", "build", "data"))

Main().main()