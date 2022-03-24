from brownie import network, MYNFT
from scripts.helpful_scripts import OPENSEA_URL, get_breed, get_account

dog_metadata_dic = {
    "ME": "https://ipfs.io/ipfs/QmVKWzmG7bRfBursq1rqPuMc2Tmf3vzoH9gXX8xkxPGm17?filename=ME.json",
    "ME2": "https://ipfs.io/ipfs/QmegHiqfzCS3KSLHjsuuPYR3siTHnyqayEQBXMd31cxyoZ?filename=ME2.json",
    "ME3": "https://ipfs.io/ipfs/QmU4a1NTLn8GKPW7y6Sv7XXd8NqDAAEmKbmnWv5SFNdnGf?filename=ME3.json",
}


def main():
    print(f"Working on {network.show_active()}")
    mynft = MYNFT[-1]
    number_of_collectibles = mynft.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds")
    for token_id in range(number_of_collectibles):
        breed = get_breed(mynft.tokenIdToBreed(token_id))
        if not mynft.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id, mynft, dog_metadata_dic[breed])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button")
