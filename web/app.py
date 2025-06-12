from flask import Flask, render_template, request

from db.utils import connect_to_db, generate_monthly_bill, modify_customer
import pandas as pd

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
    return render_template('transactions.html', transactions=df.to_dict(orient='records'))


@app.route('/monthly_bill', methods=['GET', 'POST'])
def monthly_bill():
    transactions = None
    total = None
    if request.method == 'POST':
        cc_num = request.form.get('cc_num')
        month = request.form.get('month')
        year = request.form.get('year')
        if cc_num and month and year:
            df, total_val = generate_monthly_bill(cc_num, int(month), int(year))
            if not df.empty:
                transactions = df.to_dict(orient='records')
                total = f"${total_val:.2f}"
    return render_template('monthly_bill.html', transactions=transactions, total=total)


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
