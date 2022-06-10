#!/usr/bin/python3

from brownie import MyCollectible,network,accounts,config
from metadata import sample_metadata

from pathlib import Path
import os
import requests
import json
from dotenv import load_dotenv
import time


# from scripts.helpful_scripts import OPENSEA_FORMAT

# sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=name.json"
OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"

load_dotenv()

def main(kunci, jenis_form,nama,deskrip,webs,s):
    
#brownie run scripts/my_collectible/create_collectible.py
    # dev = accounts.add(config["wallets"]["from_key"])
    dev = accounts.add("13e4b91edf3a14ddb2793b6ac01be5155b5b2e56ea3cdf3ec59752121061a77a")
    print(f"ini dev : {dev}")
    print(nama)
    print(f"network now : {network.show_active()}")
    #lama
    the_collectible = MyCollectible.at("0xab38F479fFbDC478D6083D5FE09078a46dfb8C93") # MyCollectible[len(MyCollectible) - 1]
    print(f"Ini contract address nya : {the_collectible}")
    token_id = the_collectible.tokenCounter()
    print(f"token id : {token_id}")
# #upload ipfs
#     print(
#         "The number of tokens you've deployed is: "
#         + str(token_id)
#     )
#     # write_metadata(token_id,"get from UI Form name","get description")
#     return_metadata =write_metadata(token_id,"shiba-inu","get description")
 
#     time.sleep(30)
#     #nah bingung nih ntar return nya kan banyak, blm nemu cara pisahin nya

#     transaction = the_collectible.createCollectible(return_metadata, {"from": dev})  #sample token uri nunggu dpt hasil habis write    (sample_token_uri, {"from": dev}) 
#     transaction.wait(1)
#     print(
#         "Awesome! You can view your NFT at {}".format(
#             OPENSEA_FORMAT.format(the_collectible.address, token_id)
#         )
#     )
#     print('Please wait several minutes, and hit the "refresh metadata" button')




def write_metadata(token_id,name,des): #tdnya ada token_ids ganti jd token id
    # for token_id in range(token_ids):
        collectible_metadata = sample_metadata.metadata_template
        
        # breed = get_breed(nft_contract.tokenIdToBreed(token_id))
        metadata_file_name = (
            "./metadata/{}/".format(network.show_active())
            + str(token_id)   #ya token id aja
            + "-"
            + name  #ganti jd nama file nya 
            + ".json"
        )
        if 1==2: #Path(metadata_file_name).exists():
            print(
                "{} already found, delete it to overwrite!".format(
                    metadata_file_name)
            )
        else:
            print("Creating Metadata file: " + metadata_file_name)
            collectible_metadata["name"] =  name
            collectible_metadata["description"] = des
            image_to_upload = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_path = "./img/{}.png".format(       #nanti get alamat dari form UI
                    name.lower().replace('_', '-'))
                image_to_upload = upload_to_ipfs(image_path)      #upload Image nya ke IPFS

            # image_to_upload = (
            #     breed_to_image_uri[breed] if not image_to_upload else image_to_upload
            # )

            collectible_metadata["image"] = image_to_upload
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                return upload_to_ipfs(metadata_file_name)          #upload JSON nya ke IPFS
                

# curl -X POST -F file=@metadata/rinkeby/0-CRI.json http://localhost:5001/api/v0/add


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = (
            os.getenv("IPFS_URL")
            if os.getenv("IPFS_URL")
            else "http://localhost:5001"
        )
        response = requests.post(ipfs_url + "/api/v0/add",
                                 files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = "https://ipfs.io/ipfs/{}?filename={}".format(
            ipfs_hash, filename)
        print(image_uri)
    return image_uri
