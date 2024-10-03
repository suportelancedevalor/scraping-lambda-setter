from typing import List
from features.mega_leilao.business.repository_aws import RepositoryAWS
import boto3

class RepositoryAWSImpl(RepositoryAWS):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table('scraping-auction-items')

    def save_to_dynamodb(self, data):
        """
        Saves the provided data to DynamoDB with the appropriate structure.
        """
        # Prepare the item to be saved to DynamoDB
        dynamodb_item = self.prepare_dynamodb_item(data)

        print(dynamodb_item)
        self.table.put_item(Item=dynamodb_item)
        

    def prepare_dynamodb_item(self, data):
        """
        Prepares the DynamoDB item based on the provided data.
        Handles missing attributes and prepares the structure for auction dates.
        """
        dynamodb_item = {
            'id': data['id'],
            'auction_data': {
                'category': data.get('category', 'not_informed'),
                'status': data.get('status', 'not_informed'),
                'title': data.get('title', 'not_informed'),
                'images': data.get('images', []),
                'location': data.get('location', 'not_informed'),
                'jurisdiction': data.get('jurisdiction', 'not_informed'),
                'forum': data.get('forum', 'not_informed'),
                'author': data.get('author', 'not_informed'),
                'defendant': data.get('defendant', 'not_informed'),
                'process': data.get('process', 'not_informed'),
                'control': data.get('control', 'not_informed'),
                'lot_number': data.get('lot_number', 'not_informed'),
                'last_bid': data.get('last_bid', 'not_informed'),
                'increment': data.get('increment', 'not_informed'),
                'auction_dates': self.prepare_auction_dates(data['auction_dates']),
                'valuation': data.get('valuation', 'not_informed'),
                'lat': data.get('lat', 'not_informed'),
                'lng': data.get('lng', 'not_informed'),
                'description': data.get('description', 'not_informed'),
                'pendencies': data.get('pendencies', False),
                'taxes': data.get('taxes', False),
                'debts': data.get('debts', False),
                'annotations': data.get('annotations', False)
            }
        }
        return dynamodb_item


    def prepare_auction_dates(self, auction_dates):
        """
        Prepares the auction_dates structure.
        If both first_instance and second_instance are not found, return an empty structure.
        """
        prepared_auction_dates = {}

        first_instance = auction_dates.get('first_instance', 'first_instance_not_found')
        second_instance = auction_dates.get('second_instance', 'second_instance_not_found')

        if first_instance != 'first_instance_not_found':
            prepared_auction_dates['first_auction_date'] = {
                'date': first_instance['date'],
                'value': first_instance['value']
            }

        if second_instance != 'second_instance_not_found':
            prepared_auction_dates['second_auction_date'] = {
                'date': second_instance['date'],
                'value': second_instance['value']
            }

        # If both are 'not_found', return an empty structure
        return prepared_auction_dates if prepared_auction_dates else []