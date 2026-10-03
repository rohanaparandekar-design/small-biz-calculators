import pytest
from calculators import ai_tool_value, promo_break_even, scenario, compare

# Calculator 1: returns (net_hours, time_value, monthly_net, payback)
def test_ai_jen_example():
    assert ai_tool_value(40, 15, 6, 30, 20, 4, 0) == pytest.approx((6, 180, 160, 0.75))

def test_ai_setup_cash():
    assert ai_tool_value(40, 15, 6, 30, 20, 4, 100)[3] == pytest.approx(1.375)

def test_ai_slower():
    assert ai_tool_value(40, 10, 12, 30, 20, 4, 0)[3] is None

def test_ai_tool_costs_more():
    assert ai_tool_value(10, 15, 12, 30, 20, 4, 0)[3] is None

def test_ai_zero_net():
    assert ai_tool_value(40, 15, 6, 30, 180, 4, 0)[3] is None

# Calculator 2: returns (contribution, sales_needed)
def test_promo_jen_example():
    assert promo_break_even(300, 50, 30) == (20, 15)

def test_promo_rounds_up():
    assert promo_break_even(310, 50, 30)[1] == 16

def test_promo_cost_equals_sale():
    assert promo_break_even(300, 50, 50)[1] is None

def test_promo_cost_exceeds_sale():
    assert promo_break_even(300, 50, 60)[1] is None

def test_promo_free():
    assert promo_break_even(0, 50, 30)[1] == 0

# Calculator 3: scenario returns (contribution, break_even, profit)
def test_scenario_jen_example():
    assert scenario(50, 30, 2000, 150) == (20, 100, 1000)

def test_scenario_price_up():
    assert scenario(60, 30, 2000, 150) == (30, 67, 2500)

def test_scenario_price_up_fewer_sales():
    assert scenario(60, 30, 2000, 100)[2] == 1000

def test_scenario_below_cost():
    assert scenario(25, 30, 2000, 150) == (-5, None, -2750)

def test_scenario_price_equals_cost():
    assert scenario(30, 30, 2000, 150) == (0, None, -2000)

# Calculator 3: compare returns (current, proposed, change_profit)
def test_compare_jen_example():
    assert compare(50, 50, 30, 2000, 150, 150) == ((20, 100, 1000), (20, 100, 1000), 0)

def test_compare_price_up():
    assert compare(50, 60, 30, 2000, 150, 150) == ((20, 100, 1000), (30, 67, 2500), 1500)

def test_compare_price_up_more_sales():
    assert compare(50, 60, 30, 2000, 150, 200) == ((20, 100, 1000), (30, 67, 4000), 3000)

def test_compare_price_up_fewer_sales():
    assert compare(50, 60, 30, 2000, 150, 100)[2] == 0

def test_compare_below_cost():
    assert compare(50, 25, 30, 2000, 150, 150) == ((20, 100, 1000), (-5, None, -2750), -3750)

def test_compare_price_equals_cost():
    assert compare(50, 30, 30, 2000, 150, 150) == ((20, 100, 1000), (0, None, -2000), -3000)
