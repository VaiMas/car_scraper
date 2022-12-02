import scrapy
from scrapy.http.request import Request
import time



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
        for page in range (50):
            page += 1
            webs.append(f'https://apipub.pp.lv/lv/api_user/v1/categories/2/lots?fV%5B22%5D%5Btype%5D=2363&orderColumn=publishDate&orderDirection=DESC&currentPage={page}&itemsPerPage=20')
            
        for url in webs:
            time.sleep(2)
            yield Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        pass