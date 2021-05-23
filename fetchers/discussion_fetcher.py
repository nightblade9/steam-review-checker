#!/bin/python3
from fetchers.steam_fetcher import SteamFetcher
import re
import urllib

# Scrapes Steam's discussion forums to get you the latest greatest data.
class DiscussionFetcher(SteamFetcher):

    _STEAM_DISCUSSIONS_URL = SteamFetcher._STEAM_COMMUNITY_URL + "/discussions/"
    _NUMBER_OF_REPLIES_START = '<img src="https://community.akamai.steamstatic.com/public/images/skin_1/comment_quoteicon.png">'
    _NUMBER_OF_REPLIES_STOP = '</div>'

    def get_discussions(self):
        config_json = self._read_config_json()
        app_ids = config_json["appIds"]
        all_discussions = []

        for app_id in app_ids:
            url = DiscussionFetcher._STEAM_DISCUSSIONS_URL.format(app_id)
            response = urllib.request.urlopen(url).read()
            raw_html = response.decode('utf-8')

            # Repair HTML
            raw_html = raw_html.replace('class="searchtext"', '')

            reply_counts = self._get_reply_counts(raw_html)
            print(str(reply_counts))
    
    def _get_reply_counts(self, raw_html):
        to_return = []
        for index in re.finditer(DiscussionFetcher._NUMBER_OF_REPLIES_START, raw_html):
            start_index = index.span()[1]
            stop_index = raw_html.index(DiscussionFetcher._NUMBER_OF_REPLIES_STOP, start_index)
            print("Start={} stop={}".format(start_index, stop_index))
            number_of_replies = raw_html[start_index:stop_index]
            to_return.append(int(number_of_replies))
            #print("{}, {} from {} to {}: {}".format(raw_html[index.span()[0]:index.span()[1]], number_of_replies, start_index, stop_index, number_of_replies))
            print("RAw replies are: {}".format(number_of_replies))
        return to_return