import unittest
from app.calculations import calculate_loan_payment, calculate_savings_future_value

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

    def test_savings_regular(self):
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
        interest = (annual / 100) / 12

        final = initial * (1 + interest) ** months
        for m in range(months):
            final += monthly * (1 + interest) ** (months - m - 1)

        calculated_savings = calculate_savings_future_value(initial, monthly, annual, years)
        self.assertAlmostEqual(calculated_savings, final, places=2)

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
        interest = (annual / 100) / 12

        final = initial * (1 + interest) ** months
        for m in range(months):
            final += monthly * (1 + interest) ** (months - m - 1)

        calculated_savings = calculate_savings_future_value(initial, monthly, annual, years)
        self.assertAlmostEqual(calculated_savings, final, places=2)


if __name__ == '__main__':
    unittest.main()

