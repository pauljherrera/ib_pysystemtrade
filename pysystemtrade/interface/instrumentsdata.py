from sysdata.data import Data


class instrumentsData(Data):
    """Get specific asset data.
        Extends the Data class to add additional features for asset specific.
        Will normally be overriden by a method for a specific data source.
        See legacy.py
    """

    def __init__(self, dataframe=None):
        super().__init__()
        # Check the instrument we are passing.
        setattr(self, "Instrument", dataframe)


    # This override the get_raw_price of data class
    def get_raw_price(self, instrument_code, data=None):
        """Get the close price of the stock.

        :param data: raw DataObject with stocks indicators.
        :type data: None or Pd.Series.
        """
        #this conditional fix the problem of the forecasting class to work with dicts.
        if data is not None:                                    
           df = data[instrument_code]          
           priceValue = df['close']
        else:
            completeInstruments = self.Instrument
            #Extract the Dict from init.
            dfInstruments = completeInstruments[instrument_code]
            df = dfInstruments
            #Set the datetime as index.
            priceValue =  df['close']
            
        return priceValue


    # This override the daily_prices of data class
    def daily_prices(self, instrument_code):
        """
        Gets daily prices
        :param instrument_code: Instrument to get prices for
        :type trading_rules: str
        :returns: Tx1 pd.Series
        """
        instrprice = self.get_raw_price(instrument_code)

        return instrprice
