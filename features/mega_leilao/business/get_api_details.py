from typing import List
from features.mega_leilao.business.repository_aws import RepositoryAWS
from ode.use_case import UseCase
from ode.output import Output
from ode.value_out_put import ValueOutput
from features.mega_leilao.business.repository_api import RepositoryAPI
from features.mega_leilao.domain.auction import AuctionDataCollection, AuctionParams

class GETAPIDetailUseCase(UseCase[AuctionParams, AuctionDataCollection]):
    def __init__(self, repo: RepositoryAPI, repo_aws: RepositoryAWS):
        self.repo = repo
        self.repo_aws = repo_aws

    def execute(self, param: AuctionParams) -> Output[AuctionDataCollection]:
        collected_data = self.repo.collect_data(url=param.url, category=param.category)
        if collected_data is not None:
            self.repo_aws.save_to_dynamodb(collected_data)
            
        return ValueOutput(collected_data)