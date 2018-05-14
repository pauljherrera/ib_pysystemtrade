from systems.provided.futures_chapter15.basesystem import futures_system
from systems.provided.example.rules import ewmac_forecast_with_defaults as ewmac
from systems.forecasting import TradingRule
from systems.forecasting import Rules
from sysdata.configdata import Config


my_config = Config("interface.futuresconfig.yaml")
# Config object

system = futures_system(log_level="on", config=my_config)
# We parse the config object acording the class, for basesystem, the keyword is config, this change 
# accordding to class, as you can see we don't need to parse the stages.It makes everything
#  futures_system does but with customs atributes.

portfolio = system.accounts.portfolio()
print(system.positionSize.get_subsystem_position("EDOLLAR").tail(2))
# The output is somenthing like below
# ss_position
# 2015-12-10     1.811465
# 2015-12-11     2.544598
