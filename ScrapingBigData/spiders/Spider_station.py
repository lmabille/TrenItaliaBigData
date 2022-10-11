
from scrapy import *
import json


class Station(Item):
    name = Field()
    region = Field()
    id = Field()


class QuotesSpider(Spider):
    name = "Station"
    f = open('ScrapingBigData/utils/region.json')
    data = json.load(f)
    f.close()
    url = 'http://www.viaggiatreno.it/infomobilita/resteasy/viaggiatreno/elencoStazioni/'

    def start_requests(self):
        for region in self.data:
            link = f"{self.url}{region['id']}"
            yield Request(url=link, callback=self.parse, meta={'region': region['regione']})

    def parse(self, response):
        region = response.meta['region']
        jsonresponse = json.loads(response.text)
        station_item = Station()
        station_item['region'] = region
        for station in jsonresponse:
            station_item['name'] = station['localita']['nomeBreve']
            station_item['id'] = station['localita']['id']
            yield station_item
