from pathlib import Path
import yaml
from src import *

my_data_path = Path(r"C:\Users\flore\OneDrive\Documents\Diverse\pension\my_data.yaml")
my_data = yaml.safe_load(open(my_data_path, 'r'))

statics = model_statics(**my_data["model_statics"])
pension_data : dict = my_data['pension_data']

res = get_pension_historical_summary(statics, pension_data)

print("END")