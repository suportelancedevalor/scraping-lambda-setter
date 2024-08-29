
from dataclasses import dataclass

from features.mega_leilao.domain.mega_leilao_house import House

@dataclass
class HouseDetail:
    def __init__(self, size: str="não informado", 
                principal: str="não informado", 
                auctioneer: str="não informado", 
                auction_id: str="não informado",
                street_address: str="-",
                number_address: str="-",
                neighborhood_address: str="-",
                city_address: str="-",
                state_address: str="-",
                description:str=""):
        self.size = size
        self.principal = principal
        self.auctioneer = auctioneer
        self.auction_id = auction_id
        self.street_address = street_address
        self.number_address = number_address
        self.neighborhood_address = neighborhood_address
        self.city_address = city_address
        self.state_address = state_address
        self.description  = description

@dataclass
class HouseWithDetailToReturn:
    def __init__(self, house: House):
        self.house = house