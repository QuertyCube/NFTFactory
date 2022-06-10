import brownie.project as project
from brownie import *
# project.load(r'D:\Collage\ScriptSweat\Proj\NFTFactory')
OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"

p = project.load(r'D:\Collage\ScriptSweat\Proj\NFTFactory', name="NftfactoryProject")
p.load_config()

dev = accounts.add("13e4b91edf3a14ddb2793b6ac01be5155b5b2e56ea3cdf3ec59752121061a77a")
print(f"ini dev : {dev}")
network.connect('rinkeby')
print(f"network now : {network.show_active()}")
the_collectible = p.MyCollectible.at("0x411703674217d706D055a4740771dc62C0c27054")  #(MyCollectible[len(MyCollectible) - 1])#("0xc13e7bAD43A9A4ad813D3a619c46a58D38f49f3c") # MyCollectible[len(MyCollectible) - 1]
print(f"Ini contract address nya : {the_collectible}")
token_id = the_collectible.tokenCounter()
print(f"token id : {token_id}")

transaction = the_collectible.createCollectible(("https://ipfs.io/ipfs/QmYFNrFs4EBUS7LZ2cKJY4DxK6aT4kPJLcZiv1d8DE6bRU?filename=54-f.json"), {"from": dev})
transaction.wait(1)

kalimatfull = ("{}".format(OPENSEA_FORMAT.format(the_collectible.address, token_id)))
                        # show_popup("<a href=http://google.com>Google</a>")
print(kalimatfull)