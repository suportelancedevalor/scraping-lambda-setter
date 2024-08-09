import requests
from typing import List

class AbstractBuilder:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def create_http_client(self):
        http_client = requests.Session()
        http_client.timeout = 5
        return http_client

    def build(self):
        raise NotImplementedError("build method must be implemented in subclass")