import math
from tabulate import tabulate 

# Prices 
current_price = float(input("What is your current sale price? $"))
proposed_price = float(input("What is your proposed sale price? $"))

# Costs
variable_cost = float(input("What is your variable cost per sale? $"))
# Monthly fixed costs
fixed_costs = float(input("What are your monthly fixed costs? $"))

# Monthly Sales Volume
sales_volume = float(input("What is your monthly sales volume? Enter number only. "))
proposed_sales_volume = float(input("What is your proposed monthly sales volume? Enter number only. "))

# Calculations Section

# Contributions per sale

current_contribution = current_price - variable_cost

proposed_contribution = proposed_price - variable_cost

# Monthly operating profit
current_profit = sales_volume * current_contribution - fixed_costs
proposed_profit = proposed_sales_volume * proposed_contribution - fixed_costs
change_profit = proposed_profit - current_profit

# Tell if proposed profit will increase or decrease operating profit
if proposed_profit > current_profit:
    print(f"Your proposed changes would increase operating profit by ${change_profit:,.2f}")

elif change_profit < 0:
    print(f"Your proposed changes would decrease operating profit by ${abs(change_profit):,.2f}")
    
else:
    print("Your proposed changes would not change operating profit")

# Break-even sales

# Current contribution breakeven scenario
if current_contribution > 0:
    current_breakeven = math.ceil(fixed_costs / current_contribution)
else: 
    current_breakeven = "Not reachable"
    print("In the current scenario, each sale loses money or breaks even. Review pricing and costs.")

# Proposed contribution breakeven scenario
if proposed_contribution > 0:
    proposed_breakeven = math.ceil(fixed_costs / proposed_contribution)

else:
    proposed_breakeven = "Not reachable"
    print("In the proposed scenario, each sale loses money or breaks even. Review pricing and costs.")

print("Note: This assumes an average sale. Price changes often affect sales volume, so try different volumes.")
# All the data printed together 

data_together = [
    ["Operating Profit", f"${current_profit:,.2f}", f"${proposed_profit:,.2f}"],
    ["Contributions Per Sale", f"${current_contribution:,.2f}", f"${proposed_contribution:,.2f}"],
    ["Break-Even Sales", current_breakeven, proposed_breakeven]
]

headers = ["Metric", "Current", "Proposed"]
print(tabulate(data_together, headers=headers, tablefmt="grid", colalign=("left", "right", "right")))