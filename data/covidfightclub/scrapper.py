"""
Script to scrape information from https://covidfightclub.org/?search_key=Mumbai&city_id=&medicine_id=4&type=&s=09
"""

import requests
import urllib.request
import time
from bs4 import BeautifulSoup


url = "https://covidfightclub.org/?search_key=Mumbai&city_id=&medicine_id=4&type=&s=09"
response = requests.get(url)

if str(response) == '<Response [200]>':
    # ready to scrape
    soup = BeautifulSoup(response.text, "html.parser")

    # import ipdb; ipdb.set_trace()

    mydivs = soup.findAll('div')
    for div in mydivs:
        if "class" in div:
            if (div["class"] == "detail-wrapper"):
                print(div)
                print("=======================")
    import ipdb; ipdb.set_trace()
