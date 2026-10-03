# Small Business Decision Calculators

Three simple calculators for small business decisions, in a Streamlit app:

1. **AI Tool Value**: is an AI tool worth its cost?
2. **Promotion Break-Even**: how many extra sales cover a promotion?
3. **Price & Cost Changes**: how a price or volume change affects operating profit.

The math is in `calculators.py` (pure functions, no input/output). `app.py` is the web UI. The original command-line scripts (`calc.py`, `calc2.py`, `calc3.py`) are unchanged.

## How to run

```bash
pip install -r requirements.txt
streamlit run app.py
pytest
```

## Formulas

### 1. AI Tool Value (`ai_tool_value`)

- Net hours saved = (minutes without AI − minutes with AI) × monthly tasks ÷ 60
- Value of time saved = net hours × hourly value
- Monthly value after tool cost = value of time saved − monthly tool cost
- Setup cost = setup cash + setup hours × hourly value
- Setup payback (months) = setup cost ÷ monthly value after tool cost (only when that is above 0)

### 2. Promotion Break-Even (`promo_break_even`)

- Contribution per sale = average sale − variable cost per sale
- Sales needed = promotion expense ÷ contribution, rounded up to a whole sale (only when contribution is above 0)

### 3. Price & Cost Changes (`scenario`, `compare`)

For each scenario (current and proposed):

- Contribution per sale = price − variable cost
- Operating profit = sales volume × contribution − monthly fixed costs
- Break-even sales = fixed costs ÷ contribution, rounded up (only when contribution is above 0)

Change in profit = proposed operating profit − current operating profit.

## Assumptions

- **AI Tool Value**: time saved is valued at your hourly rate. It is time value, not cash. Tool cost and setup cash are real cash costs. Setup hours are counted at your hourly rate. Task volume and minutes per task stay the same each month.
- **Promotion Break-Even**: average sale is after discounts, and variable cost includes fulfillment and transaction costs. The result is a threshold. It does not predict demand or prove the promotion caused a sale.
- **Price & Cost Changes**: uses an average sale. Variable cost and fixed costs are the same in both scenarios. Price changes often affect sales volume, so try different proposed volumes.
- If a sale doesn't make money (contribution of 0 or less), break-even is reported as not reachable.
