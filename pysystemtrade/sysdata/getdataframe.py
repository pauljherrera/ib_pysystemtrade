"""
Get data from an existing dataframe

Avanti pysystemtrade project
"""

import os
import pandas as pd


from sysdata.data import Data
#Data es el objeto base con el que trabaja pysystemtrade

class getDataFrame(Data):
    

    def __init__(self, dataframe=None):
        

        super().__init__()
        """
        Hereda atributos del objeto Data
        """
        if dataframe is not None:
            pass
        else:
            print("Introduzca un Data Frame de pandas")

        setattr(self,"activo",dataframe) # para probar que se está leyendo el df

    def get_close_price(Self,dataframe):
        """
        Obtener el precio close del dataframe

        Retorna un objeto series de pandas.
        """
        dataframe.columns = ['Close']
        price = dataframe['Close']
        return price

