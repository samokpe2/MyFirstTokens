from brownie import MYNFT
from scripts.helpful_scripts import fund_with_link, get_account
from web3 import Web3


def main():
    account = get_account()
    mynft = MYNFT[-1]
    fund_with_link(mynft.address, amount=Web3.toWei(0.1, "ether"))
    creation_transaction = mynft.createCollectible({"from": account})
    creation_transaction.wait(1)
    print("Collectible created!")
