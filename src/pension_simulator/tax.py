import pandas as pd

TAX_HISTORICAL_PARAMETERS = {
    "2020-2021":{
        "personal_allowance":12500,
        "higher_rate_threshold":150000,
        "higher_rate":12.0,
    },
    "2021-2022":{
        "personal_allowance":12570,
        "higher_rate_threshold":150000,
        "higher_rate":12.0,
    },
    "2022-2023":{
        "personal_allowance":12570,
        "higher_rate_threshold":150000,
        "higher_rate":12.0,
    },
    "2023-2024":{
        "personal_allowance":12570,
        "higher_rate_threshold":125140,
        "higher_rate":12.0,
    },
    "2024-2025":{
        "personal_allowance":12570,
        "higher_rate_threshold":125140,
        "higher_rate":8.0,
    },
    "2025-2026":{
        "personal_allowance":12570,
        "higher_rate_threshold":125140,
        "higher_rate":8.0,
    },
}

def get_available_tax_years():
    return list(TAX_HISTORICAL_PARAMETERS.keys())

def get_max_tax_year():
    tax_years = get_available_tax_years()
    max_key = max([int(k[:4]) for k in tax_years])
    return f"{str(max_key)}-{str(max_key+1)}"

def get_tax_param(tax_year, key):
    x = TAX_HISTORICAL_PARAMETERS[tax_year].get(key, None)
    if x is None:
        raise ValueError(f"key {key} not found in tax year {tax_year}")
    return x

def calculate_income_tax(gross_annual_amount: float, tax_year: str = None) -> pd.DataFrame:
    if tax_year is None:
        tax_year = get_max_tax_year()
    elif tax_year not in TAX_HISTORICAL_PARAMETERS:
        raise ValueError(f"tax year does not exist in analytics [{tax_year}]")
    allowance_rate = 0.0
    personal_allowance = get_tax_param(tax_year, "personal_allowance") # 12570.0
    less_allowance_threshold = 100000
    basic_rate = 20.0
    basic_rate_threshold_spread = 50270 - personal_allowance
    higher_rate = 40.0
    higher_rate_threshold = get_tax_param(tax_year, "higher_rate_threshold") # 150000
    additional_rate = 45.0
    
    res = []
    # allowance calculations
    allowance = personal_allowance
    allowance -= min(personal_allowance, 0.5 * max(gross_annual_amount - less_allowance_threshold, 0))
    res += [["Allowance", allowance, allowance_rate]]

    # basic calculations
    basic_rate_threshold = allowance + basic_rate_threshold_spread
    basic_gross_amount = min(basic_rate_threshold - allowance, max(0, (gross_annual_amount - allowance)))
    res += [["Basic", basic_gross_amount, basic_rate]]    

    # higher calculations
    higher_rate_threshold = allowance + higher_rate_threshold
    higher_gross_amount = min(higher_rate_threshold - basic_rate_threshold, max(0, (gross_annual_amount - basic_rate_threshold)))
    res += [["Higher", higher_gross_amount, higher_rate]]
    
    # Additional calculations
    additional_gross_amount = max(0, (gross_annual_amount - higher_rate_threshold))
    res += [["Additional", additional_gross_amount, additional_rate]]
    my_df = pd.DataFrame(res, columns=["Name", "Gross Amount", "Tax Rate (%)"])
    my_df = my_df.set_index("Name")
    my_df["Tax Amount"] = my_df["Gross Amount"] * my_df["Tax Rate (%)"] / 100.0
    totals = my_df.sum()
    totals["Tax Rate (%)"] = round(totals["Tax Amount"] / totals["Gross Amount"] * 100, 2)
    my_df.loc["Total Income Tax"] = totals
    return my_df

def calculate_national_insurance_tax(annual_gross_amount: float, tax_year: str = None) -> pd.DataFrame:
    if tax_year is None:
        tax_year = get_max_tax_year()
    elif tax_year not in TAX_HISTORICAL_PARAMETERS:
        raise ValueError(f"tax year does not exist in analytics [{tax_year}]")
    start_threshold = 242
    higher_rate = get_tax_param(tax_year, "higher_rate") # 12.0
    lower_rate_threshold = 967
    lower_rate = 2.0

    weekly_revenue = annual_gross_amount / 52.
    higher_amount = min(lower_rate_threshold - start_threshold, max(0, weekly_revenue - start_threshold))
    lower_amount = max(0, weekly_revenue - lower_rate_threshold)

    res = [
        ["No Tax", min(start_threshold, weekly_revenue) * 52.0, 0.0],
        ["Higher Tax", higher_amount * 52.0, higher_rate],
        ["Lower Tax", lower_amount * 52.0, lower_rate]
    ]
    my_df = pd.DataFrame(res, columns=["Name", "Gross Amount", "Tax Rate (%)"])
    my_df = my_df.set_index("Name")
    my_df["Tax Amount"] = my_df["Gross Amount"] * my_df["Tax Rate (%)"] / 100.0
    totals = my_df.sum()
    totals["Tax Rate (%)"] = round(totals["Tax Amount"] / totals["Gross Amount"] * 100, 2)
    my_df.loc["Total NI Tax"] = totals
    return my_df

def calculate_all_taxes(annual_gross_amount: float, tax_year: str = None) -> pd.DataFrame:
    income_tax = calculate_income_tax(annual_gross_amount, tax_year=tax_year).loc["Total Income Tax"]
    ni_tax = calculate_national_insurance_tax(annual_gross_amount, tax_year=tax_year).loc["Total NI Tax"]
    my_df = pd.DataFrame(income_tax).T
    my_df.loc["Total NI Tax"] = ni_tax
    my_df = my_df.drop("Gross Amount", axis = 1)
    my_df.loc["Total"] = my_df.sum()
    return my_df

def calculate_net_income(annual_gross_amount: float, tax_year: str = None):
    income_tax = calculate_income_tax(annual_gross_amount, tax_year = tax_year).loc["Total Income Tax"]["Tax Amount"]
    ni_tax = calculate_national_insurance_tax(annual_gross_amount, tax_year = tax_year).loc["Total NI Tax"]["Tax Amount"]
    return annual_gross_amount - income_tax - ni_tax

if __name__ == '__main__':
    d = {
        am*10: calculate_net_income(am * 10000) / 1000.0
        for am in range(1, 25)
    }
    for (k,v) in d.items():
        print(f"gross £ {k} K: year net: £ {round(v, 2)} K (monthly £ {round(v/12.0 * 1000)}) - tax rate: {round(100 * (1-v/k), 2)} %")