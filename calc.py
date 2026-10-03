# Calculator One - Are AI tools worth it

# Inputs

# Task workload per month (i.e. 40 emails/month)
monthly_tasks = float(input("How many tasks do you complete per month? "))

minutes_without = float(input("How many minutes do you spend on this task without AI? "))

# How many minutes on each task with AI
ai_minutes = float(input("How many minutes do you spend per task with AI? "))

# What is your time worth
hourly_value = float(input("What is your time worth per hour? $"))

# Monthly tool costs
monthly_cost = float(input("What is the monthly cost of your AI tool? $"))

# Time to setup AI
setup_hours = float(input("How many hours does it take to set up the AI tool? This could include but is not limited to user preferences, relevant context windows, and connection to other tools. "))

# One-time setup cost
setup_cash = float(input("What is your one-time cash setup cost? $"))

# Net hours saved
net_hours = ((minutes_without - ai_minutes) * monthly_tasks) / 60

if ai_minutes >= minutes_without:
    print("Your current setup doesn't save time on this task")
    
# Estimated value of time before tool costs
time_value = (net_hours * hourly_value) 

# Monthly net savings

monthly_net = time_value - monthly_cost

# Setup cost 

setup_cost = setup_cash + setup_hours * hourly_value 

# Wraps display in f string, prints value to one and two decimals respectively. 

print(f"Hours saved per month: {net_hours:.1f}")
print(f"Value of time saved: ${time_value:,.2f}")
print(f"Monthly value after tool cost: ${monthly_net:,.2f}")

if monthly_net > 0:
    print(f"Setup payback: {setup_cost / monthly_net:.2f} months")
else:
    print("Setup is not recovered under your inputs. ")


