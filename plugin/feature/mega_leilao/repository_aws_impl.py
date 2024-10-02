from typing import List
import uuid
from features.mega_leilao.business.repository_aws import RepositoryAWS
from features.mega_leilao.domain.mega_leilao_house import HouseSavedToReturn
import boto3

from features.mega_leilao.domain.mega_leilao_house_detail import HouseWithDetailToReturn

class RepositoryAWSImpl(RepositoryAWS):
    client = boto3.client('dynamodb')
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table('scraping-auction-items')
    
    def do_save(self, item: HouseWithDetailToReturn) -> HouseSavedToReturn:
        try:
            self.table.put_item(
                Item={
                    'id': str(uuid.uuid4()),
                    'batch_code': item.house.batch_code,
                    'price': item.house.price,
                    'category': item.house.category,
                    'title': item.house.title,
                    'card_locality': item.house.card_locality,
                    'street_address': item.house.street_address,
                    'number_address': item.house.number_address,
                    'neighborhood_address': item.house.neighborhood_address,
                    'city_address': item.house.city_address,
                    'state_address': item.house.state_address,
                    'status': item.house.status,
                    'auction_id': item.house.auction_id,
                    'auctioneer': item.house.auctioneer,
                    'card_image': item.house.card_image,
                    'principal': item.house.principal,
                    'size': item.house.size,
                    'enabled': item.house.enabled,
                    'lat': item.house.lat,
                    'lng': item.house.lng
                })
        except KeyError:
            statusCode = 400
            
        return HouseSavedToReturn(item)
    
