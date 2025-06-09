def calculate_loan_payment(principal, annual_rate, years):
    monthly_rate = annual_rate / 100 / 12
    months = years * 12
    if monthly_rate == 0:
        monthly_payment = principal / months
    else:
        monthly_payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** -months)
    total_paid = monthly_payment * months
    total_interest = total_paid - principal
    return monthly_payment, total_paid, total_interest

def calculate_savings_future_value(initial, monthly, annual_rate, years):
    months = years * 12
    monthly_rate = annual_rate / 100 / 12
    future_value = initial * (1 + monthly_rate) ** months
    for m in range(months):
        future_value += monthly * (1 + monthly_rate) ** (months - m - 1)
    return future_value
