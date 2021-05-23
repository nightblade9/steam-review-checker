#!/bin/python3
import datetime
from fetchers.steam_fetcher import SteamFetcher
import urllib
import lxml.html

# Scrapes Steam's discussion forums to get you the latest greatest data.
class DiscussionFetcher(SteamFetcher):

    _STEAM_DISCUSSIONS_URL = SteamFetcher._STEAM_COMMUNITY_URL + "/discussions/"
    _DISCUSSION_NODE_ROOT_XPATH = "//div[contains(@class, 'forum_topic ')]"

    def get_discussions(self):
        config_json = self._read_config_json()
        app_ids = config_json["appIds"]
        all_discussions = []

        for app_id in app_ids:
            url = DiscussionFetcher._STEAM_DISCUSSIONS_URL.format(app_id)
            response = urllib.request.urlopen(url).read()
            raw_html = response.decode('utf-8')

            # Repair HTML so we can use XPath
            raw_html = raw_html.replace('class="searchtext"', '')
            
            # Parse the output
            root = lxml.html.fromstring(raw_html)
            discussion_nodes = root.xpath(DiscussionFetcher._DISCUSSION_NODE_ROOT_XPATH)

            for i in range(len(discussion_nodes)):
                node = discussion_nodes[i]

                link_node = [a for a in node if a.tag == 'a'][0]
                discussion_url = link_node.attrib["href"]

                dissected_nodes = node.text_content().strip().split('\t\t\t\t')
                # Dissected nodes is eight items, including some empty ones.
                num_replies = dissected_nodes[0].strip()

                title_and_author = dissected_nodes[7].split('\n')
                title = title_and_author[0].strip()
                author = title_and_author[-1].strip()

                raw_date = dissected_nodes[2].strip()
                discussion_date = datetime.datetime.strptime(raw_date, '%d %b, %Y @ %I:%M%p').strftime("%Y-%m-%d %H:%M")
                print(discussion_date)

                all_discussions.append({
                    "title": title,
                    "date": discussion_date,
                    "author": author,
                    "url": discussion_url,
                    "num_replies": num_replies,
                })

            # Sort by time descending, order of games isn't important
            all_discussions.sort(key=lambda x: x["date"], reverse=True)
