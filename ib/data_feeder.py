# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 13:26:13 2017

@author: paulj
"""

import sys
import os
import numpy as np

import ib_insync as ib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) 
from utils import pub_sub

class IBDataFeeder:
    """
    Data feeder for historical and live prices.
    """
    def __init__(self, instruments=None, 
                 host='127.0.0.1', port=4002, *args, **kwargs):
        # Connecting to IB.
        self.client_id = np.random.randint(1, 100)
        self.ib = ib.IB()
        self.ib.connect(host, port, clientId=self.client_id)
        
        # Initializing contracts.
        self.instruments_names = []
        self.instruments_contracts = []
        if instruments:
            for i in instruments:
                self.add_instrument(i)
        
#        self.pub = pub_sub.Publisher()

    def add_instrument(self, instrument):
        self.instruments_names.append(instrument)
        
        # Adding Forex contracts.
        contract = ib.Forex(instrument)
        self.ib.qualifyContracts(contract)
        self.instruments_contracts.append(contract)
        
    
        
        
class IBfeeder_pst_adapter(IBDataFeeder):
    """
    Adapter for feeding data to the library pysystemtrade.
    """
    pass
        
        
if __name__ == "__main__":
    instruments = ['EURUSD']
    data_feeder = IBDataFeeder(instruments)
