#!/usr/bin/python3

# from brownie import MyCollectible,network,accounts,config
from dataclasses import replace
from metadata import sample_metadata

from pathlib import Path
import os
import requests
import json
from dotenv import load_dotenv
from urllib.parse import urlparse
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import time
from urllib.parse import urlparse

import textwrap
import brownie.project as project
from brownie import *

OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"

load_dotenv()

def main(kunci,akses,file_loc,name,des,webs,file_extention,reg_date,exp_date,creator_name,artist_name,fcreated_date): 
    



    dev = accounts.add(kunci)
    print(f"ini dev : {dev}")
    print(f"network now : {network.show_active()}")
    the_collectible = Contract("0xab38F479fFbDC478D6083D5FE09078a46dfb8C93") 
    print(f"Ini contract address nya : {the_collectible}")
    token_id = the_collectible.tokenCounter()
    print(f"token id : {token_id}")

    try:
        if akses=="image":
            return_metadata = write_image_metadata(token_id,file_loc,name,des,webs,file_extention)
            print(f"return metadanya : {return_metadata}")
        elif akses=="domain":
            return_metadata = write_domain_metadata(token_id,name,des,webs,reg_date,exp_date)
            print(f"return metadanya : {return_metadata}")
        elif akses=="video":
            return_metadata = write_video_metadata(token_id,file_loc,name,des,webs,file_extention,creator_name)
            print(f"return metadanya : {return_metadata}")
        elif akses=="sound":
            return_metadata = write_sound_metadata(token_id,file_loc,name,des,webs,file_extention,creator_name,artist_name)
            print(f"return metadanya : {return_metadata}")
        elif akses=="document":
            return_metadata = write_document_metadata(token_id,file_loc,name,des,webs,file_extention,fcreated_date)
            print(f"return metadanya : {return_metadata}")
        elif akses=="other":
            return_metadata = write_other_metadata(token_id,file_loc,name,des,webs,file_extention)
            print(f"return metadanya : {return_metadata}")
    except Exception as e:
        return ("ERROR on Metadata"+str(e))
    
    try:
        transaction = the_collectible.createCollectible((f"{return_metadata}"), {"from": dev})
        transaction.wait(2)
    except Exception as e:
        return ("ERROR on Ethereum"+str(e))


    kalimatfull = ("{}".format(OPENSEA_FORMAT.format(the_collectible.address, token_id)))
                           # show_popup("<a href=http://google.com>Google</a>")
    print(kalimatfull)
    return kalimatfull

def write_metadata(token_id,name,des): #tdnya ada token_ids ganti jd token id

        collectible_metadata = sample_metadata.metadata_template

        metadata_file_name = (
            "./metadata/{}/".format(network.show_active())
            + str(token_id)   #ya token id aja
            + "-"
            + name  #ganti jd nama file nya 
            + ".json"
        )
        if 1==2: 
            print(
                "{} already found, delete it to overwrite!".format(
                    metadata_file_name)
            )
        else:
            print("Creating Metadata file: " + metadata_file_name)
            collectible_metadata["name"] =  name
            collectible_metadata["description"] = des
            image_to_upload = None

            image_path = "./img/{}.png".format(       #nanti get alamat dari form UI
                name.lower().replace('_', '-'))
            image_to_upload = upload_to_ipfs(image_path)      #upload Image nya ke IPFS

            # image_to_upload = (
            #     breed_to_image_uri[breed] if not image_to_upload else image_to_upload
            # )

            collectible_metadata["image"] = image_to_upload
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)

            return upload_to_ipfs(metadata_file_name)          #upload JSON nya ke IPFS


###################################################
                          #(akses,file_loc,name,des,webs,file_extention,"reg_date","exp_date","creator_name","artist_name","fcreated_date")
def write_image_metadata(token_id,file_loc,name,des,webs,file_extention):

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

    image_path = (f"{file_loc}")       #nanti get alamat dari form UI

    image_to_upload = upload_to_ipfs(image_path)      #upload Image nya ke IPFS
    collectible_metadata["image"] = image_to_upload
    collectible_metadata["image_data"] = image_to_upload
    collectible_metadata["external_url"] = webs
    collectible_metadata["image_file_type"] = file_extention
    collectible_metadata["model_file_type"] = file_extention


    with open(metadata_file_name, "w") as file:
        json.dump(collectible_metadata, file)
    if os.getenv("UPLOAD_IPFS") == "true":
        return upload_to_ipfs(metadata_file_name)          #upload JSON nya ke IPFS


###################################################
                         #(akses,"file_loc",name,des,webs,"file_extention",reg_date,exp_date,"creator_name","artist_name","fcreated_date")
def write_domain_metadata(token_id,name,des,webs,reg_date,exp_date):

    collectible_metadata = sample_metadata.domain_template
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


    parsed = urlparse(f'{webs}')
    domain = parsed.netloc.split(".")[-2:]
    hostname = domain[0]
    domainnya= domain[1]

    create_back((hostname+"."+domainnya),"","domain")

    image_path = ("./img/cover.png")       #nanti get alamat dari form UI
    image_to_upload = upload_to_ipfs(image_path)      #upload Image nya ke IPFS

    collectible_metadata["url"] = webs
    collectible_metadata["attributes"][1]["value"]= reg_date
    collectible_metadata["attributes"][2]["value"]= exp_date
    collectible_metadata["background_image"] = image_to_upload
    collectible_metadata["image_url"] = image_to_upload


    with open(metadata_file_name, "w") as file:
        json.dump(collectible_metadata, file)
    if os.getenv("UPLOAD_IPFS") == "true":
        return upload_to_ipfs(metadata_file_name)          #upload JSON nya ke IPFS


################################################### 
                          #(akses,file_loc,name,des,webs,file_extention,"reg_date","exp_date",creator_name,"artist_name","fcreated_date")
def write_video_metadata(token_id,file_loc,name,des,webs,file_extention,creator_name):

    collectible_metadata = sample_metadata.video_template
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

    image_path = (f"{file_loc}")       #nanti get alamat dari form UI
    image_to_upload = upload_to_ipfs(image_path)      #upload Image nya ke IPFS

    create_back(name,"Video creator name : "+creator_name,"video")
    backau_path = ("./img/cover.png")       #nanti get alamat dari form UI
    backau_to_upload = upload_to_ipfs(backau_path)      #upload Image nya ke IPFS

    collectible_metadata["image"] = backau_to_upload
    collectible_metadata["external_url"] = webs
    collectible_metadata["creator_name"] = creator_name
    collectible_metadata["image_file_type"] = file_extention
    collectible_metadata["model_file_type"] = file_extention
    collectible_metadata["animation_url"] = image_to_upload


    with open(metadata_file_name, "w") as file:
        json.dump(collectible_metadata, file)
    if os.getenv("UPLOAD_IPFS") == "true":
        return upload_to_ipfs(metadata_file_name)          #upload JSON nya ke IPFS


################################################### 
                         #(akses,file_loc,name,des,webs,file_extention,"reg_date","exp_date",creator_name,artist_name,"fcreated_date")
def write_sound_metadata(token_id,file_loc,name,des,webs,file_extention,creator_name,artist_name):
    collectible_metadata = sample_metadata.audio_template
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

    image_path = (f"{file_loc}")       #nanti get alamat dari form UI
    image_to_upload = upload_to_ipfs(image_path)      #upload Image nya ke IPFS

    create_back(name,"Audio creator name : "+creator_name,"sound")
    backau_path = ("./img/cover.png")       #nanti get alamat dari form UI
    backau_to_upload = upload_to_ipfs(backau_path)      #upload Image nya ke IPFS

    collectible_metadata["image"] = backau_to_upload
    collectible_metadata["external_url"] = webs
    collectible_metadata["creator_name"] = creator_name
    collectible_metadata["image_file_type"] = file_extention
    collectible_metadata["model_file_type"] = file_extention
    collectible_metadata["animation_url"] = image_to_upload
    collectible_metadata["audio_url"] = image_to_upload
    collectible_metadata["artist_name"] = artist_name


    with open(metadata_file_name, "w") as file:
        json.dump(collectible_metadata, file)
    if os.getenv("UPLOAD_IPFS") == "true":
        return upload_to_ipfs(metadata_file_name)          #upload JSON nya ke IPFS


################################################### 
                             #(akses,file_loc,name,des,webs,file_extention,"reg_date","exp_date","creator_name","artist_name",fcreated_date)
def write_document_metadata(token_id,file_loc,name,des,webs,file_extention,fcreated_date):

    collectible_metadata = sample_metadata.document_template
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

    image_path = (f"{file_loc}")       #nanti get alamat dari form UI
    image_to_upload = upload_to_ipfs(image_path)      #upload Image nya ke IPFS

    create_back(name,"Original document file created on :\n"+(datetime.utcfromtimestamp(fcreated_date).strftime('%Y-%m-%d %H:%M:%S'))+" UTC","document")
    backau_path = ("./img/cover.png")       #nanti get alamat dari form UI
    backau_to_upload = upload_to_ipfs(backau_path)      #upload Image nya ke IPFS

    collectible_metadata["image"] = backau_to_upload
    collectible_metadata["external_url"] = webs
    collectible_metadata["url"] = image_to_upload
    collectible_metadata["image_file_type"] = file_extention
    collectible_metadata["model_file_type"] = file_extention
    collectible_metadata["attributes"][0]["value"]= fcreated_date




    with open(metadata_file_name, "w") as file:
        json.dump(collectible_metadata, file)
    if os.getenv("UPLOAD_IPFS") == "true":
        return upload_to_ipfs(metadata_file_name)          #upload JSON nya ke IPFS


################################################### 
                          #(akses,file_loc,name,des,webs,file_extention,"reg_date","exp_date","creator_name","artist_name","fcreated_date")
def write_other_metadata(token_id,file_loc,name,des,webs,file_extention):
    # "name": "",
    # "description": "",
    # "background_color":"fbbc05",
    # "image": "",
    # "url":"",
    # "external_url":"",
    # "image_file_type":"mp4",
    # "model_file_type":"mp4"
    collectible_metadata = sample_metadata.other_template
    metadata_file_name = (
            "./metadata/{}/".format(network.show_active())
            + str(token_id)   #ya token id aja
            + "-"
            + name.lower().replace('_', '-').replace(' ', '-')  #ganti jd nama file nya 
            + ".json"
        )
    print("Creating Metadata file : " + metadata_file_name)
    collectible_metadata["name"] =  name
    collectible_metadata["description"] = des

    image_path = (f"{file_loc}")       #nanti get alamat dari form UI
    image_to_upload = upload_to_ipfs(image_path)      #upload Image nya ke IPFS

    create_back(name,"File extention : "+file_extention,"other")
    backau_path = ("./img/cover.png")       #nanti get alamat dari form UI
    backau_to_upload = upload_to_ipfs(backau_path)      #upload Image nya ke IPFS

    # collectible_metadata["image"] = image_to_upload
    collectible_metadata["external_url"] = webs
    collectible_metadata["url"] = image_to_upload
    collectible_metadata["image_file_type"] = file_extention
    collectible_metadata["model_file_type"] = file_extention
    collectible_metadata["image"] = backau_to_upload

    with open(metadata_file_name, "w") as file:
        json.dump(collectible_metadata, file)
    if os.getenv("UPLOAD_IPFS") == "true":
        return upload_to_ipfs(metadata_file_name)          #upload JSON nya ke IPFS

def upload_to_ipfs(filepath):
    PINATA_BASE_URL = 'https://api.pinata.cloud/'
    endpoint = 'pinning/pinFileToIPFS'
    filename = filepath.split("/")[-1:][0]
    filename = filename.replace(" ","-")
    headers = {'pinata_api_key': os.getenv('PINATA_API_KEY'),
           'pinata_secret_api_key': os.getenv('PINATA_API_SECRET')}
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(PINATA_BASE_URL + endpoint,
                                files={"file": (filename, image_binary)},
                                headers=headers)
    print(response.json())
    ipfs_hash = response.json()["IpfsHash"]
    image_uri = "https://gateway.pinata.cloud/ipfs/{}?filename={}".format(ipfs_hash,filename)
    return image_uri 


def create_back(line1,line2,jenis):
    # get an image
    if jenis=="domain":
        base = Image.open(r'.\img\backdomain.png').convert('RGBA')
    elif jenis=="sound":
        base = Image.open(r'.\img\backaudio.png').convert('RGBA')
    elif jenis=="video":
        base = Image.open(r'.\img\backvideo.png').convert('RGBA')
    elif jenis=="document":
        base = Image.open(r'.\img\backdocument.png').convert('RGBA')
    elif jenis=="other":
        base = Image.open(r'.\img\backother.png').convert('RGBA')

    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', base.size, (255,255,255,0))
    # get a font
    fnt = ImageFont.truetype(r'.\img\roboto500.ttf', 40)
    fnt2 = ImageFont.truetype(r'D:\Collage\Smster8\pillow\roboto500.ttf', 20)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    baris1 = textwrap.fill(text=f"{line1}", width=20)
    # draw text, full opacity
    d.text((36,60), f"{baris1}", font=fnt, fill=(128,128,128,255))
    out = Image.alpha_composite(base, txt)

    if line2 != "":
        d.text((36,440), line2, font=fnt2, fill=(128,128,128,255))
        out = Image.alpha_composite(base, txt)

    out.save(r'.\img\cover.png')