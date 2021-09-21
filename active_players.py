from time import sleep
import time
import csv   
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


'''
weapon_abi = json.loads(open('../abis/weapon_abi.json').read())
market_abi = json.loads(open('../abis/market_abi.json').read())
approve_abi = json.loads(open('../abis/approve_abi.json').read())
game_abi = json.loads(open('../abis/game_abi.json').read())
weaponContract = w3.eth.contract(address=weapon_contract_address, abi=weapon_abi)
marketContract = w3.eth.contract(address=market_contract_address, abi=market_abi)
gameContract = w3.eth.contract(address=game_contract_address, abi=game_abi)
'''



addresses = []
fightMethodID = "0x8ae541cb"
def readInput(tx):
    if(tx.to == game_contract_address):
        try:
            methodID = tx.input[0:10]
            
            # decode input with ABI
            # [0] function
            # [1] {'_tokenAddress': 'ContractAddress', '_id': TOKENID, '_price': priceInWei})
        
            #decoded = w3.eth.abi.decode_abi(weapon_abi, tx.input) #or
            #decoded = gameContract.decode_function_input(tx.input)
            #function_name = decoded[0].function_identifier # slower somehow
            
            
            if(fightMethodID != methodID):
                #not a fight
                return
            else:
                #txhash = tx.hash.hex()
                sender = tx["from"]
                addresses.append(sender)

                #checking receipt is too slow
                """
                receipt = w3.eth.get_transaction_receipt(txhash)

                if(receipt.status == 1):
                    #transaction successful
                    print(c.OKGREEN,tx.hash.hex(),c.ENDC)
                    addresses.append(sender)
                else:
                    #transaction failed
                    print(c.FAIL,tx.hash.hex(),c.ENDC)
                """
                    
        except:
            pass



# inject the poa compatibility middleware to the innermost layer
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.clientVersion

#start at block 
blocknumber = 9643812       # august 1st block
endblocknumber = 11046951
timestart = time.time()

#remove duplicates with: sort active_players.txt | uniq active_players.txt > active_players_cleaned.txt

if __name__ == "__main__":
    while True:
        try: 
            block = w3.eth.getBlock(blocknumber, full_transactions=True)
        except Exception as e:
            print("couldnt get block ",blocknumber )
            blocknumber += 1    
            continue
        
        txs = block.transactions

        
        for tx in txs:
            readInput(tx)

        if(addresses != []):
            with open('active_players.txt', 'a+') as f:
                for address in addresses:
                    f.write(address+"\n")

        addresses = []
        if(blocknumber % 100 == 0):
            print(c.OKCYAN,"Next Block ", blocknumber,c.ENDC)
            print("blocks to scan: ", endblocknumber - blocknumber, "time left: ", (((endblocknumber-blocknumber) * (time.time() - timestart))/3600)/100, "hours")
            print("time for blockscan: ", (time.time() - timestart)/100)
            timestart = time.time()

        if(blocknumber >= endblocknumber):
            print("reached last block")
            print(endblocknumber)
            quit()

    
        blocknumber += 1






