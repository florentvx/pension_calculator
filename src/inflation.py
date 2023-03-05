import datetime as dt
from math import log, exp

def get_inflation_conversion_rate(data: dict, input_date: dt.date, output_date: dt.date):
    """dates are considered set to 31st Dec.
        example: input: 2017, output: 2020 -> (1+inf(2018))*(1+inf(2019))*(1+inf(2020))
    """
    if (input_date.year == output_date.year):
        return 1.0
    if input_date.year > output_date.year:
        return 1 / get_inflation_conversion_rate(data, output_date, input_date)
    else:
        return exp(sum([log(1 + data[y]/100.0) for y in range(input_date.year+1, output_date.year+1)]))
            
def convert_price_with_inflation(data: dict, input_price: float, input_date: dt.date, output_date: dt.date):
    return input_price * get_inflation_conversion_rate(data, input_date, output_date)

if __name__ == '__main__':
    data = { 2017: 1.00, 2018: 2.00, 2019: 3.00, 2020: 4.00, 2021: 5.00 }
    fx1 = get_inflation_conversion_rate(data, dt.date(2017, 1, 1), dt.date(2020, 1, 1))
    print("END")