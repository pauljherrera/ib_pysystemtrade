"""Class to parse the data from ibAPI to pysystemtrade.

Avanti.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from pysystemtrade.interface.instrumentsdata import instrumentsData


class ib_Data(instrumentsData):
    """Get data from data_Feeder using pub_sub pattern

    Extends the isntrumentData class for a specific data source
    """
    def __init__(self, instrument, *args, **kwargs):
        """
        Deals with Interactive Brokers data. Inherits from instrumentsData.
        """
        super().__init__(*args, **kwargs)
        setattr(self,"Instruments", instrument)

    def daily_prices(self, instrument_code):
        return self.get_raw_price(instrument_code)


    def get_instruments_list(self):
        portfolio = self.Instruments.keys()
        
        return portfolio
    
    
    def get_specific_instrument(self,instrument,name):
       ins = instrument[name]

       return ins       


    def get_value_of_block_price_move(self, instrument_code):
        block_price_move = {
            'USDJPY' : 1,
            'EURGBP' : 1,
            'GBPUSD' : 1,
            'EURUSD' : 1,
        }

        return block_price_move[instrument_code]
