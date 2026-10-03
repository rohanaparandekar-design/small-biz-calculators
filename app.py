import streamlit as st

from calculators import ai_tool_value, promo_break_even, scenario, compare


def money(value):
    """Format a number as $1,234.56 (negatives as -$1,234.56)."""
    if value < 0:
        return f"-${abs(value):,.2f}"
    return f"${value:,.2f}"


def signed_money(value):
    """Format a change as +$1,234.56 / -$1,234.56."""
    return f"+{money(value)}" if value > 0 else money(value)


def signed_money_short(value):
    """Like signed_money, but drops ".00" for whole dollars (for headlines)."""
    text = signed_money(value)
    return text[:-3] if text.endswith(".00") else text


def headline(kind, text, detail=None):
    """Show the headline answer as a large, color-coded line.

    kind: "good" (green), "bad" (red), "unreachable" (yellow) or "neutral" (blue).
    """
    show = {"good": st.success, "bad": st.error,
            "unreachable": st.warning, "neutral": st.info}[kind]
    body = f"### {text}"
    if detail:
        body += f"\n\n{detail}"
    show(body)


st.set_page_config(page_title="Small Business Decision Calculators", layout="centered")

# Streamlit draws labels, tabs and captions at 14px by default; bring them up
# to the 16px body size (set by baseFontSize in .streamlit/config.toml) so
# they are readable on a phone.
st.html("""
<style>
[data-testid="stWidgetLabel"] p { font-size: 1rem; }
[data-testid="stMetricLabel"] p { font-size: 1rem; }
[data-testid="stCaptionContainer"] { font-size: 1rem; }
[data-testid="stTab"] p { font-size: 1.05rem; font-weight: 600; }
</style>
""")

st.title("Small Business Decision Calculators")
st.caption("Quick break-even and profit checks for small business owners deciding on tools, promotions and prices.")

tab1, tab2, tab3 = st.tabs(["AI Tool Value", "Promotion Break-Even", "Price & Cost Changes"])


# Calculator One - Are AI tools worth it
with tab1:
    # (1) Inputs
    st.subheader("Are AI tools worth it?")
    time_col, cash_col = st.columns(2)
    with time_col:
        st.markdown("**Time**")
        monthly_tasks = st.number_input(
            "Tasks per month", min_value=0, value=40, step=1,
            help="How many tasks do you complete per month? Task workload per month (i.e. 40 emails/month).",
        )
        minutes_without = st.number_input(
            "Minutes per task without AI", min_value=0.0, value=15.0, step=1.0,
            help="How many minutes do you spend on this task without AI?",
        )
        ai_minutes = st.number_input(
            "Minutes per task with AI", min_value=0.0, value=6.0, step=1.0,
            help="How many minutes do you spend per task with AI?",
        )
        hourly_value = st.number_input(
            "Value of your time ($/hour)", min_value=0.0, value=30.0, step=1.0, format="%.2f",
            help="What is your time worth per hour?",
        )
    with cash_col:
        st.markdown("**Cash**")
        monthly_cost = st.number_input(
            "AI tool cost per month ($)", min_value=0.0, value=20.0, step=1.0, format="%.2f",
            help="What is the monthly cost of your AI tool?",
        )
        setup_cash = st.number_input(
            "One-time setup cash ($)", min_value=0.0, value=0.0, step=1.0, format="%.2f",
            help="What is your one-time cash setup cost?",
        )
        setup_hours = st.number_input(
            "Setup hours", min_value=0.0, value=4.0, step=0.5,
            help="How many hours does it take to set up the AI tool? This could include but is not "
                 "limited to user preferences, relevant context windows, and connection to other tools.",
        )

    net_hours, time_value, monthly_net, payback = ai_tool_value(
        monthly_tasks, minutes_without, ai_minutes, hourly_value,
        monthly_cost, setup_hours, setup_cash,
    )

    with st.container(border=True):
        # (2) Headline answer
        if payback is None:
            headline("unreachable", "Doesn't pay back", "Setup is not recovered under your inputs.")
        else:
            headline("good", f"Pays back in {payback:.2f} months")
        if ai_minutes >= minutes_without:
            st.warning("Your current setup doesn't save time on this task")

        # (3) Supporting numbers
        st.markdown("**Time value** (not cash)")
        c1, c2 = st.columns(2)
        c1.metric("Hours saved per month", f"{net_hours:.1f}")
        c2.metric("Value of time saved", money(time_value))

        st.markdown("**Cash**")
        c1, c2 = st.columns(2)
        c1.metric("Tool cost per month", money(monthly_cost))
        c2.metric("One-time setup cash", money(setup_cash))

        st.markdown("**Net**")
        st.metric("Monthly value after tool cost", money(monthly_net))

    # (4) Caveats
    st.caption(
        "Time saved is valued at your hourly rate; it is not cash in hand. Tool cost and setup cash are cash. "
        "Payback compares setup cost (setup cash plus setup hours at your hourly rate) to monthly value after tool cost."
    )


# Calculator Two - Will this promotion cover its cost?
with tab2:
    # (1) Inputs
    st.subheader("Will this promotion cover its cost?")
    promo_expense = st.number_input(
        "Promotion cost ($)", min_value=0.0, value=300.0, step=10.0, format="%.2f",
        help="What is your total promotion expense?",
    )
    c1, c2 = st.columns(2)
    avg_sale = c1.number_input(
        "Average sale ($)", min_value=0.0, value=50.0, step=1.0, format="%.2f",
        help="What is your average sale amount? Sales should be reported after any relevant discounts.",
    )
    promo_variable_cost = c2.number_input(
        "Variable cost per sale ($)", min_value=0.0, value=30.0, step=1.0, format="%.2f",
        help="What is your total variable cost per sale? Include relevant fulfillment or transaction costs.",
    )

    contribution, sales_needed = promo_break_even(promo_expense, avg_sale, promo_variable_cost)

    with st.container(border=True):
        # (2) Headline answer
        if sales_needed is None:
            headline(
                "unreachable", "Break-even not reachable",
                "Your variable cost currently equals or exceeds your average sale. "
                "Additional sales do not cover the promotion under these assumptions.",
            )
        else:
            headline("good", f"{sales_needed:,} more sales to break even")

        # (3) Supporting numbers
        c1, c2 = st.columns(2)
        c1.metric("Contribution per sale", money(contribution))
        c2.metric("Promotion cost", money(promo_expense))

    # (4) Caveats
    st.caption("This is a threshold. It does not predict demand or prove the promotion caused a sale.")


# Calculator Three - Price and cost changes
with tab3:
    # (1) Inputs
    st.subheader("What happens if I change my price?")
    st.markdown("**Shared**")
    c1, c2 = st.columns(2)
    variable_cost = c1.number_input(
        "Variable cost per sale ($)", min_value=0.0, value=30.0, step=1.0, format="%.2f",
        key="t3_variable_cost", help="What is your variable cost per sale?",
    )
    fixed_costs = c2.number_input(
        "Monthly fixed costs ($)", min_value=0.0, value=2000.0, step=50.0, format="%.2f",
        help="What are your monthly fixed costs?",
    )

    cur_col, prop_col = st.columns(2)
    with cur_col:
        st.markdown("**Current**")
        current_price = st.number_input(
            "Current price ($)", min_value=0.0, value=50.0, step=1.0, format="%.2f",
            help="What is your current sale price?",
        )
        sales_volume = st.number_input(
            "Current monthly volume", min_value=0, value=150, step=1,
            help="What is your monthly sales volume?",
        )
    with prop_col:
        st.markdown("**Proposed**")
        proposed_price = st.number_input(
            "Proposed price ($)", min_value=0.0, value=50.0, step=1.0, format="%.2f",
            help="What is your proposed sale price?",
        )
        proposed_sales_volume = st.number_input(
            "Proposed monthly volume", min_value=0, value=150, step=1,
            help="What is your proposed monthly sales volume?",
        )

    current, proposed, change_profit = compare(
        current_price, proposed_price, variable_cost, fixed_costs,
        sales_volume, proposed_sales_volume,
    )
    cur_contrib, cur_break_even, cur_profit = current
    prop_contrib, prop_break_even, prop_profit = proposed

    with st.container(border=True):
        # (2) Headline answer
        if change_profit > 0:
            headline("good", f"{signed_money_short(change_profit)} / month",
                     f"Your proposed changes would increase operating profit by {money(change_profit)}")
        elif change_profit < 0:
            headline("bad", f"{signed_money_short(change_profit)} / month",
                     f"Your proposed changes would decrease operating profit by {money(abs(change_profit))}")
        else:
            headline("neutral", "No change / month", "Your proposed changes would not change operating profit")

        # (3) Supporting numbers
        def break_even_text(value):
            return "Not reachable" if value is None else f"{value:,}"

        def delta_or_none(diff, fmt):
            return None if diff == 0 else fmt(diff)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Current**")
            st.metric("Operating profit", money(cur_profit))
            st.metric("Contribution per sale", money(cur_contrib))
            st.metric("Break-even sales", break_even_text(cur_break_even))
        with c2:
            st.markdown("**Proposed**")
            st.metric("Operating profit", money(prop_profit),
                      delta=delta_or_none(change_profit, signed_money))
            st.metric("Contribution per sale", money(prop_contrib),
                      delta=delta_or_none(prop_contrib - cur_contrib, signed_money))
            if cur_break_even is None or prop_break_even is None:
                be_delta = None
            else:
                be_delta = delta_or_none(prop_break_even - cur_break_even, lambda d: f"{d:+,} sales")
            # Fewer sales needed to break even is better, so invert the colors.
            st.metric("Break-even sales", break_even_text(prop_break_even),
                      delta=be_delta, delta_color="inverse")

        if cur_break_even is None:
            st.warning("In the current scenario, each sale loses money or breaks even. Review pricing and costs.")
        if prop_break_even is None:
            st.warning("In the proposed scenario, each sale loses money or breaks even. Review pricing and costs.")

    # (4) Caveats
    st.caption("Note: This assumes an average sale. Price changes often affect sales volume, so try different volumes.")
