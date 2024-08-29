from typing import List
from features.mega_leilao.business.repository_api import RepositoryAPI
from features.mega_leilao.domain.mega_leilao_house import House
from features.mega_leilao.domain.mega_leilao_house_detail import HouseDetail
from plugin.api.api_builder import ScrapingAuctionAPIBuilder
from plugin.api.base_repository import BaseRepository
import uuid
from bs4 import Tag

class RepositoryAPIImpl(BaseRepository, RepositoryAPI):
    def __init__(self, url: str):
        super().__init__(url)

    def do_fetch(self, page: int, type: str) -> Tag:
        site = self.get_body_or_throw(self.get_service().fetch_page(page=page,type=type))
        return site
    
    def do_fetch_details(self, url: str) -> Tag:
        details = self.get_body_or_throw(self.get_service().fetch_detail_page(url=url))
        return details
    
    def read_tags_from_details(self, site: Tag) -> HouseDetail:
        size = site.find_all('div', attrs={'class': 'item'})[0].text
        author = site.find('div', attrs={'class': 'author item'})
        principal = author.find_all('div', attrs={'class': 'value'})[0].text
        auctioneer = author.find('div', attrs={'class': 'value'}).find_all_next('div', attrs={'class': 'value'})[0].text
        auction_id = site.find('div', attrs={'class': 'auction-id'}).find_all_next('div', attrs={'class': 'value'})[0].text
        description_value = site.find('div', attrs={'class': 'col-sm-6 col-md-8 description border'}).find_all_next('div', attrs={'class': 'value'})[0].text
        description_disclaimer = site.find('div', attrs={'class': 'col-sm-6 col-md-8 description border'}).find_all_next('div', attrs={'class': 'disclaimer'})[0].text
        description_disclaimer_legal = site.find('div', attrs={'class': 'col-sm-6 col-md-8 description border'}).find_all_next('div', attrs={'class': 'disclaimer-legal'})[0].text
        description = description_value +"\n"+description_disclaimer+"\n"+description_disclaimer_legal
        full_address = site.find('div', attrs={'class': 'locality item'}).find_all_next('div', attrs={'class': 'value'})[0].text
        array_address = full_address.strip().split(",")
        street_address: str="-",
        number_address: str="-",
        neighborhood_address: str="-",
        city_address: str="-",
        state_address: str="-"  

        if(array_address != None):
            street_address = array_address[0]
            number_address = array_address[1]
            neighborhood_address = array_address[2]
            city_address = array_address[3]
            state_address = array_address[4]

        return HouseDetail(size=size, principal=principal, auctioneer=auctioneer, auction_id=auction_id, street_address=street_address, 
                           number_address=number_address, neighborhood_address=neighborhood_address, city_address=city_address,state_address= state_address, description=description)

    def read_tags_from_site(self, site: Tag, category: str) -> List[House]:
        houses = []
        news_houses = site.findAll('div', attrs={'class': 'col-sm-6 col-md-4 col-lg-3'})
        for news in news_houses:
            title = news.find_all('a', attrs={'class': 'card-title'})[0].text
            status = news.find_all('div', attrs={'class':'card-status'})[0].text
            batch_code = news.find_all('div', attrs={'class':'card-number pull-left'})[0].text
            card_locality = news.find_all('a', attrs={'class':'card-locality'})[0].text
            card_image = news.find_all('a', attrs={'class':'card-image'})[0]['data-bg']
            url_detail = news.find_all('a', attrs={'class':'card-image'})[0]['href']
            price = self.get_field(news, 'div', 'card-price')
            value = self.get_field(news, 'span', 'card-instance-value')

            new_house = House(uid=str(uuid.uuid4()), category=category,
                          title=title, status=status,batch_code=batch_code,
                          card_locality=card_locality, url_details=url_detail, card_image=card_image, price=price, value=value)
        
            houses.append(new_house)

        return houses

    def get_service(self):
        return ScrapingAuctionAPIBuilder(self.base_url).build()
    
    def load_category(self, type: str) -> str:
        if type == "casas":
            return "Casas"
        elif type == "apartamentos":
            return "Apartamentos"
        elif type == "galpoes--industriais":
            return "Galpões / Industriais"
        elif type == "terrenos-e-lotes":
            return "Terrenos e Lotes"
        elif type == "deposito-de-garagem":
            return "Depósito de Garagem"
        elif type == "imoveis-comerciais":
            return "Imóveis Comerciais"
        elif type == "vagas-de-garagem":
            return "Vagas de Garagem"
        elif type == "glebas":
            return "Glebas"
        elif type == "imoveis-rurais":
            return "Fazendas"
        elif type == "terrenos-para-incorporacao":
            return "Terrenos para Incorporação"
        else:
            return "não informado"
                
    def get_field(self, news, tag, fieldClass):
        field = news.find_all(tag, attrs={'class': fieldClass})[0].text
        
        if not field:
            field = 'não informado'

        return field
    