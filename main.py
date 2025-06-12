import pandas as pd
import re
from tabulate import tabulate
import os
from cli_app.visualizer import ask_for_visualization
from db.utils import connect_to_db, generate_monthly_bill as db_generate_monthly_bill, modify_customer

# Determine base directory for logs and data
CAPSTONE_HOME = os.getenv(
    "CAPSTONE_HOME", os.path.dirname(os.path.abspath(__file__))
)
LOG_FOLDER = os.path.join(CAPSTONE_HOME, "logs", "visualizations")

def clear_screen(): # defines a function to clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(): # defines a function to pause the program and wait for user input
    input("\nPress Enter to return to the main menu...")


def transaction_details(): # defines a function to retrieve and display transaction details based on ZIP code and date
    clear_screen() # clear the terminal screen
    zip_code = input("Enter 5-digit ZIP code (e.g., 12345): ") # prompt user for ZIP code
    while not re.fullmatch(r"\d{5}", zip_code): # validate ZIP code format
        zip_code = input("Invalid format. Enter a 5-digit ZIP code (e.g., 12345): ") # prompt user again if invalid

    month = input("Enter month in MM format (e.g., 01 for January): ") # prompt user for month
    while not re.fullmatch(r"(0[1-9]|1[0-2])", month): # validate month format
        month = input("Invalid format. Enter month in MM format (01-12): ") # prompt user again if invalid

    year = input("Enter 4-digit year (e.g., 2018): ")  # prompt user for year
    while not re.fullmatch(r"\d{4}", year): # validate year format 
        year = input("Invalid year. Enter a 4-digit year (e.g., 2018): ") # prompt user again if invalid

    try: 
        conn = connect_to_db() # connect to the MySQL database
        cursor = conn.cursor(dictionary=True) # create a cursor to execute SQL queries
        # SQL query to retrieve transaction details based on ZIP code and date
        query = """
            SELECT cc.TRANSACTION_ID, cc.CREDIT_CARD_NO, cc.TIMEID,
                   cc.TRANSACTION_TYPE, cc.TRANSACTION_VALUE
            FROM cdw_sapp_credit_card AS cc
            JOIN cdw_sapp_customer AS cu ON cc.CREDIT_CARD_NO = cu.CREDIT_CARD_NO
            WHERE cu.CUST_ZIP = %s AND MONTH(cc.TIMEID) = %s AND YEAR(cc.TIMEID) = %s
            ORDER BY DAY(cc.TIMEID) DESC
        """
        cursor.execute(query, (zip_code, int(month), int(year))) # execute the SQL query with parameters
        transactions = cursor.fetchall() # fetch all results from the executed query

        if not transactions: # check if no transactions were found
            print(f"Please check the ZIP code {zip_code} and the date {month}/{year}.") # if no transactions found
            df = pd.DataFrame() # create an empty DataFrame
        else:
            df = pd.DataFrame(transactions) # create a DataFrame from the fetched transactions
            if 'TRANSACTION_VALUE' in df.columns: # check if TRANSACTION_VALUE column exists
                df['TRANSACTION_VALUE'] = df['TRANSACTION_VALUE'].apply(lambda x: f"${x:.2f}") # format the TRANSACTION_VALUE column to currency format
            print(f"\n--- Transactions in ZIP {zip_code} for {month}/{year} ---") # print header for the transaction details
            print(tabulate(df, headers='keys', tablefmt='psql', showindex=False)) # print the DataFrame in a pretty table format

            ask_for_visualization(df, title="Transaction Details", log_folder=LOG_FOLDER)  # ask for visualization of the DataFrame

        cursor.close() # close the cursor
        conn.close() # close the database connection
        pause() # pause the program to allow user to view results
        print("Transaction details retrieved successfully.")
        return df # return the DataFrame containing transaction details

    except Exception as e: # handle any exceptions that occur during database operations
        print("Error:", e) # print the error message
        pause() # pause the program to allow user to view error
        return pd.DataFrame() # return an empty DataFrame

def customer_menu(): # defines a function to display the customer menu and handle user choices
    clear_screen() # clear the terminal screen
    print("=== Customer Menu ===") # print header for the customer menu
    # Display options for customer management
    print("""
1. View Customer Details
2. Modify Customer Details
3. Generate Monthly Bill
4. Display Transactions in Date Range
""")
    choice = input("Choose an option: ") # prompt user to choose an option from the customer menu

    if choice == '1': # this block handles viewing customer details 
        view_customer_details()
    elif choice == '2':
        modify_customer_details()
    elif choice == '3':
        generate_monthly_bill()
    elif choice == '4':
        customer_transactions_date_range()
    else:
        print("Invalid choice. Returning to main menu.")
        pause()

def view_customer_details(): # defines a function to view customer details based on SSN
    clear_screen() # clear the terminal screen
    ssn = input("Enter Customer SSN: ") # prompt user for SSN
    try: 
        conn = connect_to_db() # connect to the MySQL database
        cursor = conn.cursor(dictionary=True) # create a cursor to execute SQL queries
        query = "SELECT * FROM cdw_sapp_customer WHERE SSN = %s" # SQL query to retrieve customer details based on SSN
        cursor.execute(query, (ssn,)) # execute the SQL query with the provided SSN
        customer = cursor.fetchone() # fetch the first result from the executed query
        if customer: # check if a customer was found
            df = pd.DataFrame([customer]) # create a DataFrame from the fetched customer details
            print("\n--- Customer Details ---") # print header for the customer details
            print(tabulate(df, headers="keys", tablefmt="psql", showindex=False)) # print the DataFrame in a pretty table format

            ask_for_visualization(df, title="Customer Details", log_folder=LOG_FOLDER)  # ask for visualization of the DataFrame
        else: 
            print("Customer not found.")
            df = pd.DataFrame()
        cursor.close()
        conn.close()
        pause()
        return df
    except Exception as e:  # handle any exceptions that occur during database operations
        print("Error:", e) # print the error message
        pause() 
        return pd.DataFrame()

def modify_customer_details(): # defines a function to modify customer details based on SSN
    clear_screen()
    ssn = input("Enter SSN of the customer to update: ") # prompt user for SSN
    field = input("Enter the field to update (e.g., email, phone): ").strip().lower() # prompt user for the field to update

    allowed_fields = {
        'first_name': 'FIRST_NAME',
        'middle_name': 'MIDDLE_NAME',
        'last_name': 'LAST_NAME',
        'address': 'FULL_STREET_ADDRESS',
        'city': 'CUST_CITY',
        'state': 'CUST_STATE',
        'country': 'CUST_COUNTRY',
        'zip': 'CUST_ZIP',
        'phone': 'CUST_PHONE',
        'email': 'CUST_EMAIL'
    }

    if field not in allowed_fields:
        print("Invalid field. Allowed fields are: " + ", ".join(allowed_fields.keys()))
        pause()
        return

    value = input(f"Enter new value for {field}: ").strip() # prompt user for the new value of the field

    try:
        column = allowed_fields[field]
        updated_customer = modify_customer(ssn, column, value)
        print("Customer details updated successfully.")
        if updated_customer:
            df = pd.DataFrame([updated_customer])
            print("\n--- Updated Customer Details ---")
            print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
            ask_for_visualization(df, title="Updated Customer Details", log_folder=LOG_FOLDER)
        pause()
    except Exception as e:
        print("Error:", e)
        pause()

def generate_monthly_bill():
    clear_screen()
    cc_num = input("Enter Credit Card Number: ").strip()
    month = input("Enter Month (MM): ").strip()
    year = input("Enter Year (YYYY): ").strip()

    try:
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)

        # Detailed transactions for the bill
        query = """
            SELECT TIMEID AS `Date`, TRANSACTION_TYPE AS `Transaction`, TRANSACTION_VALUE AS `Amount`
            FROM cdw_sapp_credit_card
            WHERE CREDIT_CARD_NO = %s AND MONTH(TIMEID) = %s AND YEAR(TIMEID) = %s
            ORDER BY TIMEID;
        """
        cursor.execute(query, (cc_num, int(month), int(year)))
        transactions = cursor.fetchall()

        if transactions:
            df = pd.DataFrame(transactions)

            # Convert YYYYMMDD to MM/DD/YYYY
            df['Date'] = pd.to_datetime(df['Date'].astype(str), format='%Y%m%d').dt.strftime('%m/%d/%Y')

            # Format amount and calculate total
            total = df['Amount'].sum()
            df['Amount'] = df['Amount'].apply(lambda x: f"${x:.2f}")

            # Display the bill layout
            print("\n" + "=" * 60)
            print(" " * 20 + "CDW SAPP BANK STATEMENT")
            print(" " * 15 + f"Billing Period: {month}/{year}")
            print("=" * 60)
            print(f"Credit Card #: **** **** **** {cc_num[-4:]}")
            print("-" * 60)

            print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
            print("-" * 60)
            print(f"{'Total Charges':>50}: ${total:.2f}")
            print("=" * 60)

            ask_for_visualization(pd.DataFrame(transactions), title="Monthly Bill Breakdown", log_folder=LOG_FOLDER)

            cursor.close()
            conn.close()
            pause()
            return df
        else:
            print("No transactions found.")
            pause()
            return pd.DataFrame()

    except Exception as e:
        print("Error:", e)
        pause()
        return pd.DataFrame()


def customer_transactions_date_range(): # defines a function to retrieve customer transactions within a specified date range
    clear_screen() 
    cc_num = input("Enter Credit Card Number: ").strip() 
    print("\nEnter start date:") # prompt user for start date
    start_month = input("Month (MM): ") # prompt user for start month
    while not re.fullmatch(r"(0[1-9]|1[0-2])", start_month): # validate month format
        start_month = input("Invalid. Enter month (MM): ") # prompt user again if invalid
    start_day = input("Day (DD): ") # prompt user for start day
    while not re.fullmatch(r"(0[1-9]|[12][0-9]|3[01])", start_day): # validate day format
        start_day = input("Invalid. Enter day (DD): ") # prompt user again if invalid
    start_year = input("Year (YYYY): ") # prompt user for start year
    while not re.fullmatch(r"\d{4}", start_year): # validate year format
        start_year = input("Invalid. Enter year (YYYY): ") # prompt user again if invalid
    start_date = f"{start_year}-{start_month}-{start_day}" # format start date as YYYY-MM-DD

    print("\nEnter end date:") # prompt user for end date
    end_month = input("Month (MM): ") # prompt user for end month
    while not re.fullmatch(r"(0[1-9]|1[0-2])", end_month): # validate month format
        end_month = input("Invalid. Enter month (MM): ") # prompt user again if invalid
    end_day = input("Day (DD): ") # prompt user for end day
    while not re.fullmatch(r"(0[1-9]|[12][0-9]|3[01])", end_day): # validate day format
        end_day = input("Invalid. Enter day (DD): ") # prompt user again if invalid
    end_year = input("Year (YYYY): ") # prompt user for end year
    while not re.fullmatch(r"\d{4}", end_year): # validate year format
        end_year = input("Invalid. Enter year (YYYY): ") # prompt user again if invalid
    end_date = f"{end_year}-{end_month}-{end_day}" # format end date as YYYY-MM-DD

    try:
        conn = connect_to_db() 
        cursor = conn.cursor(dictionary=True) 
        query = """
            SELECT TRANSACTION_ID, CREDIT_CARD_NO, TIMEID,
                   TRANSACTION_TYPE, TRANSACTION_VALUE
            FROM cdw_sapp_credit_card
            WHERE CREDIT_CARD_NO = %s 
              AND DATE(TIMEID) BETWEEN %s AND %s
            ORDER BY YEAR(TIMEID) DESC, MONTH(TIMEID) DESC, DAY(TIMEID) DESC;
        """
        cursor.execute(query, (cc_num, start_date, end_date))
        transactions = cursor.fetchall()

        if transactions:
            df = pd.DataFrame(transactions) # create a DataFrame from the fetched transactions
            if "TRANSACTION_VALUE" in df.columns: # check if TRANSACTION_VALUE column exists
                df["TRANSACTION_VALUE"] = df["TRANSACTION_VALUE"].apply(lambda x: f"${x:.2f}") # format the TRANSACTION_VALUE column to currency format
            print(f"\n--- Transactions for Credit Card {cc_num} from {start_date} to {end_date} ---") # print header for the transaction details
            print(tabulate(df, headers="keys", tablefmt="psql", showindex=False)) # print the DataFrame in a pretty table format

            ask_for_visualization(df, title="Customer Transactions by Date Range", log_folder=LOG_FOLDER)
        else:
            print("No transactions found for that period.")
            df = pd.DataFrame()

        cursor.close()
        conn.close()
        pause()
        return df
    except Exception as e:
        print("Error:", e)
        pause()
        return pd.DataFrame()

def main_menu(): # defines the main menu function to display options and handle user choices
    while True: # loop to keep displaying the main menu until user chooses to exit
        clear_screen() # clear the terminal screen
        print(""" 
=== Bank Console App ===
1. Transaction Details
2. Customer Details
3. Exit
""")
        option = input("Select an option: ") # prompt user to select an option from the main menu
        if option == '1':
            transaction_details()
        elif option == '2':
            customer_menu()
        elif option == '3':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid option. Try again.")
            pause()

if __name__ == "__main__": # check if the script is being run directly
    main_menu() # call the main menu function to start the application
# This code is a console application that allows users to interact with a MySQL database
