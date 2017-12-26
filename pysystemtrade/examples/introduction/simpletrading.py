"""
Ejemplo simple de pysystemtrade con pequeña modificacion al momento de obtener los datos.

"""

import os 
import pandas as pd 
import numpy as np

from sysdata.getdataframe import getDataFrame
"""
No necesariamente se tiene que crear una clase ya que se puede usar un DF y pasarlo a la funcion calc_ewmac_forecast
pero creo que puede ser util luego que esta clase herede los atributos de sysdata.data . 
"""
from sysdata.reader import Reader
from syscore.algos import robust_vol_calc

def main():
    lector = Reader()
    activo = "FRED/AAA10Y"
#    df = lector.read_quandl_option(activo)
    
    df = lector.read_csv_option('BTCdata')
    
    df = pd.read_csv('BTCdata.csv', parse_dates={'Date':["date","time"]})
    df = df.set_index('Date')[['close']]

    #Se descarga un DF desde quandl, esto con el fin de cambiar la forma en que se cargan los datos

    data = getDataFrame(df)

    def calc_ewmac_forecast(price, Lfast, Lslow=None):
        """
        Calculate the ewmac trading fule forecast, given a price and EWMA speeds
        Lfast, Lslow and vol_lookback

        """
        # price: This is the stitched price series
        # We can't use the price of the contract we're trading, or the volatility
        # will be jumpy
        # And we'll miss out on the rolldown. See
        # http://qoppac.blogspot.co.uk/2015/05/systems-building-futures-rolling.html

        if Lslow is None:
            Lslow = 4 * Lfast

        # We don't need to calculate the decay parameter, just use the span
        # directly
        fast_ewma = price.ewm(span=Lfast).mean()
        slow_ewma = price.ewm(span=Lslow).mean()
        raw_ewmac = fast_ewma - slow_ewma

        vol = robust_vol_calc(price.diff())
        return raw_ewmac / vol

    price = data.get_close_price(df)
    #Obtengo los precios de cierre.

    print(price.tail(5))
    ewmac = calc_ewmac_forecast(price,32,128)
    ewmac.columns = ['forecast']

    print(ewmac.tail(5))
    from matplotlib.pyplot import show
    ewmac.plot()
    show()

    from syscore.accounting import accountCurve
    account = accountCurve(price, forecast=ewmac)
    account.curve()

    account.curve().plot()
    show()

    print(account.percent().stats())

    return data, price, ewmac

    
    

if __name__ == '__main__':
    d, p, ewmac= main()