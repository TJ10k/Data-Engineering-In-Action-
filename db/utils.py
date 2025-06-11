import os
import mysql.connector


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
    """Return total transaction value for the specified credit card and month."""
    conn = connect_to_db()
    cursor = conn.cursor()
    query = (
        "SELECT SUM(TRANSACTION_VALUE) AS bill_total "
        "FROM cdw_sapp_credit_card "
        "WHERE CREDIT_CARD_NO = %s AND MONTH(TIMEID) = %s AND YEAR(TIMEID) = %s"
    )
    cursor.execute(query, (cc_num, month, year))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None


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
