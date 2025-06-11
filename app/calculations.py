def calculate_loan_payment(principal: float, annual_rate: float, years: int) -> tuple[float, float, float]:
    """
    Calculate the monthly payment, total amount paid, and total interest payments on a loan with a given principal,
    annual interest rate, and payment period in years.

    :param float principal: Principal loan amount
    :param float annual_rate: annual interest rate as a percentage
    :param int years: loan period in years
    :return: tuple containing monthly payment, total amount paid, and total interest paid in that order
    """

    monthly_rate = annual_rate / 100 / 12
    months = years * 12
    if monthly_rate == 0:
        monthly_payment = principal / months
    else:
        monthly_payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** -months)
    total_paid = monthly_payment * months
    total_interest = total_paid - principal
    return monthly_payment, total_paid, total_interest

def calculate_savings_future_value(initial: float, monthly: float, comp_rate: float, years: int) -> float:
    """
    Calculate total savings in a savings account with some initial amount saved, a fixed monthly contributions, some
    fixed annual compounding rate, and the savings period.

    :param float initial: initial savings amount
    :param float monthly: monthly contribution
    :param float comp_rate: annual compounding rate as a percentage
    :param int years: savings period in years
    :return: total value of savings at the end of the savings period
    """

    months = years * 12
    monthly_rate = comp_rate / 100 / 12
    future_value = initial * (1 + monthly_rate) ** months
    for m in range(months):
        future_value += monthly * (1 + monthly_rate) ** (months - m - 1)
    return future_value