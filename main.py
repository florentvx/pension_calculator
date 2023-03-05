from pathlib import Path
import yaml
from src import *

my_data_path = Path(r"C:\Users\flore\OneDrive\Documents\Diverse\pension\my_data.yaml")
my_data = yaml.safe_load(open(my_data_path, 'r'))

statics = model_statics(**my_data["model_statics"])
pension_data : dict = my_data['pension_data']

res = get_pension_historical_summary(statics, pension_data)
last_date = list(res.keys())[-1]
same_inf = [
    convert_price_with_inflation(my_data['historical_inflation'], res[date_k].pension_real, date_k, last_date)
    for date_k in res
]

print("END")