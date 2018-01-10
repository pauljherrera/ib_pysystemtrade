"""Class to parse the data from ibAPI to pysystemtrade.

Avanti.
"""

from interface.instrumentsdata import instrumentsData


class ib_Data(instrumentsData):
    """Get data from data_Feeder using pub_sub pattern

    Extends the isntrumentData class for a specific data source
    """
    def __init__(self,instrument, *args, **kwargs):
        """
        Deals with Interactive Brokers data. Inherits from instrumentsData.
        """
        super().__init__(*args, **kwargs)
        setattr(self,"Instrument", instrument)


    def get_portfolio(self,instruments):
        portfolio = instruments.keys()
        
        return portfolio
    
    
    def get_specific_instrument(self,instrument,name):
       ins = instrument[name]

       return ins
   
    
    def get_instrument_list(self,instrument):
        number = len(instrument.keys())
        
        return number           

    def daily_prices(self, instrument_code):     #This override the daily_prices of data class
        """
        Gets daily prices
        :param instrument_code: Instrument to get prices for
        :type trading_rules: str
        :returns: Tx1 pd.Series
        """
        instrprice = self.get_raw_price(instrument_code)

        return instrprice