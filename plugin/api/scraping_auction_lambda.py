import json
import requests

from features.mega_leilao.domain.mega_leilao_house import House

class ScrapingAuctionLambda:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def start_sequence(self, house: House):
        url = f"https://rlaupwo5tl.execute-api.us-east-1.amazonaws.com/dev/detail"
        response = requests.post(url, data=house.toJSON())
        return response
    
    def start_save(self, house: House):
        url = f"https://rlaupwo5tl.execute-api.us-east-1.amazonaws.com/dev/save"
        response = requests.post(url, data=house.toJSON())
        return response
    
    def dumb_request(self):
        url = f"{self.base_url}/test"
        response = requests.get(url)
        return response