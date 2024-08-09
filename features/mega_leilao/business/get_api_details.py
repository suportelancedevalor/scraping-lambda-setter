from typing import List
from features.mega_leilao.business.repository_aws import RepositoryAWS
from features.mega_leilao.domain.mega_leilao_house_detail import HouseWithDetailToReturn
from ode.use_case import UseCase
from ode.output import Output
from ode.value_out_put import ValueOutput
from features.mega_leilao.business.repository_api import RepositoryAPI
from features.mega_leilao.domain.mega_leilao_house import House

class GETAPIDetailUseCase(UseCase[House, HouseWithDetailToReturn]):
    def __init__(self, repo: RepositoryAPI, repo_aws: RepositoryAWS):
        self.repo = repo
        self.repo_aws = repo_aws

    def execute(self, param: House) -> Output[HouseWithDetailToReturn]:
        site = self.repo.do_fetch_details(url=param.url_details)
        detail = self.repo.read_tags_from_details(site=site)
        param.size = detail.size
        param.principal = detail.principal
        param.auctioneer = detail.auctioneer
        param.street_address = detail.street_address
        param.number_address = detail.number_address
        param.neighborhood_address = detail.neighborhood_address
        param.city_address = detail.city_address
        param.state_address = detail.state_address
        
        new_house = self.repo_aws.do_save(HouseWithDetailToReturn(param))
        return ValueOutput(new_house)
