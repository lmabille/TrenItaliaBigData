
from scrapy import *
import json
import datetime

class Station(Item):
    station_departure = Field()
    station_arrival = Field()
    is_delay = Field()
    delay_minutes = Field()



class QuotesSpider(Spider):
    name = "Station"
    f = open('ScrapingBigData/ScrapingBigData/output/stations.json')
    data = json.load(f)
    f.close()
    url = 'http://www.viaggiatreno.it/infomobilita/resteasy/viaggiatreno/partenze/'



    def start_requests(self):
        date = datetime.datetime.now().strftime("%a %b %d %Y %X GMT+0200 (heure d’été d’Europe centrale)")
        for station in self.data:
            link = f"{self.url}{station['id']}/{date}"
            yield Request(url=link, callback=self.parse,meta={'station_departure':station['name']})

    def parse(self, response):
        region = response.meta['station_departure']
        jsonresponse = json.loads(response.text)
        station_item = Station()
        station_item['region'] = region
        for station in jsonresponse:
            station_item['name'] = station['localita']['nomeBreve']
            station_item['id'] = station['localita']['id']
            yield station_item