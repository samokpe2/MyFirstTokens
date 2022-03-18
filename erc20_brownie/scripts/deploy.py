from brownie import OkpeToken,network, config
from scripts.helpful_scripts import get_account
from web3 import Web3

initial_supply = 1000000


def main():
    account = get_account()
    okpe_token = OkpeToken.deploy(initial_supply, {"from": account}, publish_source=True)
    print(okpe_token.name())
    print(okpe_token.address)
