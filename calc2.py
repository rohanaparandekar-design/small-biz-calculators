# Will this promotion cover its cost?

import math

 # Inputs

# Calculates promotion expense
promo_expense = float(input("What is your total promotion expense? $"))

# Average sale amount ()
avg_sale = float(input("What is your average sale amount? Sales should be reported after any relevant discounts. $"))

variable_cost = float(input("What is your total variable cost per sale? Include relevant fulfillment or transaction costs. $"))

# Contribution per sale

contribution = avg_sale - variable_cost 

# Sales needed to cover the promotion

if contribution <=0:
    print("Your variable cost currently equals or exceeds your average sale. Additional sales do not cover the promotion under these assumptions.")
else: 
    sales_needed = (promo_expense / contribution)
    rounded_sales = math.ceil(sales_needed)
    print(f"Each additional sale contributes ${contribution:,.2f}.")
    print(f"Under your current assumptions, {rounded_sales} additional sales will cover your promotion.")
    print("This is a threshold. It does not predict demand or prove the promotion caused a sale.")