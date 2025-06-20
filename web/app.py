from flask import Flask, render_template, request, send_from_directory

from db.utils import connect_to_db, generate_monthly_bill, modify_customer
from cli_app.visualizer import generate_visualization, CAPSTONE_HOME
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/customer', methods=['GET'])
def customer_details():
    ssn = request.args.get('ssn')
    customer = None
    if ssn:
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cdw_sapp_customer WHERE SSN = %s", (ssn,))
        customer = cursor.fetchone()
        cursor.close()
        conn.close()
    return render_template('customer.html', customer=customer)


@app.route('/transactions', methods=['GET'])
def transactions():
    zip_code = request.args.get('zip')
    month = request.args.get('month')
    year = request.args.get('year')
    transactions = []
    if zip_code and month and year:
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)
        query = (
            "SELECT cc.TRANSACTION_ID, cc.CREDIT_CARD_NO, cc.TIMEID,"
            " cc.TRANSACTION_TYPE, cc.TRANSACTION_VALUE "
            "FROM cdw_sapp_credit_card AS cc "
            "JOIN cdw_sapp_customer AS cu ON cc.CREDIT_CARD_NO = cu.CREDIT_CARD_NO "
            "WHERE cu.CUST_ZIP = %s AND MONTH(cc.TIMEID) = %s AND YEAR(cc.TIMEID) = %s "
            "ORDER BY DAY(cc.TIMEID) DESC"
        )
        cursor.execute(query, (zip_code, int(month), int(year)))
        transactions = cursor.fetchall()
        cursor.close()
        conn.close()

    df = pd.DataFrame(transactions)
    columns = df.columns.tolist() if not df.empty else []
    return render_template(
        'transactions.html',
        transactions=df.to_dict(orient='records'),
        columns=columns,
        zip_code=zip_code,
        month=month,
        year=year,
    )


@app.route('/transactions_range', methods=['GET'])
def transactions_range():
    cc_num = request.args.get('cc_num')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    transactions = []
    if cc_num and start_date and end_date:
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)
        query = (
            "SELECT TRANSACTION_ID, CREDIT_CARD_NO, TIMEID,"
            " TRANSACTION_TYPE, TRANSACTION_VALUE "
            "FROM cdw_sapp_credit_card "
            "WHERE CREDIT_CARD_NO = %s "
            "AND DATE(TIMEID) BETWEEN %s AND %s "
            "ORDER BY YEAR(TIMEID) DESC, MONTH(TIMEID) DESC, DAY(TIMEID) DESC"
        )
        cursor.execute(query, (cc_num, start_date, end_date))
        transactions = cursor.fetchall()
        cursor.close()
        conn.close()
    df = pd.DataFrame(transactions)
    return render_template('transactions_range.html', transactions=df.to_dict(orient='records'))


@app.route('/monthly_bill', methods=['GET', 'POST'])
def monthly_bill():
    transactions = None
    total = None
    month = None
    year = None
    cc_num = None
    masked_cc = None
    if request.method == 'POST':
        cc_num = request.form.get('cc_num')
        month = request.form.get('month')
        year = request.form.get('year')
        if cc_num and month and year:
            df, total_val = generate_monthly_bill(cc_num, int(month), int(year))
            if not df.empty:
                transactions = df.to_dict(orient='records')
                total = f"${total_val:.2f}"
                masked_cc = f"**** **** **** {cc_num[-4:]}"
    return render_template(
        'monthly_bill.html',
        transactions=transactions,
        total=total,
        month=month,
        year=year,
        masked_cc=masked_cc,
        cc_num=cc_num,
    )


@app.route('/modify_customer', methods=['GET', 'POST'])
def modify_customer_route():
    customer = None
    if request.method == 'POST':
        ssn = request.form.get('ssn')
        field = request.form.get('field', '').lower()
        value = request.form.get('value')
        fields = {
            'first_name': 'FIRST_NAME',
            'middle_name': 'MIDDLE_NAME',
            'last_name': 'LAST_NAME',
            'address': 'FULL_STREET_ADDRESS',
            'city': 'CUST_CITY',
            'state': 'CUST_STATE',
            'country': 'CUST_COUNTRY',
            'zip': 'CUST_ZIP',
            'phone': 'CUST_PHONE',
            'email': 'CUST_EMAIL',
        }
        column = fields.get(field)
        if ssn and column and value:
            customer = modify_customer(ssn, column, value)
    return render_template('modify_customer.html', customer=customer)


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/help')
def help_page():
    return render_template('help.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/sitemap')
def sitemap():
    return render_template('sitemap.html')


@app.route('/search')
def search():
    query = request.args.get('query')
    results = []
    if query:
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM cdw_sapp_customer WHERE FIRST_NAME LIKE %s OR LAST_NAME LIKE %s",
            (f"%{query}%", f"%{query}%")
        )
        results = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template('search.html', results=results, query=query) 


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # Here you would typically save the feedback to a database or send an email
        print(f"Feedback received from {name} ({email}): {message}")
    return render_template('feedback.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Here you would typically check the credentials against a database
        if username == 'admin' and password == 'password':
            return render_template('dashboard.html', username=username)
        else:
            error = "Invalid credentials. Please try again."
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    # This route would typically require authentication
    return render_template('dashboard.html', username='Admin')


@app.route('/logout')
def logout():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        # Here you would typically save the new user to a database
        print(f"New user registered: {username} ({email})")
        return render_template('login.html', message="Registration successful! Please log in.")
    return render_template('register.html')


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        # Here you would typically send a password reset link to the user's email
        print(f"Password reset requested for {email}")
        return render_template('login.html', message="Password reset link sent to your email.")
    return render_template('reset_password.html')


@app.route('/profile')
def profile():
    # This route would typically requiere authentication
    return render_template('profile.html', username='Admin',
                           email='admin@example.com')


@app.route('/settings')
def settings():
    # This route would typically require authentication
    return render_template('settings.html', username='Admin',
                           email='admin@example.com')


@app.route('/notifications')
def notifications():
    # This route would typically require authentication
    return render_template('notifications.html', username='Admin',
                           email='admin@example.com')


@app.route('/support')
def support():
    # This route would typically require authentication
    return render_template('support.html', username='Admin',
                           email='admin@example.com')


@app.route('/terms_of_service')
def terms_of_service():
    return render_template('terms_of_service.html')


@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')


@app.route('/cookie_policy')
def cookie_policy():
    return render_template('cookie_policy.html')


@app.route('/accessibility')
def accessibility():
    return render_template('accessibility.html')


@app.route('/legal')
def legal():
    return render_template('legal.html')


@app.route('/careers')
def careers():
    return render_template('careers.html')


@app.route('/press')
def press():
    return render_template('press.html')