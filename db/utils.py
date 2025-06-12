import os
import mysql.connector
import pandas as pd


def connect_to_db():
    """Connect to the MySQL database using environment variables."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "password"),
        database=os.getenv("DB_NAME", "creditcard_capstone"),
    )


def generate_monthly_bill(cc_num: str, month: int, year: int):
    """Return a dataframe of transactions and the monthly total."""
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    query = (
        "SELECT TIMEID AS Date, TRANSACTION_TYPE AS Transaction, TRANSACTION_VALUE AS Amount "
        "FROM cdw_sapp_credit_card "
        "WHERE CREDIT_CARD_NO = %s AND MONTH(TIMEID) = %s AND YEAR(TIMEID) = %s "
        "ORDER BY TIMEID"
    )
    cursor.execute(query, (cc_num, month, year))
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()

    if not transactions:
        return pd.DataFrame(), 0.0

    df = pd.DataFrame(transactions)
    df['Date'] = pd.to_datetime(df['Date'].astype(str), format='%Y%m%d').dt.strftime('%m/%d/%Y')
    total = df['Amount'].sum()
    df['Amount'] = df['Amount'].apply(lambda x: f"${x:.2f}")
    return df, total


def modify_customer(ssn: str, field: str, value: str):
    """Update a customer record and return the updated row as a dictionary."""
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    query = f"UPDATE cdw_sapp_customer SET {field} = %s WHERE SSN = %s"
    cursor.execute(query, (value, ssn))
    conn.commit()
    cursor.execute("SELECT * FROM cdw_sapp_customer WHERE SSN = %s", (ssn,))
    updated = cursor.fetchone()
    cursor.close()
    conn.close()
    return updated
