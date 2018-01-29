# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import numpy as np
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from pysystemtrade.interface.ib_data import ib_Data
from pysystemtrade.interface.data_receiver import DataReceiver
from pysystemtrade.private.rules import ewmac_forecast_with_defaults as ewmac
from pysystemtrade.systems.forecasting import Rules
from pysystemtrade.systems.basesystem import System
from pysystemtrade.sysdata.configdata import Config
from systems.forecast_combine import ForecastCombine
from systems.forecast_scale_cap import ForecastScaleCap
from systems.rawdata import RawData
from systems.positionsizing import PositionSizing
from systems.portfolio import Portfolios
from systems.account import Account

from ib.data_feeder import IBfeeder_pst_adapter
from ib.historical_data import IBHistoricalData
from ib.trader import IBTrader
from ib.connection import get_ib_connection
from utils import pub_sub
import config



if __name__ == '__main__':
    # Configuration.
    instruments_dict = config.instruments
    instruments = instruments_dict['forex'] \
                  + instruments_dict['futures'] \
                  + instruments_dict['stocks']
    timeframe = config.TIMEFRAME
    duration = config.HIST_DATA_DURATION
    account = config.ACCOUNT
    buffer = config.BUFFER
                  
    # Initiallizing components.
    ib_connection = get_ib_connection()
    data_feeder = IBfeeder_pst_adapter(instruments_list=instruments, 
                                       timeframe=timeframe, 
                                       ib_connection=ib_connection)
    hist_data = IBHistoricalData(instruments_list=instruments, 
                                 timeframe=timeframe,
                                 duration=duration, 
                                 ib_connection=ib_connection)
    data_receiver = DataReceiver(instruments_list=instruments,
                                 hist_data=hist_data)
    trader = IBTrader(instruments_dict=instruments_dict, account=account,
                      ib_connection=ib_connection)
    
    # Subscribing components.
    data_feeder.pub.register('pysystemtrade_data', data_receiver)
    for i in instruments:
        data_receiver.pub.register(i, trader)
    
    
    
    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass

