from __future__ import annotations
import datetime as dt
from .dates import date_string_to_date, get_month_id
from .pension_simulator import model_statics, simulate_pension_fund, calculate_fix_pension_from_fund
from .tax import calculate_net_income

class summary_struct:
    def __init__(self, statics: model_statics, final_amount: float, cpi: float):
        self.pension_gross = calculate_fix_pension_from_fund(
            final_amount, 
            statics.retirement_number_years, statics.forward_market_rate
        )
        self.pension_real = self.pension_gross / cpi
        self.pension_real_net = calculate_net_income(12 * self.pension_real) / 12.0
        self.tax_rate = 1.0 - self.pension_real_net / self.pension_real
        self.pension_net = self.pension_gross * (1 - self.tax_rate)

def get_pension_historical_summary(statics: model_statics, pension_data: dict):
    res : dict[dt.date, summary_struct] = {}

    start_date = date_string_to_date(list(pension_data.keys())[0])
    for k in list(pension_data.keys())[1:]:
        simulation_k = simulate_pension_fund(
            start_date,
            month_id =              get_month_id(date_string_to_date(k), start_date), 
            current_amount=         pension_data[k]['amount'], 
            current_contribution=   pension_data[k]['contribution'],
            statics = statics,
        )
        res[date_string_to_date(k)] = summary_struct(
            statics, 
            simulation_k[-1].amount, 
            simulation_k[-1].cpi,
        )
    return res