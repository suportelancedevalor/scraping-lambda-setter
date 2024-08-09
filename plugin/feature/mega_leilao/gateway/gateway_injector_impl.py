
from features.mega_leilao.business.get_api import GETAPIUseCase
from features.mega_leilao.business.get_api_details import GETAPIDetailUseCase
from features.mega_leilao.gateway.presenter import Presenter
from plugin.feature.mega_leilao.gateway.presenter_impl import PresenterImpl
from plugin.feature.mega_leilao.repository_api_impl import RepositoryAPIImpl
from plugin.feature.mega_leilao.repository_aws_impl import RepositoryAWSImpl

class GatewayInjectorImpl(object):
    
    @staticmethod
    def inject()-> Presenter:
        repoAPI = RepositoryAPIImpl(url="https://www.megaleiloes.com.br")
        repoAWS = RepositoryAWSImpl()
        useCaseAPI = GETAPIUseCase(repo= repoAPI)
        useCaseDetail = GETAPIDetailUseCase(repo= repoAPI, repo_aws=repoAWS)

        return PresenterImpl(fetcher_api=useCaseAPI, 
                            fetcher_api_detail=useCaseDetail)