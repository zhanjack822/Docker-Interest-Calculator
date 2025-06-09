import unittest
from calculations import calculate_loan_payment, calculate_savings_future_value

class TestCalculations(unittest.TestCase):
    def test_loan_regular(self):
        m, t, i = calculate_loan_payment(10000, 5, 5)
        self.assertAlmostEqual(m, 188.71, places=2)
        self.assertAlmostEqual(t, 11322.74, places=2)
        self.assertAlmostEqual(i, 1322.74, places=2)

    def test_loan_zero_interest(self):
        m, t, i = calculate_loan_payment(12000, 0, 4)
        self.assertEqual(m, 250.0)
        self.assertEqual(t, 12000.0)
        self.assertEqual(i, 0.0)

    def test_savings_regular(self):
        fv = calculate_savings_future_value(1000, 100, 5, 10)
        self.assertAlmostEqual(fv, 16470.09, places=2)

    def test_savings_zero_rate(self):
        fv = calculate_savings_future_value(1000, 100, 0, 5)
        self.assertEqual(fv, 1000 + 100 * 12 * 5)

if __name__ == '__main__':
    unittest.main()
