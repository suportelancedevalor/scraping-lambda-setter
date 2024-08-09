
from dataclasses import dataclass

@dataclass
class InstanceHouse:
    def __init__(self, active: str="não informado", value: str="não informado"):
        self.active = active
        self.value = value