from dataclasses import dataclass

@dataclass
class ParamsAPI:
    def __init__(self, page: int,  type: str):
        self.page = page
        self.type = type