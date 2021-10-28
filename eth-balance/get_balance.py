
__author__ = "Jeroen Van Der Donckt"

import requests
import collections, functools, operator

from eth_token import ETHEREUM, Token
from pycoingecko import CoinGeckoAPI

# Create the globals

cg = CoinGeckoAPI()

API_KEYS = {}
ETHERSCAN_URL = "https://api.etherscan.io/api?module=account"

# ------------------------------------------------------------------------------------ #

def _read_api_keys() -> dict:
    api_keys = {}
    with open("keys.txt", "r") as f:
        line = f.readline().strip()
        api, key = line.split("=")
        api_keys[api] = key
    return api_keys

def initialize():
    global API_KEYS
    API_KEYS = _read_api_keys()

# ------------------------------------------------------------------------------------ #

def get_eth_balance(address: str) -> float:
    global API_KEYS
    url = ETHERSCAN_URL + f"&action=balance&address={address}&tag=latest&apikey={API_KEYS['ETHERSCAN']}"
    amount = str(requests.get(url).json()["result"])
    return float(amount[:-18] + "." + amount[-18:])

def get_erc20_contracts(address: str):
    global API_KEYS
    url = ETHERSCAN_URL + f"&action=tokentx&address={address}&sort=asc&apikey={API_KEYS['ETHERSCAN']}"
    txs = requests.get(url).json()["result"]
    tokens = set()
    for tokentx in txs:
        token = Token(tokentx["tokenName"], tokentx["tokenSymbol"], int(tokentx["tokenDecimal"]), tokentx["contractAddress"])
        tokens.add(token)
    return tokens

def get_erc20_balances(address: str):
    global API_KEYS
    tokens = get_erc20_contracts(address)
    url = ETHERSCAN_URL + f"&action=tokenbalance"
    token_balance = {}
    for token in tokens:
        c_url = url + f"&contractaddress={token.contract_address}&address={address}&tag=latest&apikey={API_KEYS['ETHERSCAN']}"
        amount = str(requests.get(c_url).json()["result"])
        amount = float(amount[:-token.decimal] + "." + amount[-token.decimal:])
        token_balance[token] = amount
    return token_balance

# ------------------------------------------------------------------------------------ #

def get_price(name: str, currency="usd") -> float:
    name = name.lower().replace("token", "").replace(" ","-").strip()
    try:
        return cg.get_price(ids=name, vs_currencies=currency)[name][currency]
    except:
        return 0

def get_balance(address: str) -> dict:
    balance = {}
    balance[ETHEREUM] = get_eth_balance(address)
    balance.update(get_erc20_balances(address))
    for token in balance.keys():
        balance[token] = (balance[token], get_price(token.name))
    return balance

def print_balance(balance: dict):
    print(f"ETH Balance: {balance[ETHEREUM][0]:.6f} - ${balance[ETHEREUM][0]*balance[ETHEREUM][1]:.2f}")
    tokens = [k for k in balance.keys() if balance[k][0] > 0 and k != ETHEREUM]
    if not len(tokens):
        return
    print("Tokens:")
    for token in tokens:
        amount, value = balance[token]
        print(" "*6 + f"{token.symbol:<5}: {amount:.6f} - ${amount*value:.2f}")

def get_total(balance: dict):
    total = 0
    for token in balance.keys():
        if balance[token] > 0:
            total += get_price(token.name) * balance[token]
    return total


if __name__ == "__main__":
    # Initialize the globals
    initialize()
    # Read the addresses
    addresses = []
    with open("addresses.txt", "r") as f:
        for line in f.readlines():
            addresses.append(line.strip())

    # Print the balances for the addresses
    total_balance = {}
    for address in addresses:
        print("Address:", address)
        balance = get_balance(address)
        print_balance(balance)
        for k in balance.keys():
            if k in total_balance.keys():
                total_balance[k] = (total_balance[k][0] + balance[k][0], balance[k][1])
            else:
                total_balance[k] = balance[k]
        print()

    # Print the totals
    print("Combined")
    print_balance(total_balance)
    print()
    total = sum(v[0]*v[1] for v in total_balance.values())
    print(f"TOTAL: ${total:.2f}")