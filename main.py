from data_fetcher import DataFetcher
import os
import subprocess
from threading import Thread

class Main:
    def main(self):
        # Required for parallel execution
        self._ensure_output_directory_exists()

        # Start building/running web server
        web_thread = Thread(target = self._build_web_app)
        web_thread.start()

        # Grab all the necessary data from API calls and dump them to files
        data_thread = Thread(target = self._fetch_all_data)
        data_thread.start()

        # Wait for everything to be done
        web_thread.join()
        data_thread.join()

        # Start web server
        subprocess.Popen(["python", "-m", "http.server"], cwd=os.path.join("web", "build"), shell=True)


    def _build_web_app(self):
        # Build the self-hostable version of the app
        subprocess.run(["npm", "run", "build"], cwd="web", shell=True)

    def _fetch_all_data(self):
        fetcher = DataFetcher()
        all_reviews = fetcher.get_reviews()
        return {"reviews": all_reviews}
    
    def _ensure_output_directory_exists(self):
        if not os.path.isdir(os.path.join("web", "build")):
            os.mkdir(os.path.join("web", "build"))

        if not os.path.isdir(os.path.join("web", "build", "data")):
            os.mkdir(os.path.join("web", "build", "data"))

Main().main()