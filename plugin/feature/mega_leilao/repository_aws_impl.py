from typing import List
from features.mega_leilao.business.repository_aws import RepositoryAWS
import boto3

class RepositoryAWSImpl(RepositoryAWS):
    client = boto3.client('dynamodb')
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table('scraping-auction-items')
    
    # Function to save the extracted data into DynamoDB
    def save_to_dynamodb(self, data):
        # Prepare the data to be stored as a Map in DynamoDB
        item = {
            'id': data['id'],
            'category': data['category'],
            'auction_data': {
                'title': data['title'],
                'images': data['images'],  # List of image URLs
                'location': data['location'],
                'category': data['category'],
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
                'lat': data['lat'],
                'lng': data['lng'],
                'description': data['description'],
                'pendencies': data['pendencies'],
                'taxes': data['taxes'],
                'debts': data['debts'],
                'annotations': data['annotations']
            }
        }

        # Save the data to DynamoDB as a Map structure
        try:
            response = self.table.put_item(Item=item)
            print("Data successfully saved to DynamoDB!")
            return response
        except Exception as e:
            print(f"Error saving to DynamoDB: {str(e)}")
            return None