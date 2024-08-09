
from dataclasses import dataclass
import json
from typing import List

@dataclass
class House:
    def __init__(self, uid: str, category: str,
                title: str="não informado",
                price: str="não informado", 
                status: str="não informado",
                value: str="não informado", 
                batch_code: str="não informado", 
                card_locality: str="não informado", 
                street_address: str="-",
                number_address: str="-",
                neighborhood_address: str="-",
                city_address: str="-",
                state_address: str="-",
                url_details: str="não informado", 
                card_image: str="não informado",
                size: str="não informado", 
                principal: str="não informado", 
                auctioneer: str="não informado", 
                auction_id: str="não informado",
                enabled: bool=True):
        self.uid = uid
        self.category = category
        self.title = title
        self.price = price
        self.status = status
        self.value = value
        self.batch_code = batch_code
        self.card_locality = card_locality
        self.street_address = street_address
        self.number_address = number_address
        self.neighborhood_address = neighborhood_address
        self.city_address = city_address
        self.state_address = state_address
        self.url_details = url_details
        self.card_image = card_image
        self.size = size
        self.principal = principal
        self.auctioneer = auctioneer
        self.auction_id = auction_id
        self.enabled = enabled

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=14)


@dataclass
class HousesToReturn:
    def __init__(self, houses: List[House]):
        self.houses = houses

@dataclass
class HouseSavedToReturn:
    def __init__(self, house: House):
        self.house = house