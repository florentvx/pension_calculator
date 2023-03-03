from __future__ import annotations
import datetime as dt

class model_statics:
    def __init__(
        self,
        forward_inflation_rate: float,
        forward_market_rate: float,
        working_number_years: int,
        retirement_number_years: int,
        contribution_increase_month: int,
        annual_contribution_increase_rate: float,
        ):
        self.forward_inflation_rate = forward_inflation_rate
        self.forward_market_rate = forward_market_rate
        self.working_number_years = working_number_years
        self.retirement_number_years = retirement_number_years
        self.contribution_increase_month = contribution_increase_month
        self.annual_contribution_increase_rate = annual_contribution_increase_rate

def add_month(date: dt.date, nb_month: int = 1, set_day_to_one: bool = True):
    new_month = date.month + nb_month
    x_year = int((new_month - 1) / 12)
    x_month = new_month - x_year * 12
    return dt.date(date.year + x_year, max(1, x_month), 1 if set_day_to_one else date.day )

class _simulate_pension_struct:
    def __init__(self, month_id: int, date: dt.date, cpi: float, contribution:float, amount: float):
        self.month_id = month_id
        self.date = date
        self.cpi = cpi
        self.contribution = contribution
        self.amount = amount
    
    @property
    def real_amount(self):
        return self.amount / self.cpi

    def get_next(
        self, 
        cpi_rate: float, 
        contribution: float, 
        forward_market_growth: float
        ) -> _simulate_pension_struct:
        return _simulate_pension_struct(
            self.month_id + 1,
            add_month(self.date),
            self.cpi * (1 + cpi_rate / 12.0),
            contribution,
            amount=self.amount * (1 + forward_market_growth / 12.0) + contribution
        )


def simulate_pension_fund(
    start_date:                     dt.date,
    month_id:                       int,
    current_amount:                 float,
    current_contribution:           float,
    statics:                        model_statics,
    ) -> list[_simulate_pension_struct]:

    res = [_simulate_pension_struct(month_id, add_month(start_date, month_id) , 1.0, 0, current_amount)]
    while res[-1].month_id < statics.working_number_years * 12:
        new_contrib = res[-1].contribution if res[-1].contribution != 0 else current_contribution
        new_contrib *= 1 + (statics.annual_contribution_increase_rate \
            if add_month(res[-1].date).month == statics.contribution_increase_month else 0)
        res += [res[-1].get_next(statics.forward_inflation_rate, new_contrib, statics.forward_market_rate)]
    return res

def calculate_fix_pension_from_fund(
    final_amount: float,
    nb_retirement_years: int,
    forward_market_growth: float,
    ):
    fwd_mkt_mthly = forward_market_growth / 12.0
    return final_amount * fwd_mkt_mthly/(1 - (1 + fwd_mkt_mthly)**(-nb_retirement_years * 12))
