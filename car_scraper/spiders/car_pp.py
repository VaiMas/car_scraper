import scrapy
from scrapy.http.request import Request
import time
import json
import csv


class CarPpSpider(scrapy.Spider):
    name = 'car_pp'
    headers = {
        "Connection": "keep-alive",
        "accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
        "content-type": "application/javascript",
        "Origin": "https://pp.lv",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://pp.lv/",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept": "application/json, text/plain, */*",
    }

    def start_requests(self):
        """Sends request to url with headers and get json file for parsing, for 
        now it is 50 urls with 20 entries each with 2s delay.
        """
        webs = []
        for page in range(3):
            page += 1
            webs.append(
                f'https://apipub.pp.lv/lv/api_user/v1/categories/2/lots?fV%5B22%5D%5Btype%5D=2363&orderColumn=publishDate&orderDirection=DESC&currentPage={page}&itemsPerPage=20')

        for url in webs:
            time.sleep(2)
            yield Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        """Parses json file and writes to csv with information of manufacturer,
        model, production year, milage, VIN code and license plate.
        """
        data = json.loads(response.body)
        car = []
        try:
            for name in data['content']['data']:
                data_for_dictionary = {
                    'Manufacturer': name['category']['parent']['name'],
                    'Model': name['category']['name'],
                    'Year': None,
                    'Milage': None,
                    'VIN': None,
                    'LP': None
                }

                for value in name['adFilterValues']:
                    if value['filter']['name'] == 'Izlaiduma gads':
                        year = value["value"]["displayValue"]
                        data_for_dictionary['Year'] = year
                    if value['filter']['name'] == 'Nobraukums, km':
                        milage = value["textValue"]
                        data_for_dictionary['Milage'] = milage
                    if value['filter']['name'] == 'VIN kods':
                        vin = value["textValue"]
                        data_for_dictionary['VIN'] = vin
                    if value['filter']['name'] == 'Auto numurs':
                        lp = value["textValue"]
                        data_for_dictionary['LP'] = lp

                car.append(data_for_dictionary)

            with open('file.csv', 'a', encoding='utf-8', newline='') as csvfile:
                headers = ['Manufacturer', 'Model',
                           'Year', 'Milage', 'VIN', 'LP']
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                csvfile.seek(0, 2)

                if csvfile.tell() == 0:
                    writer.writeheader()

                writer.writerows(car)
        except:
            print('Something went wrong please try it again or contact developer')
