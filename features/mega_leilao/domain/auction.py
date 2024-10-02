from dataclasses import dataclass
from typing import List

@dataclass
class AuctionParams:
    def __init__(self, url: str, category: str):
        self.url = url
        self.category = category

@dataclass
class AuctionDataCollection:
    def __init__(self, data: any):
        self.data = data

@dataclass
class AuctionResultParams:
    def __init__(self, params: List[AuctionParams]):
        self.params = params