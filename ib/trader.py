# -*- coding: utf-8 -*-
import os
import sys
import asyncio

import ib_insync as ib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from ib.connection import IBConnection
from utils import pub_sub
import config


class IBTrader(IBConnection, pub_sub.Subscriber):
    """
    This class handles all the interaction with Interactive Brokers
    for trading related operations.
    """
    def __init__(self, instruments_dict, account, buffer=0.2,
                 *args, **kwargs):
        """
        :param instruments_dict: dict. Contains the market and the ticker
                                       of the traded instruments. Normally 
                                       will be pulled from a configuration
                                       file.
        :param account: str. Interactive Brokers account code. Normally will
                             be pulled from a configuration file.
        :param account: float. Buffer for a new position. If the differnce
                               between a forecast and the actual position if
                               smaller than the buffer, no new position will
                               be placed.
        """
        super().__init__(*args, **kwargs)
        self._counter = 1
        self.trades = {}
        self.contracts = {}
        self.account = account
        self._buffer = buffer
        self._contract_types = {'stock': ib.Stock,
                                'futures': ib.Future,
                                'forex': ib.Forex}
        self._positions = self.ib.portfolio()
       
        # Initializin all the contracts.
        for market in instruments_dict.keys():
            for ticker in instruments_dict[market]:
                self.contracts[ticker] = self.create_contract(ticker, market)
                    
    
    def create_contract(self, ticker, market):
        """
        Returns the qualified contract of a ticker.
        
        :param ticker: str. Instrument ticker.
        :pararm market: str. Market of the instrument. 'stock'/'futures'/'forex'
        
        :return: ib_insync.Contract
        """
        contract = self._contract_types[market](ticker)
        self.ib.qualifyContracts(contract)
        
        return contract
        
        
    def _get_order_id(self):
        """
        Gets an internal int to identify trades.
        
        :return: int
        """
        order_id = self._counter
        self._counter += 1
        
        return order_id
    
    
    def get_positions(self):
        """
        Gets a list of the positions of the account.
        
        :return: list. List of ib_insync.Position instances.
        """
        
        self.ib.sleep()
        return self._positions
    
    
    def get_instrument_position(self, instrument):
        """
        Gets the size of the position for an instrument. If there's no 
        position for that instrument returns 0.
        
        :param instrument: str. Instrument ticker.
        :return: float. Position size or 0.
        """
        for p in self._positions:
            symbol = "".join(p.contract.localSymbol.split('.'))
            if symbol == instrument:
                return p.position
        
        return 0
        
        
    def place_limit_order(self, contract, type_, price, quantity, sleep=True):
        """
        Places a limit order.
        
        :param contract: ib_insync.Contract instance.
        :param type_: str. 'BUY'/'Sell'
        :param price: float. Price at which the order will be triggered.
        :param quantity: int. Size of the position in dollars.
        
        :return: int. The order id used by the Trader class to indentify 
                      trades. See _get_order_id()
        """
        # Generating order.
        order = ib.LimitOrder(type_, int(quantity), price, account=self.account)
        
        # Placing order.
        order_trade_id = self._place_order(contract=contract, order=order, 
                                           sleep=sleep)
        
        return order_trade_id

    
    def place_market_order(self, contract, type_, quantity):
        """
        Places a market order.
        
        :param contract: ib_insync.Contract instance.
        :param type_: str. 'BUY'/'Sell'
        :param quantity: int. Size of the position in dollars.
        
        :return: int. The order id used by the Trader class to indentify 
                      trades. See _get_order_id()
        """
        print("\nPlacing {} order of quantity {} for contract:".format(type_,
                                                                       quantity))
        print(contract)
        
        # Generating order.
        order = ib.MarketOrder(type_, int(quantity), account=self.account)
        
        # Placing order.
        order_trade_id = self._place_order(contract=contract, order=order)
        
        return order_trade_id
        
    
    def _place_order(self, contract, order, sleep=True):
        """
        Places an order and updates self.trades in the process.
        
        :param contract: ib_insync.Contract instance.
        :param order: ib_insync.order.Order. Could be a market order or
                                             a limit order.
        
        :return: int. The order id used by the Trader class to indentify 
                      trades. See _get_order_id()
        """
        trade = self.ib.placeOrder(contract, order)
        
        # Storing order and trade.
        order_trade_id = self._get_order_id()
        order_trade_dict = {'order': order, 'trade': trade}
        self.trades[order_trade_id] = order_trade_dict
        
        # Waiting for execution.
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ib.IB.run(asyncio.sleep(0.2, loop=loop))
#        future = asyncio.ensure_future(self.ib.sleep()) 
#        loop.run_until_complete(future)
            
        return order_trade_id
    
    
    async def _sleep(self, timer=0.2):
        self.ib.sleep(timer)
        
    
    def update(self, message):
        """
        Subscriber pattern main method. Will be called each time a registered
        event occurs.
        
        :param message: dict. message will at least contain the keys 'ticker'
                              and 'forecast'.
        """
        # Extracting data from message.
        instrument = message['ticker']
        forecast = float(message['forecast'])
        
        # Position calculations.
        current_position = self.get_instrument_position(instrument)
        position_diff = forecast - current_position
        contract = self.contracts[instrument]
        buffer = current_position * self._buffer
        
        # Placing a new position.
        if abs(position_diff) > buffer:
            if position_diff > 0:
                self.place_market_order(contract, 'BUY', position_diff)
            elif position_diff < 0:
                self.place_market_order(contract, 'SELL', -position_diff)
        
            
    
if __name__ == "__main__":
    # Configuration.
    instruments_dict = config.instruments
    account = config.ACCOUNT
    buffer = config.BUFFER

    # Initiallization.
    trader = IBTrader(instruments_dict=instruments_dict, account=account)
    
    
    
    
    