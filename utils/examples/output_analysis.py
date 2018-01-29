pysystemtrade outputs anaysis. (Pseudocode)

Account


Portfolio

	get_notional_position():
		# diversification multiplier
		if config.use_instrument_div_mult_estimates == True:
			config.instrument_div_mult_estimate (func and complex)
			config.instrument_correlation_estimate(func and complex)
			superstage.account.pandl_across_subsystems()
		else:
			config.instrument_div_multiplier
			# also used in instrument weights.
			if config.use_instrument_weight_estimates == True:
				config.instrument_weight_estimate (func, complex)
				superstage.account.pandl_across_subsystems()
			else:
				try:
					config.instrument_weights (complex) # One for each instrument
				except:
					weight = 1.0 / len(instruments) # Sends a warning.

		substage.position_sizing.get_subsystem_position()

		return subsystem_position * weights * instrument_diversification_multiplier


Position Sizing

	get_subsystem_position():
		defaults.average_absolute_forecast

		# volatility_scalar = cash_vol_target / instr_value_vol
		# instr_value_vol
		if stage.rawdata:
			substage.rawdata.daily_denominator_price()
		else:
			substage.data.daily_prices()
			robust_vol_calc()

		substage.data.get_value_of_block_price_move()  # 1.0 by default
		if stage.rawdata:
			substage.rawdata.get_daily_percentage_volatility()
		else:
			substage.data.daily_prices()

		# cash_vol_target
		config.percentage_vol_target
		config.notional_trading_capital
		config.base_currency

		# forecast
		substage.forecast_combine.get_combined_forecast()

		return volatility_scalar * forecast / average_absolute_forecast














