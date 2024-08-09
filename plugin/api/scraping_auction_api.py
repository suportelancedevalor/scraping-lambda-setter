import requests

from features.mega_leilao.domain.mega_leilao_house import House

class ScrapingAuctionAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_page(self, page: int, type: str):
        url = f"{self.base_url}/imoveis/{type}?pagina={page}"
        response = requests.get(url)
        return response
    
    def fetch_detail_page(self, url: str):
        response = requests.get(url)
        return response

    def dumb_request(self):
        url = f"{self.base_url}/test"
        response = requests.get(url)
        return response