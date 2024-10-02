from typing import List

from features.mega_leilao.business.repository_api import RepositoryAPI
from features.mega_leilao.domain.mega_leilao_house import House
from features.mega_leilao.domain.mega_leilao_house_detail import HouseDetail
from plugin.api.api_builder import ScrapingAuctionAPIBuilder
from plugin.api.base_repository import BaseRepository
import uuid
from bs4 import Tag
import boto3

class RepositoryAPIImpl(BaseRepository, RepositoryAPI):
    def __init__(self, url: str):
        super().__init__(url)

    def extract_title(self, soup):
        title_tag = soup.find('h1', class_='section-header')
        return title_tag.get_text(strip=True) if title_tag else 'title_not_found'

    
    def extract_images(self, soup):
        images = [img['src'] for img in soup.find_all('img') if img.get('src')]
        return images if images else []

    
    def extract_location(self, soup):
        location_tag = soup.find('div', class_='locality item')
        return location_tag.find('div', class_='value').get_text(strip=True) if location_tag else 'location_not_found'

    
    def extract_jurisdiction(self, soup):
        jurisdiction_tag = soup.find('div', class_='jurisdiction item')
        return jurisdiction_tag.find('div', class_='value').get_text(strip=True) if jurisdiction_tag else 'jurisdiction_not_found'

    
    def extract_forum(self, soup):
        forum_tag = soup.find('div', class_='forum item')
        return forum_tag.find('div', class_='value').get_text(strip=True) if forum_tag else 'forum_not_found'

    
    def extract_author(self, soup):
        author_tag = soup.find('div', class_='author item')
        return author_tag.find('div', class_='value').get_text(strip=True) if author_tag else 'author_not_found'

    
    def extract_defendant(self, soup):
        defendant_tag = soup.find('div', class_='forum.item')
        return defendant_tag.find('div', class_='value').get_text(strip=True) if defendant_tag else 'defendant_not_found'

    
    def extract_process(self, soup):
        process_tag = soup.find('div', class_='process-number.item')
        return process_tag.find('div', class_='value').get_text(strip=True) if process_tag else 'process_not_found'

    
    def extract_control(self, soup):
        control_tag = soup.find('div', class_='process-control item')
        return control_tag.find('div', class_='value').get_text(strip=True) if control_tag else 'control_not_found'

    
    def extract_lot_number(self, soup):
        lot_number_tag = soup.find('div', class_='col-md-6').find('div', class_='card-number')
        return lot_number_tag.get_text(strip=True) if lot_number_tag else 'lot_number_not_found'

    
    def extract_last_bid(self, soup):
        last_bid_tag = soup.find('div', class_='last-bid')
        return last_bid_tag.find('div', class_='value').get_text(strip=True) if last_bid_tag else 'last_bid_not_found'

    
    def extract_increment(self, soup):
        increment_tag = soup.find('div', class_='increment')
        return increment_tag.find('div', class_='value').get_text(strip=True) if increment_tag else 'increment_not_found'

    
    def extract_auction_dates(self, soup):
        first_auction_tag = soup.find('span', class_='card-first-instance-date')
        second_auction_tag = soup.find('span', class_='card-second-instance-date')
        first_value_tag = soup.find('span', class_='card-instance-value')
        second_value_tag = soup.find_all('span', class_='card-instance-value')[1] if len(soup.find_all('span', 'card-instance-value')) > 1 else None

        return {
            'first_auction': {
                'date': first_auction_tag.get_text(strip=True) if first_auction_tag else 'first_auction_not_found',
                'value': first_value_tag.get_text(strip=True) if first_value_tag else 'first_value_not_found'
            },
            'second_auction': {
                'date': second_auction_tag.get_text(strip=True) if second_auction_tag else 'second_auction_not_found',
                'value': second_value_tag.get_text(strip=True) if second_value_tag else 'second_value_not_found'
            }
        }

    
    def extract_valuation(self, soup):
        valuation_tag = soup.find('div', class_='rating-value')
        return valuation_tag.find('div', class_='value').get_text(strip=True) if valuation_tag else 'valuation_not_found'

    
    def check_debts(self, soup):
        description_tag = soup.find('div', class_='description')
        description_text = description_tag.get_text(strip=True) if description_tag else ''
        return 'não há débitos tributários' not in description_text.lower()
    
    def extract_description(self, soup):
        description_tag = soup.find('div', class_='description')
        return description_tag.get_text(strip=True) if description_tag else 'description_not_found'

    # Function to save the extracted data into DynamoDB
    def save_to_dynamodb(self, data):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('scraping-auction-items')

        # Prepare the data to be stored as a Map in DynamoDB
        item = {
            'id': data['id'],
            'auction_id': data['process'],  # Assuming 'process' can be used as a unique identifier
            'auction_data': {
                'title': data['title'],
                'images': data['images'],  # List of image URLs
                'location': data['location'],
                'jurisdiction': data['jurisdiction'],
                'forum': data['forum'],
                'author': data['author'],
                'defendant': data['defendant'],
                'process': data['process'],
                'control': data['control'],
                'lot_number': data['lot_number'],
                'last_bid': data['last_bid'],
                'increment': data['increment'],
                'auction_dates': {
                    'first_auction': data['auction_dates']['first_auction'],
                    'second_auction': data['auction_dates']['second_auction']
                },
                'valuation': data['valuation'],
                'description': data['description'],
                'pendencies': data['pendencies'],
                'taxes': data['taxes'],
                'debts': data['debts'],
                'annotations': data['annotations']
            }
        }

        # Save the data to DynamoDB as a Map structure
        try:
            response = table.put_item(Item=item)
            print("Data successfully saved to DynamoDB!")
            return response
        except Exception as e:
            print(f"Error saving to DynamoDB: {str(e)}")
            return None

    def collect_data(self, url: str):
        soup : Tag = self.get_body_or_throw(self.get_service().fetch_detail_page(url=url))
        print(soup)
        data = {
            'id': str(uuid.uuid4()),
            'title': self.extract_title(soup),
            'images': self.extract_images(soup),
            'location': self.extract_location(soup),
            'jurisdiction': self.extract_jurisdiction(soup),
            'forum': self.extract_forum(soup),
            'author': self.extract_author(soup),
            'defendant': self.extract_defendant(soup),
            'process': self.extract_process(soup),
            'control': self.extract_control(soup),
            'lot_number': self.extract_lot_number(soup),
            'last_bid': self.extract_last_bid(soup),
            'increment': self.extract_increment(soup),
            'auction_dates': self.extract_auction_dates(soup),
            'valuation': self.extract_valuation(soup),
            'description': self.extract_description(soup),
            'pendencies': False,
            'taxes': False,
            'debts': False,
            'annotations': False
        }
        
        return data

    def do_fetch(self, page: int, type: str) -> Tag:
        site = self.get_body_or_throw(self.get_service().fetch_page(page=page,type=type))
        return site
    
    def do_fetch_details(self, url: str) -> Tag:
        details = self.get_body_or_throw(self.get_service().fetch_detail_page(url=url))
        return details
    
    def read_tags_from_details(self, site: Tag) -> HouseDetail:
         # # HTML da notícia
        size = site.find_all('div', attrs={'class': 'item'})[0].text
        author = site.find('div', attrs={'class': 'author item'})
        principal = author.find_all('div', attrs={'class': 'value'})[0].text
        auctioneer = author.find('div', attrs={'class': 'value'}).find_all_next('div', attrs={'class': 'value'})[0].text
        auction_id = site.find('div', attrs={'class': 'auction-id'}).find_all_next('div', attrs={'class': 'value'})[0].text    

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
                           number_address=number_address, neighborhood_address=neighborhood_address, city_address=city_address,state_address= state_address)

    def read_tags_from_site(self, site: Tag, category: str) -> List[House]:
         # # HTML da notícia
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
    