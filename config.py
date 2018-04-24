# Interactive Brokers configuration.
IB_API_HOST = '127.0.0.1'
IB_API_PORT = 4002
ACCOUNT='DU912679'

# Trading variable.
TIMEFRAME = 1		# In minutes. A timeframe of 60 would be an hour, a timeframe of 1440 would be a day.
HIST_DATA_DURATION = '1 D'   # '1 W' for one week, '2 M' for two months, '3 Y' for three years and so on.
BUFFER = 0.2 	    # Percentage

# Instruments to trade with.
instruments = {
    'forex': ['EURUSD'],
    'futures': [],
    'stocks': []
}
