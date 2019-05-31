use sys;
-- select * from dividend where date(dt_last_update) = date(now())
-- truncate table dividend

select * from dividend 
where 
	stock_available_amount > 400000000 AND
    avg_21_negociation >= 0 AND
    avg_payout_12_months <= 0.7 AND
    avg_payout_5_years <= 0.7 AND
    valuation > 500000000 AND
    roe > 0.1 AND
    roe_5_yrs > 0.1 AND
    gross_debt_over_ebtida < 0.5 AND
    has_dividend_grwth_5_yrs = 1 AND
    has_dividend_srd_5_yers = 1 AND
    has_net_profit_reg_5_yrs = 1 AND
    dividend_yield_5_yrs > 0.03 AND
    dividend_yeld > 0.03 
	-- AND avg_21_negociation >= (0.20 * stock_available_amount) 