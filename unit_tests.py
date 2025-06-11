import unittest
from app.calculations import calculate_loan_payment, calculate_savings_future_value

class TestCalculations(unittest.TestCase):
    def test_loan_regular(self):
        monthly_payments, total_payment, total_interest = calculate_loan_payment(10000, 5, 5)
        self.assertAlmostEqual(monthly_payments, 188.71, places=2)
        self.assertAlmostEqual(total_payment, 11322.74, places=2)
        self.assertAlmostEqual(total_interest, 1322.74, places=2)

    def test_loan_zero_interest(self):
        monthly_payments, total_payment, total_interest = calculate_loan_payment(12000, 0, 4)
        self.assertEqual(monthly_payments, 250.0)
        self.assertEqual(total_payment, 12000.0)
        self.assertEqual(total_interest, 0.0)

    def test_savings_regular(self):
        calculated_savings = calculate_savings_future_value(1000, 100, 5, 10)

        # correct savings calculation
        initial = 1000
        monthly = 100
        months = 120
        interest = (5 / 100) / 12

        final = initial * (1 + interest) ** months
        for m in range(months):
            final += monthly * (1 + interest) ** (months - m - 1)

        self.assertAlmostEqual(calculated_savings, final, places=2)

    def test_savings_zero_rate(self):
        fv = calculate_savings_future_value(1000, 100, 0, 5)
        self.assertEqual(fv, 1000 + 100 * 12 * 5)

if __name__ == '__main__':
    unittest.main()
