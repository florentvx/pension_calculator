def calculate_income_tax(gross_annual_amount: float):
    personal_allowance = 12570.0
    basic_rate = 0.2
    basic_rate_threshold_spread = 50270 - personal_allowance
    higher_rate = 0.4
    higher_rate_threshold = 150000
    additional_rate = 0.45
    less_allowance = 100000

    allowance = personal_allowance
    allowance -= min(personal_allowance, 0.5 * max(gross_annual_amount - less_allowance, 0))

    basic_rate_threshold = allowance + basic_rate_threshold_spread
    higher_rate_threshold = allowance + higher_rate_threshold

    basic_tax = min(basic_rate_threshold - allowance, max(0, (gross_annual_amount - allowance))) * basic_rate
    higher_tax = min(higher_rate_threshold - basic_rate_threshold, max(0, (gross_annual_amount - basic_rate_threshold))) * higher_rate
    additional_tax = max(0, (gross_annual_amount - higher_rate_threshold) * additional_rate)
    return basic_tax + higher_tax + additional_tax

def calculate_national_insurance_tax(annual_gross_amount: float):
    start_threshold = 242
    higher_rate = 0.12
    lower_rate_threshold = 967
    lower_rate = 0.02

    weekly_revenue = annual_gross_amount / 52.
    higher_tax = min(lower_rate_threshold - start_threshold, max(0, weekly_revenue - start_threshold)) * higher_rate
    lower_tax = max(0, weekly_revenue - lower_rate_threshold) * lower_rate
    return (higher_tax + lower_tax) * 52.

def calculate_net_income(annual_gross_amount: float):
    return annual_gross_amount - calculate_income_tax(annual_gross_amount) - calculate_national_insurance_tax(annual_gross_amount)

if __name__ == '__main__':
    d = {
        am*10: calculate_net_income(am * 10000) / 1000.0
        for am in range(1, 25)
    }
    for (k,v) in d.items():
        print(f"gross £ {k} K: year net: £ {round(v, 2)} K (monthly £ {round(v/12.0 * 1000)}) - tax rate: {round(100 * (1-v/k), 2)} %")