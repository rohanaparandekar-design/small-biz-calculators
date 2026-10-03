"""Pure calculator functions converted from calc.py, calc2.py and calc3.py.

No input() or print() here; app.py and test_calc.py import these.
"""

import math


# Calculator One (calc.py) - Are AI tools worth it
def ai_tool_value(monthly_tasks, minutes_without, ai_minutes, hourly_value,
                  monthly_cost, setup_hours, setup_cash):
    """Return (net_hours, time_value, monthly_net, payback).

    payback is setup payback in months, or None when monthly_net <= 0.
    """
    # Net hours saved
    net_hours = ((minutes_without - ai_minutes) * monthly_tasks) / 60

    # Estimated value of time before tool costs
    time_value = net_hours * hourly_value

    # Monthly net savings
    monthly_net = time_value - monthly_cost

    # Setup cost
    setup_cost = setup_cash + setup_hours * hourly_value

    if monthly_net > 0:
        payback = setup_cost / monthly_net
    else:
        payback = None

    return net_hours, time_value, monthly_net, payback


# Calculator Two (calc2.py) - Will this promotion cover its cost?
def promo_break_even(promo_expense, avg_sale, variable_cost):
    """Return (contribution, sales_needed).

    sales_needed is rounded up to a whole sale, or None when contribution <= 0.
    """
    # Contribution per sale
    contribution = avg_sale - variable_cost

    # Sales needed to cover the promotion
    if contribution <= 0:
        sales_needed = None
    else:
        sales_needed = math.ceil(promo_expense / contribution)

    return contribution, sales_needed


# Calculator Three (calc3.py) - Price and cost changes
def scenario(price, variable_cost, fixed_costs, volume):
    """Return (contribution, break_even, profit) for one scenario.

    break_even is rounded up to a whole sale, or None when contribution <= 0.
    """
    # Contribution per sale
    contribution = price - variable_cost

    # Monthly operating profit
    profit = volume * contribution - fixed_costs

    # Break-even sales
    if contribution > 0:
        break_even = math.ceil(fixed_costs / contribution)
    else:
        break_even = None

    return contribution, break_even, profit


def compare(current_price, proposed_price, variable_cost, fixed_costs,
            sales_volume, proposed_sales_volume):
    """Return (current, proposed, change_profit).

    current and proposed are each the tuple returned by scenario().
    """
    current = scenario(current_price, variable_cost, fixed_costs, sales_volume)
    proposed = scenario(proposed_price, variable_cost, fixed_costs, proposed_sales_volume)
    change_profit = proposed[2] - current[2]
    return current, proposed, change_profit
