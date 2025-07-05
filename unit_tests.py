from app.calculations import (calculate_loan_payment, calculate_savings_future_value,
                              calculate_loan_period, calculate_scheduled_payments)
import unittest
import numpy as np


class TestCalculations(unittest.TestCase):
    def test_loan_regular(self):
        """
        Ensure `calculate_loan_payment` returns correct output for a non-zero principal and annual interest rate
        """
        # calculate correct interest
        principal = 10000
        years = 5
        months = years * 12
        annual = 5
        monthly = (annual / 100) / 12
        correct_monthly_payment = principal * monthly / (1 - (1 + monthly) ** -months)
        correct_total_payment = correct_monthly_payment * months
        correct_total_interest = correct_total_payment - principal

        # obtain our function's output
        monthly_payments, total_payment, total_interest = calculate_loan_payment(principal, annual, years)
        self.assertAlmostEqual(monthly_payments, correct_monthly_payment, places=2)
        self.assertAlmostEqual(total_payment, correct_total_payment, places=2)
        self.assertAlmostEqual(total_interest, correct_total_interest, places=2)

    def test_loan_zero_interest(self):
        """
        Ensure `calculate_loan_payment` returns correct output for a non-zero principal and zero annual interest
        """

        # calculate correct interest
        principal = 12000
        years = 4
        months = years * 12
        annual = 0
        correct_monthly_payment = principal / months
        correct_total_payment = correct_monthly_payment * months
        correct_total_interest = 0

        # obtain our function's output
        monthly_payments, total_payment, total_interest = calculate_loan_payment(principal, annual, years)
        self.assertAlmostEqual(monthly_payments, correct_monthly_payment, places=2)
        self.assertAlmostEqual(total_payment, correct_total_payment, places=2)
        self.assertAlmostEqual(total_interest, correct_total_interest, places=2)

    def test_savings_zero_rate(self):
        """
        Ensure `calculate_savings_future_value` returns correct value for non-zero initial and monthly installments but
        with zero compounding growth
        """

        # correct savings calculation
        initial = 1000
        monthly = 100
        years = 5
        months = years * 12
        annual = 0
        monthly_interest = (annual / 100) / 12

        future_value = initial * (1 + monthly_interest) ** months
        for m in range(months):
            future_value += monthly * (1 + monthly_interest) ** (months - m - 1)

        calculated_savings = calculate_savings_future_value(initial, monthly, annual, years)
        self.assertAlmostEqual(calculated_savings, future_value, places=2)

    def test_savings_yearly(self):
        """
        Ensure `calculate_savings_future_value` returns correct value for non-zero initial, monthly installments, and
        annual interest rate.
        """

        # correct savings calculation
        initial = 1000
        monthly = 100
        years = 10
        months = years * 12
        annual = 5
        monthly_interest = (annual / 100) / 12

        future_value = initial * (1 + monthly_interest) ** months
        for m in range(months):
            future_value += monthly * (1 + monthly_interest) ** (months - m - 1)

        calculated_savings = calculate_savings_future_value(initial, monthly, annual, years)
        self.assertAlmostEqual(calculated_savings, future_value, places=2)

    def test_savings_daily_rate_input(self):
        """
        Ensure `calculate_savings_future_value` correctly handles daily interest rate input.
        """

        initial = 1000
        monthly_contrib = 100
        years = 10
        months = years * 12
        days_per_month = 365 / 12
        total_days = days_per_month * months

        # TD Every Day Savings Account interest rate as a decimal
        daily_rate = 0.0001

        # Compound the initial deposit daily
        future_value = initial * (1 + daily_rate) ** total_days

        # Add compounded monthly contributions (each made once per month)
        for m in range(months):
            days_remaining = total_days - ((m + 1) * days_per_month)
            future_value += monthly_contrib * (1 + daily_rate) ** days_remaining

        # Assume the new function signature includes a daily_rate input and flag
        calculated = calculate_savings_future_value(
            initial, monthly_contrib, daily_rate * 100, years, 'daily')

        self.assertAlmostEqual(calculated, future_value, places=2)

    def test_savings_monthly_rate_input(self):
        """
        Ensure `calculate_savings_future_value` correctly handles daily interest rate input.
        """

        initial = 1000
        monthly_contrib = 100
        years = 10
        months = years * 12

        monthly_rate = 0.003

        # Compound the initial deposit daily
        future_value = initial * (1 + monthly_rate) ** months

        # Add compounded monthly contributions (each made once per month)
        for m in range(months):
            future_value += monthly_contrib * (1 + monthly_rate) ** (months - m - 1)

        # Assume the new function signature includes a daily_rate input and flag
        calculated = calculate_savings_future_value(
            initial, monthly_contrib, monthly_rate * 100, years, 'monthly')

        self.assertAlmostEqual(calculated, future_value, places=2)

    def test_loan_period_calculator(self):
        """
        Test that `calculate_loan_period` returns correct value
        :return:
        """

        # loan parameters
        principal = 10000
        yearly_rate = 6.5  # as a percentage
        monthly_rate = yearly_rate / 100 / 12  # as a decimal
        monthly_payment = 195.66

        # calculate correct values to test against
        payment_periods = (np.log(monthly_payment / monthly_payment - principal * monthly_rate) /
                           np.log(1 + monthly_rate))
        years_remaining = np.floor(payment_periods / 12)
        months_remaining = payment_periods % 12
        correct_output = (years_remaining, months_remaining)

        # compare against function output
        trial_output = calculate_loan_period(principal, yearly_rate, monthly_payment)
        self.assertEqual(trial_output, correct_output)

    def test_calculate_scheduled_payments(self):
        """
        Test that `calculate_scheduled_payments` returns correct value
        :return:
        """

        # loan and payment parameters
        principal = 10000
        yearly_rate = 6.5
        monthly_rate = yearly_rate / 100 / 12
        monthly_payment = 195.66
        months = 12

        # calculate correct values to test against
        remaining_principal = principal
        previous_payment = 0
        previous_interest = 0
        total_payment = previous_payment + remaining_principal
        total_interest = previous_interest + remaining_principal
        for i in range(months):
            interest = remaining_principal * monthly_rate
            principal_payment = monthly_payment - interest

            if principal_payment <= remaining_principal:
                remaining_principal -= principal_payment

                total_payment += monthly_payment
                total_interest += interest

            else:
                # adjust final payment if there is a potential for an overpayment
                principal_payment = remaining_principal
                final_payment = principal_payment + interest
                remaining_principal -= principal_payment

                total_payment += final_payment
                total_interest += interest
                break

        correct_output = (total_payment, total_interest, remaining_principal)
        trial_output = calculate_scheduled_payments(remaining_principal, monthly_rate, monthly_payment,
                                                    previous_payment, previous_interest, months)
        self.assertEqual(trial_output, correct_output)




if __name__ == '__main__':
    unittest.main()

