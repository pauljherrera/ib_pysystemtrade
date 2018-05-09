from pysystemtrade.sysdata.data import Data


class instrumentsData(Data):
    """Get specific asset data.
        Extends the Data class to add additional features for asset specific.
        Will normally be overriden by a method for a specific data source.
        See legacy.py
    """

    def __init__(self, dataframe=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check the instrument we are passing.
        setattr(self, "Instruments", dataframe)


    # This override the get_raw_price of data class
    def get_raw_price(self, instrument_code, data=None):
        """Get the close price of the stock.

        :param data: raw DataObject with stocks indicators.
        :type data: None or Pd.Series.
        """
        
        #this conditional fix the problem of the forecasting class to work with dicts.
        if data is not None:                                    
           df = data[instrument_code2]          
           priceValue = df['close']
        else:
            #Extract the Dict from init.
            df = self.Instruments[instrument_code]
            #Set the datetime as index.
            priceValue =  df['close']
            
        return priceValue



