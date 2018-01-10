# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 13:26:13 2017

@author: paulj
"""

import sys
import os
import asyncio
import numpy as np
import ib_insync as ib

from apscheduler.schedulers.background import BackgroundScheduler

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) 
from utils import pub_sub



class IBDataFeeder:
    """
    Data feeder for live prices.
    """
    def __init__(self, instruments=None, 
                 host='127.0.0.1', port=4003, auto_dispatch=False,
                 *args, **kwargs):
        # Connecting to IB.
        self.client_id = np.random.randint(1, 500)
        self.ib = ib.IB()
        self.ib.connect(host, port, clientId=self.client_id)
        
        # Initializing contracts.
        self.instruments_names = []
        self.instruments_contracts = {}
        if instruments:
            for i in instruments:
                self.add_instrument(i)
        
        # Initializing events and channels.
        self.pub = pub_sub.Publisher(instruments)

        # Requesting live data.
        self.instruments_df = {}
        self.instruments_data = {}
        for inst in instruments:
            print("\nConnecting to live historical data channel for instrument: {}".format(inst))
            self.instruments_data[inst] = self.ib.reqRealTimeBars(self.instruments_contracts[inst], 
                                                                  5, 'MIDPOINT', 
                                                                  False)
                    
        # Setting event driven callbacks.
        self.ib.setCallback('barUpdate', self.onBarUpdate)
        self.auto_dispatch = auto_dispatch


    def add_instrument(self, instrument):
        self.instruments_names.append(instrument)
        
        # Adding Forex contracts.
        contract = ib.Forex(instrument)
        self.ib.qualifyContracts(contract)
        self.instruments_contracts[instrument] = contract
        
        
    def onBarUpdate(self, bars, hasNewBar):
        for inst in self.instruments_names:
            self.instruments_df[inst] = ib.util.df(self.instruments_data[inst])
            #print("\n{}\n".format(inst))
            #print(self.instruments_df[inst].tail(10))
            if self.auto_dispatch:
                self.pub.dispatch(inst, self.instruments_df[inst])
            
        
    
        
        
class IBfeeder_pst_adapter(IBDataFeeder):
    """
    Adapter for feeding data to the library pysystemtrade.
    """
    def __init__(self, timeframe=1, *args, **kwargs):
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
        data = {}
        for inst in self.instruments_names:
            df = self.instruments_df[inst].set_index('time')
            data[inst] = df.resample('{}T'.format(self.timeframe))\
                           .last()['close'].to_frame(name='close')
        self.pub.dispatch('pysystemtrade_data', data)
        

        
        

        
if __name__ == "__main__":
    instruments = ['USDJPY', 'EURGBP']
    data_feeder = IBfeeder_pst_adapter(instruments=instruments, timeframe=1)
    
    subscriber = pub_sub.Subscriber()
    data_feeder.pub.register('pysystemtrade_data', subscriber)
    
    
    
    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
