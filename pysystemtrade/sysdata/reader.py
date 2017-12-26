import pandas as pd
import os
from pandas import read_csv
import quandl



class Reader:
    """Clase para leer de un archivo CSV"""

    def read_csv_option(self,dirname):
        try:
            path = os.getcwd() + "\\" + str(dirname) + ".csv"
            data=read_csv(path)

            return data
        except Exception as e:
            print("Nombre incorrecto, segurese de estar en la carpeta del proyecto")
            print(path)

    def read_quandl_option(self,activo):

        try:
            data= quandl.get(activo)
            print(activo)
            return data

        except Exception as e:
            print(e)
