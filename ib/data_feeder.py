# -*- coding: utf-8 -*-

import sys
import os
import asyncio
import ib_insync as ib

from apscheduler.schedulers.background import BackgroundScheduler

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) 
from utils import pub_sub
from ib.connection import IBConnection
import config



class IBDataFeeder(IBConnection):
    """
    Data feeder for live prices.
    Has a Publisher component that publishes the data to registered subscribers.
    """
    def __init__(self, instruments_list=None, auto_dispatch=False,
                 *args, **kwargs):
        """
        :param instrument_list: list of str containing the ticker names of
                                the instruments to be traded.
        :param auto_dispatch (optional): bool. If True, the Publisher component
               will dispatch all the data automatically.
        """
        super().__init__(*args, **kwargs)
               
        # Initializing contracts.
        self.instruments_names = []
        self.instruments_contracts = {}
        if instruments_list:
            for i in instruments_list:
                self.add_instrument(i)
        
        # Initializing events and channels.
        self.pub = pub_sub.Publisher(instruments_list)

        # Requesting live data.
        self.instruments_df = {}
        self.instruments_data = {}
        for inst in instruments_list:
            print("\nConnecting to live historical data channel for instrument: {}".format(inst))
            self.instruments_data[inst] = self.ib.reqRealTimeBars(self.instruments_contracts[inst], 
                                                                  5, 'MIDPOINT', 
                                                                  False)
                    
        # Setting event driven callbacks.
        self.ib.setCallback('barUpdate', self.onBarUpdate)
        self.auto_dispatch = auto_dispatch


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
        
        
    def onBarUpdate(self, bars, hasNewBar):
        """
        Callback method. It is called each time Interactive Brokers
        updates the data (Normally, each 5 seconds).
        
        :param bars: list of new bars data. Not used, but required by the
               IB API.
        :param hasNewBar: Not used, but required by the IB API.        
        """
        for inst in self.instruments_names:
            self.instruments_df[inst] = ib.util.df(self.instruments_data[inst])
            if self.auto_dispatch:
                self.pub.dispatch(inst, self.instruments_df[inst])
            
        
    
        
        
class IBfeeder_pst_adapter(IBDataFeeder):
    """
    Adapter for feeding data to the library pysystemtrade.
    """
    def __init__(self, timeframe=1, *args, **kwargs):
        """
        :param timeframe: int. Timeframe expressed in minutes.
        """
        super().__init__(*args, **kwargs)
        
        # Scheduling timed calls.
        self.timeframe = timeframe
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.onTimer, trigger='cron',
                          minute='*/{}'.format(timeframe))
        scheduler.start()
        
        # Adding pysystemtrade channel.
        self.pub.set_event('pysystemtrade_data')
    
    def onTimer(self):
        """
        Scheduled method. Will be called according to the timeframe set.
        """
        data = {}
        for inst in self.instruments_names:
            
           
            df = self.instruments_df[inst]
            df = df.rename(index=str, columns={"time": "date"})
            df = df.set_index('date')
            df = df.tz_localize(None)
            
            data[inst] = df.resample('{}T'.format(self.timeframe))\
                           .last()['close'].to_frame(name='close')
        self.pub.dispatch('pysystemtrade_data', data)
        

        
if __name__ == "__main__":
    # Configuration.
    instruments = config.instruments['forex'] \
                  + config.instruments['futures'] \
                  + config.instruments['stocks']
    
    # Initialization.
    data_feeder = IBfeeder_pst_adapter(instruments_list=instruments, 
                                       timeframe=1)
    
    subscriber = pub_sub.Subscriber()
    data_feeder.pub.register('pysystemtrade_data', subscriber)
    
    
    
    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
