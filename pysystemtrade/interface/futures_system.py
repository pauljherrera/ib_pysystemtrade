#!/usr/bin/python3

from pprint import pprint
from matplotlib import pyplot as plt

from systems.provided.futures_chapter15.estimatedsystem import futures_system
from sysdata.configdata import Config
from sysdata.csvdata import csvFuturesData


# Initializing system.
my_config = Config("systems.private.nocarryconfig2.yaml")
data = csvFuturesData("systems.private.data")
system = futures_system(log_level="on", config=my_config, data=data)

# Making the backtest for the complete portfolio.
portfolio = system.accounts.portfolio()

# Showing useful plots and stats.
print("\n\nProfits and loss curve for the complete portfolio:")
portfolio.curve().plot()
plt.show()

print("\n\nCompounded profits and loss curve for the complete portfolio:")
portfolio.cumulative().curve().plot()
plt.show()

print("\n\nProfits and loss curve for each one of the assets:")
portfolio.to_frame().cumsum().plot()
plt.show()

print("\n\nDrawdown chart:")
portfolio.drawdown().plot()
plt.show()

print("\n\nBacktest stats:")
print(system.accounts.portfolio().stats())
plt.show()

