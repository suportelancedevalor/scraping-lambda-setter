


from plugin.api.scraping_auction_api import ScrapingAuctionAPI
from plugin.api.scraping_auction_lambda import ScrapingAuctionLambda

class ScrapingAuctionAPIBuilder:
    def __init__(self, base_url):
        self.base_url = base_url

    def build(self):
        return ScrapingAuctionAPI(self.base_url)
    

class ScrapingAuctionLambdaBuilder:
    def __init__(self, base_url):
        self.base_url = base_url

    def build(self):
        return ScrapingAuctionLambda(self.base_url)