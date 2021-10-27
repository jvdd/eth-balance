__author__ = "Jeroen Van Der Donckt"

from dataclasses import dataclass

@dataclass
class Coin:
    name: str
    symbol: str
    decimal: int

    def __hash__(self):
        return hash("__".join([self.name, self.symbol, str(self.decimal)]))

@dataclass
class Token(Coin):
    name: str
    symbol: str
    decimal: int
    contract_address: str

    def __post_init__(self):
        super().__init__(self.name, self.symbol, self.decimal)

    def __hash__(self):
        return super().__hash__() + hash(self.contract_address)

ETHEREUM = Coin("Ethereum", "ETH", 18)