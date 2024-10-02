from typing import Any, List
from ode.use_case import UseCase
from ode.output import Output
from ode.value_out_put import ValueOutput
from features.mega_leilao.business.repository_api import RepositoryAPI
from features.mega_leilao.domain.auction import AuctionParams, AuctionResultParams
from features.mega_leilao.domain.params_api import ParamsAPI

class GETAPIUseCase(UseCase[ParamsAPI, AuctionResultParams]):
    def __init__(self, repo: RepositoryAPI):
        self.repo = repo

    def execute(self, param: ParamsAPI) -> Output[AuctionResultParams]:
        site = self.repo.do_fetch(page=param.page, type=param.type)
        category = self.repo.load_category(type=param.type)
        params = self.repo.read_url_from_site(site, category)

        return ValueOutput(AuctionResultParams(params))