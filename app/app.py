from flask import Flask, render_template, request
from .calculations import calculate_loan_payment, calculate_savings_future_value
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# check where other directories are
print("Current working dir:", os.getcwd())
print("Contents of working dir:", os.listdir())
print("Full path contents of working dir:")
for item in os.listdir():
    print(" -", os.path.abspath(item))
templates_path = os.path.join(os.path.dirname(__file__), 'templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/loan', methods=['POST'])
def loan():
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
def savings():
    initial = float(request.form['initial'])
    monthly = float(request.form['monthly'])
    rate = float(request.form['rate'])
    years = int(request.form['years'])

    future_value = calculate_savings_future_value(initial, monthly, rate, years)

    return render_template('result.html', result={
        "type": "Savings",
        "future_value": f"${future_value:.2f}"
    })

if __name__ == "__main__":
    app.run(debug=True)
