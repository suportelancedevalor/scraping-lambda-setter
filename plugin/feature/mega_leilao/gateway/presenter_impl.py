from typing import List
from ode.base_controller import BaseController
from ode.sequence_use_case import SequenceUseCase
from features.mega_leilao.business.get_api import GETAPIUseCase
from features.mega_leilao.business.get_api_details import GETAPIDetailUseCase
from features.mega_leilao.domain.auction import AuctionParams, AuctionResultParams
from features.mega_leilao.domain.params_api import ParamsAPI
from features.mega_leilao.gateway.gateway_injector import GatewayInjector
from features.mega_leilao.gateway.presenter import Presenter

class PresenterImpl(GatewayInjector, BaseController, Presenter):
    def __init__(self, fetcher_api: GETAPIUseCase, 
                fetcher_api_detail: GETAPIDetailUseCase):
        self.fetcher_api = fetcher_api
        self.fetcher_api_detail = fetcher_api_detail

    def handle_error(self, error: Exception):
        print(f"handle_error : {error}.")
    
    def handle_success(self, value):
        if isinstance(value, AuctionResultParams):
            return self.on_sequence(value.params)

    def on_sequence(self, params: List[AuctionParams]):
        sequence = SequenceUseCase.builder()
        for param in params:
            sequence.add(use_case=self.fetcher_api_detail, param=param)
        
        usecases = sequence.build()
        self.dispatch_use_case(None, usecases)

    def get_house(self, page :int):
        params = ParamsAPI(page= page, type="casas")
        self.dispatch_use_case(params, self.fetcher_api)

    def get_apartment(self, page: int):
        params = ParamsAPI(page= page, type="apartamentos")
        self.dispatch_use_case(params, self.fetcher_api)

    def get_shed(self, page: int):
        params = ParamsAPI(page= page, type="galpoes--industriais")
        self.dispatch_use_case(params, self.fetcher_api)

    def get_land(self, page: int):
        params = ParamsAPI(page= page, type="terrenos-e-lotes")
        self.dispatch_use_case(params, self.fetcher_api)

    def get_garage_deposit(self, page: int):
        params = ParamsAPI(page= page, type="deposito-de-garagem")
        self.dispatch_use_case(params, self.fetcher_api)
    
    def get_commercial_real_estate(self, page: int):
        params = ParamsAPI(page= page, type="imoveis-comerciais")
        self.dispatch_use_case(params, self.fetcher_api)
    
    def get_parking_spaces(self, page: int):
        params = ParamsAPI(page= page, type="vagas-de-garagem")
        self.dispatch_use_case(params, self.fetcher_api)
    
    def get_plots(self, page: int):
        params = ParamsAPI(page= page, type="glebas")
        self.dispatch_use_case(params, self.fetcher_api)
    
    def get_rural_properties(self, page: int):
        params = ParamsAPI(page= page, type="imoveis-rurais")
        self.dispatch_use_case(params, self.fetcher_api)
    
    def get_rural_real_estate(self, page: int):
        params = ParamsAPI(page= page, type="terrenos-para-incorporacao")
        self.dispatch_use_case(params, self.fetcher_api)