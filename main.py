from pathlib import Path
import yaml


from src import *

my_data_path = Path(r"C:\Users\flore\OneDrive\Documents\Diverse\pension\my_data.yaml")
my_data = yaml.safe_load(open(my_data_path, 'r'))

statics = model_statics(**my_data["model_statics"])
pension_data : dict = my_data['pension_data']

res = get_pension_historical_summary(statics, pension_data)

historical_dates = [
    date_string_to_date(k) 
    for k in pension_data.keys() 
    if pension_data[k]['amount'] > 0
]
historical_dates.sort()
first_date = historical_dates[0]
last_date = historical_dates[-1]

simulated_date_list = list(res[first_date].historical_real_amounts.keys())
simulated_date_list.sort()
closest_date = max([d for d in simulated_date_list if d < last_date])

pension_evolution = [
    convert_price_with_inflation(
        my_data['historical_inflation'], 
        res[date_k].pension_real * 12.0, 
        date_k, 
        last_date
    )
    for date_k in res
]

pension_real_net_evolution = [
    convert_price_with_inflation(
        my_data['historical_inflation'], 
        res[date_k].pension_real_net, 
        date_k, 
        last_date
    )
    for date_k in res
]

pension_total_evolution = [
    convert_price_with_inflation(
        my_data['historical_inflation'], 
        res[date_k].historical_real_amounts[closest_date], 
        date_k, 
        last_date
    )
    for date_k in res
]

plot_all(
    historical_dates, 
    pension_evolution, 
    pension_real_net_evolution, 
    pension_total_evolution, 
    historical_inflation=my_data['historical_inflation'],
    historical_performance=my_data['historical_performance']
)



print("END")