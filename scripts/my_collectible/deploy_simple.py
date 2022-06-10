#!/usr/bin/python3
import os
from brownie import MyCollectible, accounts, network, config


def main():
    # dev = accounts.add(config["wallets"]["from_key"])
    dev = accounts.add("13e4b91edf3a14ddb2793b6ac01be5155b5b2e56ea3cdf3ec59752121061a77a")
    print(network.show_active())
    publish_source = True if os.getenv("ETHERSCAN_TOKEN") else False
    MyCollectible.deploy({"from": dev}, publish_source=publish_source)
