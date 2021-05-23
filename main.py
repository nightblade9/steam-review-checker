from data_fetcher import DataFetcher
import web_server

class Main:
    def main():
        fetcher = DataFetcher()
        all_reviews = fetcher.get_reviews()

        web_server.contents = len(all_reviews)
        web_server.run()

Main.main()