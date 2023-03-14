from pathlib import Path
import yaml
import matplotlib.pyplot as plt
import numpy as np

from src import *

my_data_path = Path(r"C:\Users\flore\OneDrive\Documents\Diverse\pension\my_data.yaml")
my_data = yaml.safe_load(open(my_data_path, 'r'))

statics = model_statics(**my_data["model_statics"])
pension_data : dict = my_data['pension_data']

res = get_pension_historical_summary(statics, pension_data)
last_date = list(res.keys())[-1]

pension_evolution = [
    convert_price_with_inflation(my_data['historical_inflation'], res[date_k].pension_real * 12.0, date_k, last_date)
    for date_k in res
]

pension_real_net_evolution = [
    convert_price_with_inflation(my_data['historical_inflation'], res[date_k].pension_real_net, date_k, last_date)
    for date_k in res
]

first_date = list(res.keys())[0]
date_list = list(res[first_date].historical_real_amounts.keys())
date_list.sort()
closest_date = max([d for d in date_list if d < last_date])
pension_total_evolution = [
    convert_price_with_inflation(my_data['historical_inflation'], res[date_k].historical_real_amounts[closest_date], date_k, last_date)
    for date_k in res
]


#plot

from matplotlib.dates import DateFormatter, YearLocator

#yearsFmt = 
#yearLoc = YearLocator()

figure, axis = plt.subplots(2, 2)
axis[0,0].xaxis.set_major_locator(YearLocator())
axis[0,0].xaxis.set_major_formatter(DateFormatter('%Y'))
axis[0,0].plot(res.keys(), pension_evolution, label="pension real yearly")
axis[0,0].set_title('pension yrly')
axis[0,0].grid()
axis[0,1].xaxis.set_major_locator(YearLocator())
axis[0,1].xaxis.set_major_formatter(DateFormatter('%Y'))
axis[0,1].plot(res.keys(), pension_real_net_evolution, label="pension net")
axis[0,1].set_title('pension net mthly')
axis[0,1].grid()
axis[1,0].xaxis.set_major_locator(YearLocator())
axis[1,0].xaxis.set_major_formatter(DateFormatter('%Y'))
axis[1,0].plot(res.keys(), pension_total_evolution, label="pension total")
axis[1,0].set_title(f'pension total {last_date.year}')
axis[1,0].grid()
bx1 = np.arange(len(list(my_data['historical_inflation'].values())))
bx2 = [bx1_k + 0.25 for bx1_k in bx1]
axis[1,1].bar(bx1, my_data['historical_inflation'].values(), label="inflation", color='r', width=0.25)
axis[1,1].bar(bx2, my_data['historical_performance'].values(), label="performance", color='b', width=0.25)
plt.xticks(
    [r + 0.25 for r in range(len(list(my_data['historical_inflation'].values())))],
    my_data['historical_inflation'].keys()
)
axis[1,1].set_title('inflation/performance')
axis[1,1].grid()
axis[1,1].legend()





# axis[1,0].xaxis.set_major_locator(yearLoc)
# axis[1,0].xaxis.set_major_formatter(yearsFmt)
# axis[0,1].xaxis.set_major_locator(yearLoc)
# axis[0,1].xaxis.set_major_formatter(yearsFmt)
# axis[1,1].xaxis.set_major_locator(yearLoc)
# axis[1,1].xaxis.set_major_formatter(yearsFmt)
# axis[0,0].autoscale_view()

#figure.update_xaxis(dtick="Y1", tickformat="%Y")

plt.show()


print("END")