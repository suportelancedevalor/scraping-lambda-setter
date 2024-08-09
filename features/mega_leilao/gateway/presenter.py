from abc import ABC, abstractmethod

class Presenter(ABC):
    @abstractmethod
    def get_apartment(self, page: int):
        pass
    @abstractmethod
    def get_house(self, page :int):
        pass
    @abstractmethod
    def get_shed(self, page: int):
        pass
    @abstractmethod
    def get_land(self, page: int):
        pass
    @abstractmethod
    def get_garage_deposit(self, page :int):
        pass
    @abstractmethod
    def get_plots(self, page :int):
        pass
    @abstractmethod
    def get_commercial_real_estate(self, page: int):
        pass
    @abstractmethod
    def get_rural_real_estate(self, page: int):
        pass
    @abstractmethod
    def get_rural_properties(self, page: int):
        pass
    @abstractmethod
    def get_parking_spaces(self, page: int):
        pass