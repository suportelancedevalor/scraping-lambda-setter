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
        collected_data = self.repo.collect_data(url=param.url_details)
        self.repo.save_to_dynamodb(collected_data)
        return ValueOutput(collected_data)
