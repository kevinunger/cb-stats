from time import sleep
import time
import csv   
import json
from web3 import Web3, IPCProvider, WebsocketProvider, HTTPProvider
from web3.middleware import geth_poa_middleware

class c:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'  
    
weapon_contract_address = "0x7E091b0a220356B157131c831258A9C98aC8031A"
char_contract_address = "0xc6f252c2CdD4087e30608A35c022ce490B58179b"
market_contract_address = "0x90099dA42806b21128A094C713347C7885aF79e2"
skill_contract_address = "0x154A9F9cbd3449AD22FDaE23044319D6eF2a1Fab"

game_contract_address = "0x39Bea96e13453Ed52A734B6ACEeD4c41F57B2271"

ws_url = "wss://bsc.getblock.io/mainnet/?api_key="

w3 = Web3(Web3.WebsocketProvider(ws_url))
print("is connected: ",w3.isConnected())




game_abi = json.loads(open('game_abi.json').read())
gameContract = w3.eth.contract(address=game_contract_address, abi=game_abi)



# inject the poa compatibility middleware to the innermost layer
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.clientVersion

timestart = time.time()

igo_skill = 0
if __name__ == "__main__":
    with open ('active_players.txt', 'r') as f:
        for idx, address in enumerate(f):
            address = address.strip("\n")
            igo_skill_wei = gameContract.functions.getTokenRewardsFor(address).call()
            igo_skill += float(w3.fromWei(igo_skill_wei, 'ether'))

            if(idx % 500 == 1 ):
                print(igo_skill)
                print("avg: ", igo_skill/idx)
                with open('totalRewards.txt', 'w+') as f:
                    f.write("Total IGO Skill " + str(igo_skill) + " avg: " + str(igo_skill/idx)+ " checked: " + str(idx+1) +" addresses" )
            


    
        






