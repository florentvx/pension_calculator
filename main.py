
from src import *

# tax
d = {
    am: calculate_net_income(am * 10000) / 12.0
    for am in range(25)
}

# pension
res = simulate_pension_fund(
    dt.date(2017, 8, 1), 
    month_id = 40, 
    current_amount=39680.05, 
    current_contribution=968.75,
)

print("END")