from brownie import MYNFT, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json
import os

breed_to_image_uri = {
    "ME": "https://ipfs.io/ipfs/QmZxQhLnHgHj3UZjnsZTLQC3Q7UCJAU7iN7htU6q9NNwnb?filename=me.jpeg",
    "ME2": "https://ipfs.io/ipfs/QmegHiqfzCS3KSLHjsuuPYR3siTHnyqayEQBXMd31cxyoZ?filename=me2.jpeg",
    "ME3": "https://ipfs.io/ipfs/QmT25tTj7rG3QsUnHiepbJcUwgZPKR8XtuPq4ge6dSHmUB?filename=me3.jpeg",
}


def main():
    mynft = MYNFT[-1]
    number_of_advanced_collectibles = mynft.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(mynft.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{breed}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An nice image of {breed} !"
            image_path = "./img/" + breed.lower().replace("_", "-") + ".jpeg"

            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "false":
                image_uri = upload_to_ipfs(image_path)
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]
            

            collectible_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)


# curl -X POST -F file=@metadata/rinkeby/0-SHIBA_INU.json http://localhost:5001/api/v0/add


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        # "./img/0-PUG.png" -> "0-PUG.png"
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
