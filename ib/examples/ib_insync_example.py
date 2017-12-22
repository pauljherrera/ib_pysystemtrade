# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 17:57:50 2017

@author: paulj
"""

from ib_insync import *
import pandas as pd

ib = IB()
ib.connect('127.0.0.1', 4002, clientId=10)

contract = Forex('EURUSD')

contracts = [Forex(pair) for pair in 'EURUSD USDJPY GBPUSD USDCHF USDCAD AUDUSD'.split()]

eurusd = contracts[0]

for contract in contracts:
    ib.reqMktData(contract, '', False, False)

def onBarUpdate(bars, hasNewBar):
    print(bars)

ib.setCallback('barUpdate', onBarUpdate)

bars = ib.reqRealTimeBars(contract, 5, 'MIDPOINT', False)

df = pd.DataFrame(columns='symbol bidSize bid ask askSize high low close'.split())
df['symbol'] = [c.symbol + c.currency for c in contracts]
contract2Row = {c: i for (i, c) in enumerate(contracts)}

def onPendingTickers(tickers):
    for t in tickers:
        row = contract2Row[t.contract]
        df.iloc[row, 1:] = (t.bidSize, t.bid, t.ask, t.askSize, t.high, t.low, t.close)
    print(df)        

ib.setCallback('pendingTickers', onPendingTickers)
ib.sleep(60)

order = MarketOrder('BUY', 1000)
trade = ib.placeOrder(contract, order)
ib.sleep(1)
trade.log


contract = Forex('EURUSD')
ib.qualifyContracts(contract)
order = MarketOrder('BUY', 1000, account=ib.managedAccounts()[0])
trade = ib.placeOrder(contract, order)
while not trade.isDone():
    ib.waitOnUpdate()
    
limitOrder = LimitOrder('BUY', 100, 0.05)


