from app.calculations import (calculate_loan_payment, calculate_savings_future_value,
                              calculate_loan_period, calculate_scheduled_payments)
import unittest
from math import log as ln, ceil, floor


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
        self.assertAlmostEqual(correct_monthly_payment, monthly_payments, places=2)
        self.assertAlmostEqual(correct_total_payment, total_payment, places=2)
        self.assertAlmostEqual(correct_total_interest, total_interest, places=2)

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
        self.assertAlmostEqual(correct_monthly_payment, monthly_payments, places=2)
        self.assertAlmostEqual(correct_total_payment, total_payment, places=2)
        self.assertAlmostEqual(correct_total_interest, total_interest, places=2)

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
        self.assertAlmostEqual(future_value, calculated_savings, places=2)

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
        self.assertAlmostEqual(future_value, calculated_savings, places=2)

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

        self.assertAlmostEqual(future_value, calculated, places=2)

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

        self.assertAlmostEqual(future_value, calculated, places=2)

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
        payment_periods = (ln(monthly_payment / (monthly_payment - principal * monthly_rate)) /
                           ln(1 + monthly_rate))
        years_remaining = floor(payment_periods / 12)
        months_remaining = ceil(payment_periods % 12)
        correct_output = (years_remaining, months_remaining)

        # compare against function output
        trial_output = calculate_loan_period(principal, yearly_rate, monthly_payment)
        self.assertEqual(correct_output, trial_output)


    def test_payed_off_loan_period_calculator(self):
        """
        Test that `calculate_loan_period` returns correct value when the loan is fully paid off
        :return:
        """

        # loan parameters
        principal = 0
        yearly_rate = 6.5  # as a percentage
        monthly_rate = yearly_rate / 100 / 12  # as a decimal
        monthly_payment = 195.66

        # calculate correct values to test against
        payment_periods = (ln(monthly_payment / (monthly_payment - principal * monthly_rate)) /
                           ln(1 + monthly_rate))
        years_remaining = floor(payment_periods / 12)
        months_remaining = ceil(payment_periods % 12)
        correct_output = (years_remaining, months_remaining)

        # compare against function output
        trial_output = calculate_loan_period(principal, yearly_rate, monthly_payment)
        self.assertEqual(correct_output, trial_output)

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
        payments_made = 0
        interest_paid = 0
        for i in range(months):
            interest = remaining_principal * monthly_rate
            principal_payment = monthly_payment - interest

            if principal_payment <= remaining_principal:
                remaining_principal -= principal_payment

                payments_made += monthly_payment
                interest_paid += interest

            else:
                # adjust final payment if there is a potential for an overpayment
                principal_payment = remaining_principal
                final_payment = principal_payment + interest
                remaining_principal -= principal_payment

                payments_made += final_payment
                interest_paid += interest
                break

        total_payment = previous_payment + payments_made
        total_interest = previous_interest + interest_paid

        correct_output = (total_payment, total_interest, principal - (payments_made - interest_paid))
        trial_output = calculate_scheduled_payments(principal, yearly_rate, monthly_payment,
                                                    previous_payment, previous_interest, months)
        for i in range(3):
            self.assertAlmostEqual(correct_output[i], trial_output[i])

    def test_calculate_overextended_scheduled_payments(self):
        """
        Test that `calculate_scheduled_payments` returns correct value when payment period is too long
        :return:
        """

        # loan and payment parameters
        principal = 10000
        yearly_rate = 6.5
        monthly_rate = yearly_rate / 100 / 12
        monthly_payment = 195.66
        months = 70

        # calculate correct values to test against
        remaining_principal = principal
        previous_payment = 0
        previous_interest = 0
        payments_made = 0
        interest_paid = 0
        for i in range(months):
            interest = remaining_principal * monthly_rate
            principal_payment = monthly_payment - interest

            if principal_payment <= remaining_principal:
                remaining_principal -= principal_payment

                payments_made += monthly_payment
                interest_paid += interest

            else:
                # adjust final payment if there is a potential for an overpayment
                principal_payment = remaining_principal
                final_payment = principal_payment + interest
                remaining_principal -= principal_payment

                payments_made += final_payment
                interest_paid += interest
                break

        total_payment = previous_payment + payments_made
        total_interest = previous_interest + interest_paid

        correct_output = (total_payment, total_interest, principal - (payments_made - interest_paid))
        trial_output = calculate_scheduled_payments(principal, yearly_rate, monthly_payment,
                                                    previous_payment, previous_interest, months)
        for i in range(3):
            self.assertAlmostEqual(correct_output[i], trial_output[i])


    def test_calculate_scheduled_overpayment(self):
        """
        Test that `calculate_scheduled_payments` returns correct value when there is an overpayment in the
        second month
        :return:
        """

        # loan and payment parameters
        principal = 194.71
        yearly_rate = 6.5
        monthly_rate = yearly_rate / 100 / 12
        monthly_payment = 195.66
        months = 10

        # calculate correct values to test against
        remaining_principal = principal
        previous_payment = 11543.94
        previous_interest = 1738.65
        payments_made = 0
        interest_paid = 0
        for i in range(months):
            interest = remaining_principal * monthly_rate
            principal_payment = monthly_payment - interest

            if principal_payment <= remaining_principal:
                remaining_principal -= principal_payment

                payments_made += monthly_payment
                interest_paid += interest

            else:
                # adjust final payment if there is a potential for an overpayment
                principal_payment = remaining_principal
                final_payment = principal_payment + interest
                remaining_principal -= principal_payment

                payments_made += final_payment
                interest_paid += interest
                break

        total_payment = previous_payment + payments_made
        total_interest = previous_interest + interest_paid

        correct_output = (total_payment, total_interest, principal - (payments_made - interest_paid))
        trial_output = calculate_scheduled_payments(principal, yearly_rate, monthly_payment,
                                                    previous_payment, previous_interest, months)
        for i in range(3):
            self.assertAlmostEqual(correct_output[i], trial_output[i])




if __name__ == '__main__':
    unittest.main()

