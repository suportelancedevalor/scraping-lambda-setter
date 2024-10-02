import re
from typing import List

from features.mega_leilao.business.repository_api import RepositoryAPI
from features.mega_leilao.domain.auction import AuctionParams
from plugin.api.api_builder import ScrapingAuctionAPIBuilder
from plugin.api.base_repository import BaseRepository
import uuid
from bs4 import Tag
import boto3

class RepositoryAPIImpl(BaseRepository, RepositoryAPI):
    def __init__(self, url: str):
        super().__init__(url)

    def clean_text(self, text):
        """
        Cleans the provided text by removing unnecessary characters like newlines, excessive spaces,
        and other special characters except for numbers, periods, commas, and currency symbols.
        """
        # Remove quebras de linha e múltiplos espaços em branco
        cleaned_text = re.sub(r'\s+', ' ', text)
        
        # Remove caracteres especiais indesejados, mantendo números, letras e símbolos como R$, ., e ,
        cleaned_text = re.sub(r'[^\w\s.,R$%-]', ' ', cleaned_text).strip()
        
        return cleaned_text

    def extract_title(self, soup):
        """
        Extracts the auction title from the HTML. Looks for 'section-header' class.
        """
        title_tag = soup.find('h1', class_='section-header')
        return self.clean_text(title_tag.get_text(strip=True)) if title_tag else 'title_not_found'

    def extract_locality(self, soup):
        """
        Extracts the locality information from the HTML, looking for 'locality' class.
        """
        locality_tag = soup.find('div', class_='locality')
        return self.clean_text(locality_tag.find('div', class_='value').get_text(strip=True)) if locality_tag else 'locality_not_found'

    def extract_location(self, soup):
        """
        Extracts the location (localidade) information from the HTML, looking for the 
        'locality' class and cleans the text by removing unnecessary characters.
        """
        location_tag = soup.find('div', class_='locality')
        return self.clean_text(location_tag.find('div', class_='value').get_text(strip=True)) if location_tag else 'location_not_found'

    def extract_jurisdiction(self, soup):
        """
        Extracts jurisdiction information, looking for 'jurisdiction' class.
        """
        jurisdiction_tag = soup.find('div', class_='jurisdiction')
        return self.clean_text(jurisdiction_tag.find('div', class_='value').get_text(strip=True)) if jurisdiction_tag else 'jurisdiction_not_found'

    def extract_forum(self, soup):
        """
        Extracts forum information from the HTML, looking for 'forum' class.
        """
        forum_tag = soup.find('div', class_='forum')
        return self.clean_text(forum_tag.find('div', class_='value').get_text(strip=True)) if forum_tag else 'forum_not_found'

    def extract_author(self, soup):
        """
        Extracts the author information from the HTML, looking for 'author' class.
        """
        author_tag = soup.find('div', class_='author')
        return self.clean_text(author_tag.find('div', class_='value').get_text(strip=True)) if author_tag else 'author_not_found'

    def extract_defendant(self, soup):
        """
        Extracts the defendant (Réu) information from the HTML.
        """
        defendant_tag = soup.find('div', class_='forum', text='Réu')
        return self.clean_text(defendant_tag.find_next('div', class_='value').get_text(strip=True)) if defendant_tag else 'defendant_not_found'

    def extract_process_number(self, soup):
        """
        Extracts the process number from the HTML, looking for 'process-number' class.
        """
        process_tag = soup.find('div', class_='process-number')
        return self.clean_text(process_tag.find('div', class_='value').get_text(strip=True)) if process_tag else 'process_number_not_found'

    def extract_control(self, soup):
        """
        Extracts control information from the HTML, looking for 'process-control' class.
        """
        control_tag = soup.find('div', class_='process-control')
        return self.clean_text(control_tag.find('div', class_='value').get_text(strip=True)) if control_tag else 'control_not_found'

    def extract_last_bid(self, soup):
        """
        Extracts the last bid information from the HTML, looking for 'last-bid' class.
        """
        bid_tag = soup.find('div', class_='last-bid')
        return self.clean_text(bid_tag.find('div', class_='value').get_text(strip=True)) if bid_tag else 'last_bid_not_found'

    def extract_increment(self, soup):
        """
        Extracts the increment value from the HTML, looking for 'increment' class.
        """
        increment_tag = soup.find('div', class_='increment')
        return self.clean_text(increment_tag.find('div', class_='value').get_text(strip=True)) if increment_tag else 'increment_not_found'

    def extract_status(self, soup):
        """
        Extracts the auction status, looking for the status section in the auction information.
        """
        status_tag = soup.find('div', class_='instance-text')
        return self.clean_text(status_tag.get_text(strip=True)) if status_tag else 'status_not_found'

    def extract_first_instance(self, soup):
        """
        Extracts the first auction date from the HTML.
        """
        first_instance_tag = soup.find('span', class_='card-first-instance-date')
        return self.clean_text(first_instance_tag.get_text(strip=True)) if first_instance_tag else 'first_instance_not_found'

    def extract_second_instance(self, soup):
        """
        Extracts the second auction date from the HTML.
        """
        second_instance_tag = soup.find('span', class_='card-second-instance-date')
        return self.clean_text(second_instance_tag.get_text(strip=True)) if second_instance_tag else 'second_instance_not_found'

    def extract_valuation(self, soup):
        """
        Extracts the valuation value from a BeautifulSoup object, specifically looking for text
        within the 'rating-value' class. Cleans the extracted text by removing unnecessary spaces,
        newlines, and special characters.
        """
        valuation_tag = soup.find('div', class_='rating-value')
        
        if valuation_tag:
            valuation_text = valuation_tag.find('div', class_='value').get_text(strip=True)
            
            # Remove non-numeric characters, except for '.', ',', and 'R$'
            cleaned_valuation = re.sub(r'[^\d.,R$]', '', valuation_text)
            
            # Return cleaned valuation
            return cleaned_valuation
        
        return 'valuation_not_found'

    def extract_images(self, soup):
        """
        Extracts image URLs from the HTML, filtering only URLs that contain '/batches/' or '/bank_icons/'.
        """
        images = []
        image_tags = soup.find_all('img')
        
        for img in image_tags:
            img_url = img.get('src')
            if '/batches/' in img_url in img_url:
                images.append(img_url)
        
        return images if images else 'images_not_found'

    def extract_process(self, soup):
        """
        Extracts the process details from the HTML, looking for 'process-number' class.
        """
        process_tag = soup.find('div', class_='process-number')
        return self.clean_text(process_tag.find('a').get_text(strip=True)) if process_tag else 'process_not_found'

    def extract_lot_number(self, soup):
        """
        Extracts the lot number from the HTML, if it exists.
        """
        lot_tag = soup.find('div', class_='lot-number')
        return self.clean_text(lot_tag.get_text(strip=True)) if lot_tag else 'lot_number_not_found'

    def extract_auction_dates(self, soup):
        """
        Extracts the auction dates (both first and second instances) from the HTML.
        """
        first_instance = self.extract_first_instance(soup)
        second_instance = self.extract_second_instance(soup)
        return {
            'first_instance': first_instance,
            'second_instance': second_instance
        }

    def extract_description(self, soup):
        """
        Extracts the description of the auction lot from the HTML.
        """
        description_tag = soup.find('div', class_='description')
        return self.clean_text(description_tag.get_text(strip=True)) if description_tag else 'description_not_found'

    def collect_data(self, url: str, category: str):
        soup : Tag = self.get_body_or_throw(self.get_service().fetch_detail_page(url=url))
        status = self.extract_status(soup)
        
        if status == "Finalizado":
            return
        
        data = {
            'id': str(uuid.uuid4()),
            'category': category,
            'status': status,
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
            'lat': 'não informado',
            'lng': 'não informado',
            'pendencies': False,
            'taxes': False,
            'debts': False,
            'annotations': False
        }
        return data

    def do_fetch(self, page: int, type: str) -> Tag:
        site = self.get_body_or_throw(self.get_service().fetch_page(page=page,type=type))
        return site
    
    def read_url_from_site(self, site: Tag, category: str) -> List[AuctionParams]:
        params = []
        houses = site.findAll('div', attrs={'class': 'col-sm-6 col-md-4 col-lg-3'})
        for news in houses:
            url_detail = news.find_all('a', attrs={'class':'card-image'})[0]['href']
            params.append(AuctionParams(url=url_detail, category=category))

        return params

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
    