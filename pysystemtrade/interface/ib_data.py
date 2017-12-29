"""Class to parse the data from ibAPI to pysystemtrade.

Avanti.
"""
import pandas as pd
import os
from pandas import read_csv

from interface.instrumentsdata import instrumentsData

from utils import pub_sub

class ib_Data(instrumentsData):
    """Get data from data_Feeder using pub_sub pattern

    Extends the isntrumentData class for a specific data source
    """
    def __init__(self,instrument):
        """Create a instrumentsData object for reading  files from quandl.
        
        inherits from instrumentsData
        
        :returns: new object
        """
    
        super().__init__()
        data = instrument
        setattr(self,"Instrument",data)

    def get_portfolio(self,instruments):
        
        portfolio = instruments.keys()
        
        return portfolio
    def get_specific_instrument(self,instrument,name):
        
       ins = instrument[name]

       return ins
    def get_instrument_list(self,instrument):

        number = len(instrument.keys())
        
        return number           

    def daily_prices(self, instrument_code):                    #This override the daily_prices of data class
        """
        Gets daily prices

        :param instrument_code: Instrument to get prices for
        :type trading_rules: str

        :returns: Tx1 pd.Series

        """
        instrprice = self.get_raw_price(instrument_code)
        

        return instrprice