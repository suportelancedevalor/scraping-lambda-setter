from abc import ABC, abstractmethod

class RepositoryAWS(ABC):
    @abstractmethod
    def save_to_dynamodb(self, data):
        pass