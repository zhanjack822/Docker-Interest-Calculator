from math import log as ln, ceil, floor
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


def calculate_savings_future_value(initial: float, monthly: float, comp_rate: float, years: int,
                                   compounding_period: str = 'yearly') -> float:
    """
    Calculate total savings in a savings account with some initial amount saved, a fixed monthly contributions, some
    fixed annual compounding rate, and the savings period.

    :param float initial: initial savings amount
    :param float monthly: monthly contribution
    :param float comp_rate: compounding rate as a percentage
    :param int years: savings period in years
    :param str compounding_period: period of compounding ('daily', 'monthly', or 'yearly')
    :return: total value of savings at the end of the savings period
    """

    months = years * 12

    if compounding_period == 'monthly':
        monthly_rate = comp_rate / 100

        # Compound the initial deposit daily
        future_value = initial * (1 + monthly_rate) ** months

        # Add compounded monthly contributions (each made once per month)
        for m in range(months):
            future_value += monthly * (1 + monthly_rate) ** (months - m - 1)

    elif compounding_period == 'daily':
        days_per_month = 365 / 12
        total_days = days_per_month * months

        daily_rate = comp_rate / 100

        # Compound the initial deposit daily
        future_value = initial * (1 + daily_rate) ** total_days

        # Add compounded monthly contributions (each made once per month)
        for m in range(months):
            days_remaining = total_days - ((m + 1) * days_per_month)
            future_value += monthly * (1 + daily_rate) ** days_remaining

    else:
        # default to yearly compounding rate
        monthly_rate = comp_rate / 100 / 12
        future_value = initial * (1 + monthly_rate) ** months
        for m in range(months):
            future_value += monthly * (1 + monthly_rate) ** (months - m - 1)


    return future_value


def calculate_loan_period(remaining_principal: float, annual_rate: float, monthly_payment: float) -> tuple[int, int]:
    """
    Calculate the time needed to pay off a loan given the remaining principal, annual interest rate, and monthly payment.

    :param float remaining_principal: remaining principal amount
    :param float annual_rate: annual interest rate as a percentage
    :param float monthly_payment: monthly payment amount
    :return: tuple containing years and months needed to pay off the loan
    """
    if remaining_principal <= 0:
        return (0, 0)

    monthly_rate = annual_rate / 100 / 12

    if monthly_rate == 0:
        payment_periods = remaining_principal / monthly_payment
        years_remaining = floor(payment_periods / 12)
        months_remaining = floor(payment_periods % 12)
    else:
        # calculate correct values to test against
        payment_periods = (ln(monthly_payment / (monthly_payment - remaining_principal * monthly_rate)) /
                           ln(1 + monthly_rate))
        years_remaining = floor(payment_periods / 12)
        months_remaining = ceil(payment_periods % 12)

    return (years_remaining, months_remaining)


def calculate_scheduled_payments(remaining_principal: float, annual_rate: float, monthly_payment: float,
                                 previous_total_payments: float, previous_interest_paid: float,
                                 payment_period_months: int) -> tuple[float, float, float]:
    """
    Calculate scheduled payments for a specific period.

    :param float remaining_principal: remaining principal amount
    :param float annual_rate: annual interest rate as a percentage
    :param float monthly_payment: monthly payment amount
    :param float previous_total_payments: total payments made in previous periods
    :param float previous_interest_paid: total interest paid in previous periods
    :param int payment_period_months: duration of payment period in months
    :return: tuple containing total payments made during period, total interest paid thus far, and remaining principal
    """
    monthly_rate = annual_rate / 100 / 12
    current_principal = remaining_principal
    period_payments = 0
    period_interest = 0

    for month in range(payment_period_months):
        if current_principal <= 0:
            break

        interest_payment = current_principal * monthly_rate
        principal_payment = min(monthly_payment - interest_payment, current_principal)

        period_payments += interest_payment + principal_payment
        period_interest += interest_payment
        current_principal -= principal_payment

        if current_principal <= 0:
            break

    total_payments_so_far = previous_total_payments + period_payments
    total_interest_so_far = previous_interest_paid + period_interest

    return (total_payments_so_far, total_interest_so_far, current_principal)