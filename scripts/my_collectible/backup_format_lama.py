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

def main(): #(akses,file_loc,name,des,webs,file_extention,reg_date,exp_date,creator_name,artist_name,fcreated_date)
    


    dev = accounts.add(config["wallets"]["from_key"])
    print(f"ini dev : {dev}")
    print(f"network now : {network.show_active()}")
    the_collectible = MyCollectible.at("0xc13e7bAD43A9A4ad813D3a619c46a58D38f49f3c") # MyCollectible[len(MyCollectible) - 1]
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
###################################################
                          #(akses,file_loc,name,des,webs,file_extention,"reg_date","exp_date","creator_name","artist_name","fcreated_date")
def write_image_metadata(token_id,file_loc,name,des,webs,file_extention):
    # "name": "",
    # "description": "",
    # "image": "",
    # "external_url":"https://artifex.art/3100020046",
    # "image_file_type":"mp4",
    collectible_metadata = sample_metadata.image_template
    metadata_file_name = (
            "./metadata/{}/".format(network.show_active())
            + str(token_id)   #ya token id aja
            + "-"
            + name.lower().replace('_', '-').replace(' ', '-')  #ganti jd nama file nya 
            + ".json"
        )
    print("Creating Metadata file: " + metadata_file_name)
    collectible_metadata["name"] =  name
    collectible_metadata["description"] = des

    image_to_upload = None

    if os.getenv("UPLOAD_IPFS") == "true":
        image_path = (f"{file_loc}")       #nanti get alamat dari form UI

        image_to_upload = upload_to_ipfs(image_path)      #upload Image nya ke IPFS
    collectible_metadata["image"] = image_to_upload

    collectible_metadata["external_url"] = webs
    collectible_metadata["image_file_type"] = file_extention


    with open(metadata_file_name, "w") as file:
        json.dump(collectible_metadata, file)
    if os.getenv("UPLOAD_IPFS") == "true":
        return upload_to_ipfs(metadata_file_name)          #upload JSON nya ke IPFS

###################################################
                         #(akses,"file_loc",name,des,webs,"file_extention",reg_date,exp_date,"creator_name","artist_name","fcreated_date")
def write_domain_metadata(token_id,name,des,webs,reg_date,exp_date):
    print("hello domain")
################################################### 
                          #(akses,file_loc,name,des,webs,file_extention,"reg_date","exp_date",creator_name,"artist_name","fcreated_date")
def write_video_metadata(token_id,file_loc,name,des,webs,file_extention,creator_name):
#    "name":"ARC Artifex #46 of 100",
#    "description":"Artifex 3D Sculpture of manifest by ARC",
#    "background":"ffffff",
#    "image":"https://gateway.pinata.cloud/ipfs/QmYaAw7638A4EYehWj9WXa8CE5GpYsYdXUKuEKY7UXg753", 
#    "external_url":"https://artifex.art/3100020046",
#    "creator_name":"DurkAtWork",
#    "image_file_type":"mp4",
#    "model_file_type":"mp4",
#    "animation_url":"https://gateway.pinata.cloud/ipfs/QmYaAw7638A4EYehWj9WXa8CE5GpYsYdXUKuEKY7UXg753"
    print("hello domain")
################################################### 
                         #(akses,file_loc,name,des,webs,file_extention,"reg_date","exp_date",creator_name,artist_name,"fcreated_date")
def write_sound_metadata(token_id,file_loc,name,des,webs,file_extention,creator_name,artist_name):
#    "name":"omgkirby GENESIS #860",
#    "description":"The omnd-dn art.",
#    "external_url":"https://www.notables.co",
#    "animation_url": "https://dreamers-metadata-media.s3.amazonaws.com/music/bass10-basstone3_lead18-sound1_beat8.mp3",#audionya
#    "audio_url":"https://shufflemint.mypinata.cloud/ipfs/QmZskqSMitv4ASymmy9XB24g6U2bDYM9cptDJXJH3CNRKJ",  #audionya
#    "image":"ipfs://QmfTdeN3QQ1jDmZ1kU7RWBDyQGACb9Egv18W6JRaCF3Fct", #gambarnya/animasi
#    "artist_name":"ARC",
#    "creator_name":"DurkAtWork"
    print("hello domain")
################################################### 
                             #(akses,file_loc,name,des,webs,file_extention,"reg_date","exp_date","creator_name","artist_name",fcreated_date)
def write_document_metadata(token_id,file_loc,name,des,webs,file_extention,fcreated_date):
#     "name": "",
#     "description": "",
#     "image": "",
#     "external_url":"https://artifex.art/3100020046",
#     "image_file_type":"mp4",
#       "attributes": [
#     {
#       "trait_type": "Created Date",
#       "display_type": "date",
#       "value": ""
#     }
#   ]
    print("hello domain")
################################################### 
                          #(akses,file_loc,name,des,webs,file_extention,"reg_date","exp_date","creator_name","artist_name","fcreated_date")
def write_other_metadata(token_id,file_loc,name,des,webs,file_extention):
    # "name": "",
    # "description": "",
    # "image": "",
    # "external_url":"https://artifex.art/3100020046",
    # "image_file_type":"mp4",
    print("hello domain")









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
