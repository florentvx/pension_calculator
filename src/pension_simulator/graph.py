from __future__ import annotations
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, YearLocator

def plot_all(
    dates: list[dt.date], 
    pension_evolution, 
    pension_real_net_evolution, 
    pension_total_evolution,
    historical_inflation: dict,
    historical_performance: dict,
    ):
    figure, axis = plt.subplots(2, 2)

    axis[0,0].xaxis.set_major_locator(YearLocator())
    axis[0,0].xaxis.set_major_formatter(DateFormatter('%Y'))
    axis[0,0].plot(dates, pension_evolution, label="pension real yearly")
    axis[0,0].set_title('pension yrly')
    axis[0,0].grid()

    axis[0,1].xaxis.set_major_locator(YearLocator())
    axis[0,1].xaxis.set_major_formatter(DateFormatter('%Y'))
    axis[0,1].plot(dates, pension_real_net_evolution, label="pension net")
    axis[0,1].set_title('pension net mthly')
    axis[0,1].grid()

    axis[1,0].xaxis.set_major_locator(YearLocator())
    axis[1,0].xaxis.set_major_formatter(DateFormatter('%Y'))
    axis[1,0].plot(dates, pension_total_evolution, label="pension total")
    axis[1,0].set_title(f'pension total (last year)')
    axis[1,0].grid()
    
    hist_inf_val = list(historical_inflation.values())[:(-1)]
    historical_inf_rate = [100.0 * (hist_inf_val[i+1]/hist_inf_val[i] - 1) for i in range(len(hist_inf_val) - 1)]
    bx1 = list(np.arange(len(historical_inf_rate)))
    bx2 = [bx1_k + 0.25 for bx1_k in bx1][:len(historical_inf_rate)]
    
    axis[1,1].bar(bx1, historical_inf_rate, label="inflation", color='r', width=0.25)
    axis[1,1].bar(bx2, historical_performance.values(), label="performance", color='b', width=0.25)
    plt.xticks(
        [r + 0.25 for r in range(len(list(historical_inflation.values())))],
        historical_inflation.keys()
    )
    axis[1,1].set_title('inflation/performance')
    axis[1,1].grid()
    axis[1,1].legend()

    plt.show()