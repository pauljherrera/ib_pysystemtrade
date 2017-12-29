import os
import pandas as pd
import numpy as np
import asyncio

from syscore.algos import robust_vol_calc
from interface.ib_data import ib_Data
from systems.provided.example.rules import ewmac_forecast_with_defaults as ewmac
from systems.forecasting import Rules
from systems.basesystem import System
from sysdata.configdata import Config
from ib.data_feeder import IBfeeder_pst_adapter

from syscore.pdutils import pd_readcsv  # Momentary, delete when complete.
from syscore.fileutils import get_pathname_for_package  # Delete when complete

from utils import pub_sub

DATA_PATH = "sysdata.avanti"
DATA_PATH1 = "sysdata.tests"


def main():

    filename = os.path.join(get_pathname_for_package(
        DATA_PATH), "EURUSD_price.csv")

    filename1 = os.path.join(
        get_pathname_for_package(DATA_PATH1), "BUND_price.csv")

    # This two DF are just for testing purpose, delete when complete integration.
    USD = instr_data = pd.read_csv(filename)
    BUND = instr_data1 = pd.read_csv(filename1)

    instrument = {"USD": USD, "BUND": BUND}
    #Here should be de dict from data_feeder

    conector = ib_Data(instrument)
    # Ib data Object. This is the Object that manage the data from ibAPI. 

    print(type(conector.get_raw_price("BUND", instrument)))
    print(type(conector.daily_prices("BUND")))
    # We need a series pandas object in order to the system work.

    # create a list with the instruments for the config object
    systemInstruments = list(conector.get_portfolio(instrument))
    print(type(systemInstruments))

    my_config = Config()  # create a config object.

    # Set the instrument of the system via the config.
    my_config.instruments = systemInstruments

    my_rules = Rules(dict(ewmac=ewmac))
    my_rules.trading_rules()

    my_system = System([my_rules], conector, my_config)

    print(my_system.rules.get_raw_forecast("BUND", "ewmac"))


if __name__ == '__main__':
    main()

    ('pysystemtrade_data', subscriber)
