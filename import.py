# -*- coding: utf-8 -*-
"""
IBAPI - Getting Options Contracts (option chain)

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time


class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self,self)
        
    def contractDetails(self, reqId, contractDetails):
        print("redID: {}, contract:{}".format(reqId,contractDetails))

def websocket_con():
    app.run()
    
app = TradingApp()      
app.connect("127.0.0.1", 7497, clientId=1)

# starting a separate daemon thread to execute the websocket connection
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1) # some latency added to ensure that the connection is established

#creating object of the Contract class - will be used as a parameter for other function calls
def usTechOpt(symbol,sec_type="AAPL",currency="USD",exchange="BOX"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.currency = currency
    contract.exchange = exchange
    contract.right = "C"
    contract.strike = 150
    contract.lastTradeDateOrContractMonth = "20220120"
    contract.multiplier = 100
    return contract 

app.reqContractDetails(100, usTechOpt("AAPL")) # EClient function to request contract details