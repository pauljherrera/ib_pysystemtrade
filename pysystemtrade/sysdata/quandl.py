"""Implementation of quandl module

Avanti                  
"""
import pandas as pd
import os
from pandas import read_csv
import quandl #quandl should be in the requirements.txt file.
# Specific Data Object to read OHLC format data
from sysdata.instrumentsData import instrumentsData


class getInstrument(instrumentsData):
    """Get instrument specific data from quandl files

        Extends the instrumentsData class for a specific data source

     """

    def __init__(self):
        """Create a instrumentsData object for reading  files from quandl.
        
        inherits from instrumentsData

        :returns: new object
        """
        super().__init__()

    def get_Close(self, instrument):
        """Get the close price of the asset.

        :param instrument: raw DataObject with stocks indicators.
        :type instrument: None or DataFrame.
        """
        instrument_df = quandl.get(instrument)
        OpenValue = self._get_Close(instrument_df)
        return OpenValue

    def get_Open(self, instrument):
        pass

if __name__ == '__main__':
    pass
