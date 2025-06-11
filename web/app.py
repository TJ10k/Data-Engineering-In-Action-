from flask import Flask, render_template, request

from db.utils import connect_to_db
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


if __name__ == '__main__':
    app.run(debug=True)
