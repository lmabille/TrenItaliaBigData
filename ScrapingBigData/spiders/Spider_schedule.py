
from scrapy import *
import json
import datetime


class trains_item(Item):
    train_id = Field()
    station_departure = Field()
    station_departure_id = Field()
    station_arrival = Field()
    station_arrival_id = Field()
    is_delay = Field()
    delay = Field()
    delay_minutes = Field()


class QuotesSpider(Spider):
    name = "schedule"
    f = open('ScrapingBigData/output/stations.json')
    data = json.load(f)
    f.close()
    url = 'http://www.viaggiatreno.it/infomobilita/resteasy/viaggiatreno/partenze/'

    def start_requests(self):
        date = datetime.datetime.now().strftime(
            "%a %b %d %Y %X GMT+0200 (heure d’été d’Europe centrale)")
        day = datetime.datetime.now().strftime("%a")
        month = datetime.datetime.now().strftime("%b")
        day_num = datetime.datetime.now().strftime("%d")
        year = datetime.datetime.now().strftime("%Y")
        hour = datetime.datetime.now().strftime("%X")

        for station in self.data:
            link = f"{self.url}{station['id']}/{date}"
            url = f"http://www.viaggiatreno.it/infomobilita/resteasy/viaggiatreno/partenze/{station['id']}/{day}%20{month}%20{day_num}%20{year}%20{hour}%20GMT+0200%20(heure%20d%E2%80%99%C3%A9t%C3%A9%20d%E2%80%99Europe%20centrale)"
            yield Request(url=url, callback=self.parse, meta={'station_departure': station['name'], 'id': station['id']})

    def parse(self, response):
        station_departure = response.meta['station_departure']
        station_departure_id = response.meta['id']
        if response.text != '[]':
            jsonresponse = json.loads(response.text)
            trains = trains_item()
            trains['station_arrival'] = station_departure
            trains['station_arrival_id'] = station_departure_id
            for train in jsonresponse:
                trains['train_id'] = train['numeroTreno']
                trains['delay'] = train['compRitardo'][1]
                trains['station_departure_id'] = train['codOrigine']
                yield trains
