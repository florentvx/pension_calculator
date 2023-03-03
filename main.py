from pathlib import Path
import yaml
from src import *

# tax
d = {
    am: calculate_net_income(am * 10000) / 12.0
    for am in range(25)
}

# pension

my_data_path = Path(r"C:\Users\flore\OneDrive\Documents\Diverse\pension\my_data.yaml")
my_data = yaml.safe_load(open(my_data_path, 'r'))

statics = model_statics(**my_data["model_statics"])

pension_data : dict = my_data['pension_data']

def date_string_to_date(input: str) -> dt.date:
    return dt.datetime.strptime(input, "%Y/%m/%d").date()

def get_month_id(date: dt.date, date_ref: dt.date):
    return date_k.month - date_ref.month + (date_k.year - date_ref.year) * 12 + (1 if date.day >= 25 else 0)

all_fix = []

start_date = date_string_to_date(list(pension_data.keys())[0])
for k in list(pension_data.keys())[1:]:
    date_k = date_string_to_date(k)
    value_k = pension_data[k]
    res = simulate_pension_fund(
        start_date,
        month_id =              get_month_id(date_k, start_date), 
        current_amount=         value_k['amount'], 
        current_contribution=   value_k['contribution'],
        statics = statics,
    )

    final_amounts = res[-1]
    all_fix += [(
        calculate_fix_pension_from_fund(final_amounts.amount, statics.retirement_number_years, statics.forward_market_rate),
        calculate_fix_pension_from_fund(final_amounts.real_amount, statics.retirement_number_years, statics.forward_market_rate)
    )]

print("END")