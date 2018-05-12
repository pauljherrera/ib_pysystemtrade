# -*- coding: utf-8 -*-

import sys
import os
import numpy as np
import ib_insync as ib

from tqdm import tqdm

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) 
from ib.connection import IBConnection
import config


timeframes = {1: '1 min', 5: '5 mins', 15: '15 mins', 30: '30 min2', 
              60: '1 hour', 240: '4 hours', 480: '8 hours', 1440: '1 day',
              'w': '1 week', 'm': '1 month'}


class IBHistoricalData(IBConnection):
    """
    Historical data retriever.
    """
    def __init__(self, instruments_list=None, timeframe=1, duration='1 M',
                 *args, **kwargs):
        """
        :param instrument_list: list of str containing the ticker names of
                                the instruments to be traded.
        :param timeframe: int. Timeframe expressed in minutes.
        :param duration: str. Quantity of historical data to be downloaded.
                              Examples: - '2 D': two days.
                                        - '3 Y': three years.
        """
        super().__init__(*args, **kwargs)
        
        # Initializing variables.
        self.timeframe = timeframe
        self.duration = duration
        self.instruments_names = []
        self.instruments_contracts = {}
        self.instruments_data = {}

        # Initializing contracts.
        print('\nRetrieving historical data\n')
        if instruments_list:
            for i in instruments_list:
                self.get_historical_data(i)
                
            
    def add_instrument(self, instrument):
        """
        Adds a qualified contract to self.instrument_contracts.
        :param instrument: str. Ticker of the instrument to be added.
        """
        self.instruments_names.append(instrument)
        
        # Adding Forex contracts.
        contract = ib.Forex(instrument)
        self.ib.qualifyContracts(contract)
        self.instruments_contracts[instrument] = contract
        
        
    def get_historical_data(self, instrument):
        """
        Retrieves the historical data for an instrument. Adds the data to 
        self.instruments_data.
        
        :param instrument: str. Ticker of the instrument.
        """
        self.add_instrument(instrument)
        self.instruments_data[instrument] = ib.util.df(self.ib.reqHistoricalData(
                                              self.instruments_contracts[instrument], 
                                              endDateTime='', 
                                              durationStr=self.duration,
                                              barSizeSetting=timeframes[self.timeframe], 
                                              whatToShow='MIDPOINT', 
                                              useRTH=True))


if __name__ == "__main__":
    # Configuration.
    instruments = config.instruments['forex'] \
                  + config.instruments['futures'] \
                  + config.instruments['stocks']
                  
    # Initiallization.
    hist_data = IBHistoricalData(instruments_list=instruments, 
                                 timeframe=1,
                                 duration='1 D')
    


