from abc import ABC, abstractmethod
from typing import Any, List
from features.mega_leilao.domain.mega_leilao_house import HouseSavedToReturn
from features.mega_leilao.domain.mega_leilao_house_detail import HouseWithDetailToReturn

class RepositoryAWS(ABC):
    @abstractmethod
    def do_save(self, item: HouseWithDetailToReturn) -> HouseSavedToReturn:
        pass