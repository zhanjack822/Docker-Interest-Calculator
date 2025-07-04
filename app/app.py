from flask import Flask, render_template, request
from .calculations import calculate_loan_payment, calculate_savings_future_value
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/loan', methods=['POST'])
def loan() -> str:
    """
    Renders the Loan calculator
    :return: updated html with loan calculator
    """

    principal = float(request.form['principal'])
    rate = float(request.form['rate'])
    years = int(request.form['years'])

    monthly_payment, total_paid, total_interest = calculate_loan_payment(principal, rate, years)

    return render_template('result.html', result={
        "type": "Loan",
        "monthly_payment": f"${monthly_payment:.2f}",
        "total_paid": f"${total_paid:.2f}",
        "total_interest": f"${total_interest:.2f}"
    })

@app.route('/savings', methods=['POST'])
def savings() -> str:
    """
    Renders savings calculator
    :return: updated html with savings calculator
    """

    initial = float(request.form['initial'])
    monthly = float(request.form['monthly'])
    rate = float(request.form['rate'])
    years = int(request.form['years'])
    compounding_period = request.form['compounding_period']

    future_value = calculate_savings_future_value(initial, monthly, rate, years, compounding_period)

    return render_template('result.html', result={
        "type": "Savings",
        "future_value": f"${future_value:.2f}"
    })

if __name__ == "__main__":
    app.run(debug=True)