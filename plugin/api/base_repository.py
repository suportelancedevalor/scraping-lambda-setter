from requests import Response
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from ode.authentication_exception import AuthenticationException
from ode.http_exception import HttpException
from ode.internet_connection_exception import InternetConnectionException

from plugin.api.scraping_auction_api import ScrapingAuctionAPI


class BaseRepository:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_body_or_throw(self, call :Response):
        try:
            content = call.content            
            return BeautifulSoup(content, 'html.parser')
        except RequestException as e:
            if call.status_code == 401:
                raise AuthenticationException()
            raise HttpException(call.status_code, call.reason)

    def get_service_mega_leilao(self) -> ScrapingAuctionAPI:
        raise NotImplementedError("get_service method must be implemented in subclass")

    def dumb_request(self):
        self.get_body_or_throw(self.get_service().dumb_request())