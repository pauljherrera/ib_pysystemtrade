import sys
from sysdata.csvdata import csvFuturesData

stdout_ = sys.stdout
sys.stdout = open('output.txt', 'w')

data = csvFuturesData("sysdata.tests")

space = '\n'+'---'*20+'\n'

print("Data object.")
print("Data = csvFuturesData() \nData: {}".format(data), end=space)

cost_data = data._get_all_cost_data()
message = "\ndata._get_all_cost_data()"\
          "returns Data frame of all cost data:"\
          "\n{},\ntype:{}"

print(message.format(cost_data, type(cost_data)), end=space)

cost_data = data.get_raw_cost_data("EDOLLAR")

message = "\ndata.get_raw_cost_data(instrument_code='EDOLLAR')"\
            "\nreturns Dict of float for a"\
            " given instrument. Example:\n{}\n"

items = cost_data.items()
print(message.format(items), end=space)

price = data.get_raw_price("EDOLLAR").tail(5)
message = "\ndata.get_raw_price(instrument_code='EDOLLAR')"\
            "\nreturns a Pandas Series of prices and timestamps for a"\
            " given instrument. Example:\n{}\n"

print(message.format(price), end=space)

df = data.get_instrument_raw_carry_data("EDOLLAR").tail(4)

message = "\ndata.get_instrument_raw_carry_data(instrument_code='EDOLLAR') for futures trading"\
            "\nreturns a Pandas DataFrame\n"\
            "PRICE CARRY CARRY_CONTRACT PRICE_CONTRACT for a"\
            " given instrument. Example:\n{}\n"

print(message.format(df), end=space)

df = data._get_instrument_data()
message = "\ndata._get_instrument_data()"\
            "\nreturns a Pandas DataFrame\n"\
            "with information about instruments. Example:"\
            ":\n{}\n"

print(message.format(df), end=space)

instruments = data.get_instrument_list()
message = "\ndata.get_instrument_list()"\
            "\nreturns a list of strings\n"\
            "with the instruments. Example:"\
            ":\n{}\n"

print(message.format(instruments), end=space)

df = data._get_fx_data("EUR", "USD").tail(4)

message = "\ndata._get_fx_data('EUR', 'USD')"\
            "\nreturns a Pandas DataFrame or none if not available\n"\
            "currency 1: numerator.\ncurrency2: denominator. Example:"\
            "\n{}\n"

print(message.format(df), end=space)
print("\nSystem forecasting.\n", end=space)

from systems.provided.example.rules import ewmac_forecast_with_defaults as ewmac
from systems.forecasting import Rules
from systems.provided.futures_chapter15.basesystem import futures_system
"""
to make our rule work it needs to have:
"""

my_rules = Rules(ewmac)
print("\n",my_rules.trading_rules(), end=space)

my_rules = Rules(dict(ewmac=ewmac))
print("\n",my_rules.trading_rules(), end=space)

from systems.basesystem import System
my_system = System([my_rules], data)
print("\n",my_system, end=space)

df = my_system.rules.get_raw_forecast("EDOLLAR", "ewmac").tail(5)

message = "\nmy_system.rules.get_raw_forecast('EDOLLAR', 'ewmac')"\
            "\nreturns a Pandas DataFrame with the forecast of each day\n"\
            "Example:"\
            "\n{}\n"

print(message.format(df), end=space)

"""
Define a TradingRule
"""

from systems.forecasting import TradingRule
from systems.positionsizing import PositionSizing

ewmac_rule = TradingRule(ewmac)
my_rules = Rules(dict(ewmac=ewmac_rule))
print(ewmac_rule, end=space)

possizer = PositionSizing()
my_system = System([my_rules, possizer], data)
my_system.rules.get_raw_forecast("EDOLLAR", "ewmac").tail(5)

print("System position features.", end=space)

df = my_system.positionSize.get_price_volatility("EDOLLAR").tail(5)

message = "\nmy_system.positionSize.get_price_volatility('EDOLLAR')"\
            "\nreturns a Pandas DataFrame with the price volatility of each day\n"\
            "Example:"\
            "\n{}\n"

print(message.format(df), end=space)
print("Daily cash volume target:")
print(my_system.positionSize.get_daily_cash_vol_target(), end=space)


sys.stdout = stdout_
