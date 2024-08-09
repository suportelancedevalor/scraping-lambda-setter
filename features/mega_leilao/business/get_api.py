from typing import Any, List
from ode.use_case import UseCase
from ode.output import Output
from ode.value_out_put import ValueOutput
from features.mega_leilao.business.repository_api import RepositoryAPI
from features.mega_leilao.domain.mega_leilao_house import HousesToReturn
from features.mega_leilao.domain.params_api import ParamsAPI

class GETAPIUseCase(UseCase[ParamsAPI, HousesToReturn]):
    def __init__(self, repo: RepositoryAPI):
        self.repo = repo

    def execute(self, param: ParamsAPI) -> Output[HousesToReturn]:
        site = self.repo.do_fetch(page=param.page, type=param.type)
        category = self.repo.load_category(type=param.type)
        houses = self.repo.read_tags_from_site(site, category)
        
        return ValueOutput(HousesToReturn(houses))