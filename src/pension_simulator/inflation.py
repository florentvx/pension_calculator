import datetime as dt
from math import log, exp

def _get_linest_inflation_index(data: dict, input_date: dt.date):
    dates_before = [k for k in data.keys() if k <= input_date]
    dates_after = [k for k in data.keys() if k >= input_date]
    if len(dates_before) == 0:
        raise ValueError(f"input date {input_date} before data start date {min(data.keys())}")
    date_before = max(dates_before)
    if len(dates_after) == 0:
        dates_after = [k for k in data.keys() if k >= input_date - dt.timedelta(days=100)]
        if len(date_after) == 0:
            raise ValueError(f"input date {input_date} after data end date (-100 days) {max(data.keys())}")
    date_after = min(dates_after)
    if date_before == date_after:
        return data[date_before]
    w = 1 - (input_date - date_before) / (date_after - date_before)
    return w * data[date_before] + (1 - w) * data[date_after]

def get_inflation_conversion_rate(data: dict, input_date: dt.date, output_date: dt.date):
    return _get_linest_inflation_index(data, output_date) / _get_linest_inflation_index(data, input_date)
            
def convert_price_with_inflation(data: dict, input_price: float, input_date: dt.date, output_date: dt.date):
    return input_price * get_inflation_conversion_rate(data, input_date, output_date)

if __name__ == '__main__':
    data = { 2017: 1.00, 2018: 2.00, 2019: 3.00, 2020: 4.00, 2021: 5.00 }
    fx1 = get_inflation_conversion_rate(data, dt.date(2017, 1, 1), dt.date(2020, 1, 1))
    print("END")