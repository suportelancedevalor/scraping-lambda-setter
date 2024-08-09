from abc import ABC, abstractmethod
from typing import Any, List
from features.mega_leilao.domain.mega_leilao_house import House
from bs4 import Tag

from features.mega_leilao.domain.mega_leilao_house_detail import HouseDetail

class RepositoryAPI(ABC):
    @abstractmethod
    def do_fetch(self, page: int, type: str) -> Tag:
        pass

    def do_fetch_details(self, url: str) -> Tag:
        pass

    @abstractmethod
    def read_tags_from_site(self, site: Tag, category: str) -> List[House]:
        pass

    @abstractmethod
    def read_tags_from_details(self, site: Tag) -> HouseDetail:
        pass

    @abstractmethod
    def load_category(self, type: str) -> str:
        pass
    