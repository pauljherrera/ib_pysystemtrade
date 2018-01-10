# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 19:01:28 2017

@author: paulj
"""

import sys
import os
import numpy as np
import ib_insync as ib

from tqdm import tqdm

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) 


timeframes = {1: '1 min', 5: '5 mins', 15: '15 mins', 30: '30 min2', 
              60: '1 hour', 240: '4 hours', 480: '8 hours', 1440: '1 day',
              'w': '1 week', 'm': '1 month'}


class IBHistoricalData:
    """
    Historical data retriever.
    """
    def __init__(self, instruments=None, timeframe=1, duration='1 M',
                 host='127.0.0.1', port=4003,
                 *args, **kwargs):
        # Connecting to IB.
        self.client_id = np.random.randint(1, 500)
        self.ib = ib.IB()
        self.ib.connect(host, port, clientId=self.client_id)
        
        # Initializing variables.
        self.timeframe = timeframe
        self.duration = duration
        self.instruments_names = []
        self.instruments_contracts = {}
        self.instruments_data = {}

        # Initializing contracts.
        print('\nRetrieving historical data\n')
        if instruments:
            for i in tqdm(instruments):
                self.get_historical_data(i)
                
            
    def add_instrument(self, instrument):
        self.instruments_names.append(instrument)
        
        # Adding Forex contracts.
        contract = ib.Forex(instrument)
        self.ib.qualifyContracts(contract)
        self.instruments_contracts[instrument] = contract
        
        
    def get_historical_data(self, instrument):
        self.add_instrument(instrument)
        self.instruments_data[instrument] = ib.util.df(self.ib.reqHistoricalData(
                                              self.instruments_contracts[instrument], 
                                              endDateTime='', 
                                              durationStr=self.duration,
                                              barSizeSetting=timeframes[self.timeframe], 
                                              whatToShow='MIDPOINT', 
                                              useRTH=True))



if __name__ == "__main__":
    instruments = ['USDJPY', 'EURGBP']
    hist_data = IBHistoricalData(instruments=instruments, timeframe=5,
                                   duration='1 M')
    


