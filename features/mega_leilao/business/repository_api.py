from abc import ABC, abstractmethod
from typing import Any, List
from bs4 import Tag

from features.mega_leilao.domain.auction import AuctionParams

class RepositoryAPI(ABC):
    @abstractmethod
    def collect_data(self, url: str, category: str):
        pass

    @abstractmethod
    def do_fetch(self, page: int, type: str) -> Tag:
        pass

    @abstractmethod
    def read_url_from_site(self, site: Tag, category: str) -> List[AuctionParams]:
        pass

    @abstractmethod
    def load_category(self, type: str) -> str:
        pass