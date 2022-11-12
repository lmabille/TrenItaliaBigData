# launcher.py'
import sys
import json

from ScrapingBigData.crawl import crawl


def scrape(event={}, context={}):
    crawl()


if __name__ == "__main__":
    try:
        event = json.loads(sys.argv[1])
    except IndexError:
        event = {}
    scrape(event)
