from flask import Flask, render_template, request, redirect, url_for, flash
import matplotlib.pyplot as plt
import io
import base64
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Mock data for income and expenses over time (add datetime for demonstration)
expenses = [{'description': 'Rent', 'amount': 500, 'date': datetime.date(2024, 10, 1)},
            {'description': 'Groceries', 'amount': 200, 'date': datetime.date(2024, 10, 5)}]

income = [{'description': 'Salary', 'amount': 1500, 'date': datetime.date(2024, 10, 1)},
          {'description': 'Bonus', 'amount': 300, 'date': datetime.date(2024, 10, 10)}]

budget = 0

# Route for home page
@app.route('/')
def home():
    total_income = sum([i['amount'] for i in income])
    total_expenses = sum([e['amount'] for e in expenses])
    remaining_budget = total_income - total_expenses  # Corrected
    return render_template('index.html', income=total_income, expenses=total_expenses, budget=remaining_budget)

# Route for managing expenses
@app.route('/expenses', methods=['GET', 'POST'])
def manage_expenses():
    if request.method == 'POST':
        description = request.form['expense']
        amount = float(request.form['amount'])
        date = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        expenses.append({'description': description, 'amount': amount, 'date': date})
        flash('Expense added successfully!')
        return redirect(url_for('manage_expenses'))
    return render_template('expenses.html', expenses=expenses)

# Route for managing income
@app.route('/income', methods=['GET', 'POST'])
def manage_income():
    if request.method == 'POST':
        description = request.form['income']
        amount = float(request.form['amount'])
        date = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        income.append({'description': description, 'amount': amount, 'date': date})
        flash('Income added successfully!')
        return redirect(url_for('manage_income'))
    return render_template('income.html', income=income)

# Route for expense and income analysis with line graph
@app.route('/analysis')
def show_analysis():
    total_income = sum([i['amount'] for i in income])
    total_expenses = sum([e['amount'] for e in expenses])
    remaining_budget = total_income - total_expenses  # Corrected

    # Extract data for line graph
    dates = sorted(list(set([i['date'] for i in income] + [e['date'] for e in expenses])))

    # Create cumulative income and expenses over time
    income_by_date = {d: 0 for d in dates}
    expenses_by_date = {d: 0 for d in dates}

    for i in income:
        income_by_date[i['date']] += i['amount']

    for e in expenses:
        expenses_by_date[e['date']] += e['amount']

    cumulative_income = []
    cumulative_expenses = []
    total_inc = total_exp = 0

    for date in dates:
        total_inc += income_by_date[date]
        total_exp += expenses_by_date[date]
        cumulative_income.append(total_inc)
        cumulative_expenses.append(total_exp)

    # Plot the income and expenses over time using a line graph
    fig, ax = plt.subplots()
    ax.plot(dates, cumulative_income, label="Income", color="green", marker='o')
    ax.plot(dates, cumulative_expenses, label="Expenses", color="red", marker='o')
    ax.set_xlabel('Date')
    ax.set_ylabel('Amount (Tenge)')
    ax.set_title('Income vs Expenses Over Time')
    ax.legend()

    # Convert plot to PNG image and then to base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('analysis.html', income=total_income, expenses=total_expenses, budget=remaining_budget, plot_url=plot_url)


# Route for tax calculator
@app.route('/tax_calculator', methods=['GET', 'POST'])
def tax_calculator():
    tax_amount = 0
    if request.method == 'POST':
        income_value = float(request.form['income_value'])
        tax_percentage = float(request.form['tax_percentage'])
        tax_amount = (tax_percentage / 100) * income_value
    return render_template('tax_calculator.html', tax_amount=tax_amount)

if __name__ == '__main__':
    app.run(debug=True)
