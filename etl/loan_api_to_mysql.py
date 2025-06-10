import pandas as pd
import requests
import mysql.connector as dbconnect
from mysql.connector import errorcode
import os

# Optional base directory for future data storage
CAPSTONE_HOME = os.getenv(
    "CAPSTONE_HOME", os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "creditcard_capstone")

def fetch_posts(): # Fetch loan application data
    url = "https://raw.githubusercontent.com/platformps/LoanDataset/main/loan_data.json" # URL to fetch data from
    response = requests.get(url) # Make a GET request to the URL
    if response.status_code == 200: # Check if the request was successful
        print("Data fetched successfully.") # Print success message
        return response.json() # Return the JSON data
    else:
        print(f"Failed to fetch data. Status Code: {response.status_code}") # Print error message if the request failed
        return None # Return None if the request failed
    
def load_to_mysql(data): # Load data into MySQL database
    if data is None: # Check if data is None
        print("No data to load.") # If data is None, print message and return
        return 

    df = pd.DataFrame(data) # Convert JSON data to DataFrame
    print(f"DataFrame created with {len(df)} rows.") # Print number of rows in DataFrame

    try:
        conn = dbconnect.connect(  # Connect to MySQL database
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
        cursor = conn.cursor() # Create a cursor object to execute SQL queries

        insert_query = """  
INSERT INTO cdw_sapp_loan_application 
(Application_ID, Application_Status, Credit_History, Dependents, Education, Gender, Income, Married, Property_Area, Self_Employed)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = [(
            row['Application_ID'],
            row['Application_Status'],
            row['Credit_History'],
            row['Dependents'],
            row['Education'],
            row['Gender'],
            row['Income'],
            row['Married'],
            row['Property_Area'],
            row['Self_Employed']
        ) for index, row in df.iterrows()]

        cursor.executemany(insert_query, values)
        conn.commit()
        print(f"Inserted {len(values)} rows.")


    except dbconnect.Error as err: # Handle MySQL errors
        print(f"Error: {err}") 
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected(): # Check if connection is open before closing
            conn.close()
        print("MySQL connection closed.")

if __name__ == "__main__": # Main function to execute the script
    data = fetch_posts() # Fetch loan application data
    load_to_mysql(data) # Load data into MySQL database
