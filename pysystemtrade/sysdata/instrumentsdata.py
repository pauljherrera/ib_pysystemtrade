import os

import pandas as pd

from sysdata.data import Data


class instrumentsData(Data):
    """Get specific asset data.

        Extends the Data class to add additional features for asset specific.

        Will normally be overriden by a method for a specific data source.
        See legacy.py
    """ 
    def __init__(self, dataframe = None):
       
       
        super().__init__()
        data = dataframe
        setattr(self,"Instrument",dataframe) #Check the instrument we are passing.
    
    def _get_Close(self,data):
        """Get the close price of the stock.

        :param data: raw DataObject with stocks indicators.
        :type data: None or DataFrame.
        """
        try:
            priceValue = data["Close"]
        except KeyError as identifier:
            priceValue = data["Value"]
        
        return priceValue
        