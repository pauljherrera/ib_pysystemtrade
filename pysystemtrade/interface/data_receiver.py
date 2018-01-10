import os
import sys
import pandas as pd
import numpy as np
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from pysystemtrade.interface.ib_data import ib_Data
from pysystemtrade.systems.provided.example.rules import ewmac_forecast_with_defaults as ewmac
from pysystemtrade.systems.forecasting import Rules
from pysystemtrade.systems.basesystem import System
from pysystemtrade.sysdata.configdata import Config

from ib.data_feeder import IBfeeder_pst_adapter
from ib.historical_data import IBHistoricalData
from utils import pub_sub



class DataReceiver(pub_sub.Subscriber):
    def __init__(self, hist_data=None, *args, **kwargs):
        """
        :param hist_data: ib.historical_data.IBHistoricalData instance
        """
        super().__init__(*args, **kwargs)
        if hist_data:
            self.hist_data = hist_data
        
            
    def update(self, message):
        data = self.get_data(message)
        # Ib data Object. This is the Object that manage the data from ibAPI. 
        conector = ib_Data(data)
    
        # create a list with the instruments for the config object
        systemInstruments = list(conector.get_portfolio(data))
        
        my_config = Config()  # create a config object.
    
        # Set the instrument of the system via the config.
        my_config.instruments = systemInstruments
    
        my_rules = Rules(dict(ewmac=ewmac))
        my_rules.trading_rules()
    
        my_system = System([my_rules], conector, my_config)
    
        # Forecast for each instrument.
        for i in message.keys():
            print("\n{} forecast:\n".format(i))
            forecast = my_system.rules.get_raw_forecast(i, "ewmac")
            print(forecast.tail(10), '\n')
            
            
    def get_data(self, live_data):
        """
        Concatenates the historical data with the live data.
        :param live_data: dict with instrument names as keys and pd.Dataframe
                          as values.
        :return: dict with instrument names as keys and pd.Dataframe
                 as values.
        """
        data = {}
        for k in live_data.keys():
            df_1 = self.hist_data.instruments_data[k].set_index('date')[['close']]
            concatenated = pd.concat([df_1, live_data[k]], axis=0)
            data[k] = concatenated.groupby(concatenated.index).last()
        
        return data
        


if __name__ == '__main__':
    instruments = ['USDJPY', 'EURGBP']
    data_feeder = IBfeeder_pst_adapter(instruments=instruments, timeframe=1)
    hist_data = IBHistoricalData(instruments=instruments, timeframe=1,
                                 duration='1 D')
    subscriber = DataReceiver(hist_data=hist_data)
    data_feeder.pub.register('pysystemtrade_data', subscriber)
    
    
    
    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass



