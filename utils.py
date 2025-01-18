import os
import json

BOOKMARK_FILE = "/Users/roshanraj-mac/Documents/VSCodeWS/py-browser/bookmarks.json"
HOME_TAB = "home_tab_title"
NEW_TAB = "new_tab_title"
GOOGLE = "http://www.google.com"

# Search and load the Home URL and new tab URL from bookmarks.json
def load_urls_from_bookmarks():
    # If there is no bookmark.json, create one with default tab URLs in it
    if not os.path.exists(BOOKMARK_FILE):
        with open(BOOKMARK_FILE, 'w') as file:
            json.dump([{'title': HOME_TAB, 'url': GOOGLE}, {'title': NEW_TAB, 'url': GOOGLE}], file, indent=4)
        return GOOGLE, GOOGLE
    try:
        with open(BOOKMARK_FILE, 'r') as file:
            bookmarks = json.load(file)
            home_url = next((bookmark['url'] for bookmark in bookmarks if bookmark['title'] == HOME_TAB), GOOGLE)
            new_tab_url = next((bookmark['url'] for bookmark in bookmarks if bookmark['title'] == NEW_TAB), GOOGLE)
            return home_url, new_tab_url
    except json.JSONDecodeError:
        return GOOGLE, GOOGLE
