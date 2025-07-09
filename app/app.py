from flask import Flask, render_template, request, session, jsonify, redirect
from .calculations import calculate_loan_payment, calculate_savings_future_value, calculate_loan_period, calculate_scheduled_payments
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))

app.secret_key = 'your-secret-key-here'
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

    # Store loan details in session for payment schedule calculator
    session['loan_data'] = {
        'principal': principal,
        'rate': rate,
        'years': years,
        'monthly_payment': monthly_payment,
        'total_paid': total_paid,
        'total_interest': total_interest
    }

    # flag to enable the scheduled payments calculator
    should_enable_payment_plan = True

    return render_template('result.html', result={
        "type": "Loan",
        "monthly_payment": f"${monthly_payment:.2f}",
        "total_paid": f"${total_paid:.2f}",
        "total_interest": f"${total_interest:.2f}"
    }, enable_payment_plan=should_enable_payment_plan)


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


@app.route('/payment-schedule')
def payment_schedule():
    """
    Renders the payment schedule calculator
    """
    if 'loan_data' not in session:
        return redirect('/')

    return render_template('schedule_calculator.html', loan_data=session['loan_data'])


@app.route('/calculate-loan-period', methods=['POST'])
def calculate_loan_period_route():
    """
    API endpoint to calculate loan period
    """
    data = request.get_json()
    remaining_principal = float(data['remaining_principal'])
    annual_rate = float(data['annual_rate'])
    monthly_payment = float(data['monthly_payment'])

    years, months = calculate_loan_period(remaining_principal, annual_rate, monthly_payment)

    return jsonify({
        'years': years,
        'months': months
    })


@app.route('/calculate-scheduled-payments', methods=['POST'])
def calculate_scheduled_payments_route():
    """
    API endpoint to calculate scheduled payments
    """
    data = request.get_json()
    remaining_principal = float(data['remaining_principal'])
    annual_rate = float(data['annual_rate'])
    monthly_payment = float(data['monthly_payment'])
    previous_total_payments = float(data['previous_total_payments'])
    previous_interest_paid = float(data['previous_interest_paid'])
    payment_period_months = int(data['payment_period_months'])

    total_payments, total_interest, remaining = calculate_scheduled_payments(
        remaining_principal, annual_rate, monthly_payment,
        previous_total_payments, previous_interest_paid, payment_period_months
    )

    return jsonify({
        'total_payments': total_payments,
        'total_interest': total_interest,
        'remaining_principal': remaining
    })

if __name__ == "__main__":
    app.run(debug=True)