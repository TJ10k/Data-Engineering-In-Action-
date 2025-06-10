from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat_ws, lpad, udf, initcap, lower
from pyspark.sql.types import StringType
import re
import os

# Base directory for input data
CAPSTONE_HOME = os.getenv(
    "CAPSTONE_HOME", os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
DATA_DIR = os.path.join(CAPSTONE_HOME, "data")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "creditcard_capstone")

# Start Spark session
spark = SparkSession.builder \
    .appName("ETL to MySQL") \
    .config("spark.jars.packages", "mysql:mysql-connector-java:8.0.33") \
    .getOrCreate()

# UDF to format phone numbers
def format_phone(phone):
    digits = ''.join(filter(str.isdigit, str(phone)))
    if len(digits) == 10:
        return f"({digits[0:3]}){digits[3:6]}-{digits[6:]}" # adds () to the first 3 digits, and then a dash in between the middle 3 and the last 4
    elif len(digits) == 7:
        return f"(XXX){digits[0:3]}-{digits[3:]}" # adds XXX to the front if the phone number is only 7 digits
    else:
        return phone  # Return as-is if it doesn't match 7 or 10 digits

format_phone_udf = udf(format_phone, StringType()) # Register the UDF

# CUSTOMER ETL
customer_df = spark.read.option("multiLine", True).json(
    os.path.join(DATA_DIR, "cdw_sapp_customer.json")
)  # Load the JSON file
# Transform the customer data
transformed_customer = customer_df \
    .withColumn("FIRST_NAME", initcap(col("FIRST_NAME"))) \
    .withColumn("MIDDLE_NAME", lower(col("MIDDLE_NAME"))) \
    .withColumn("LAST_NAME", initcap(col("LAST_NAME"))) \
    .withColumn("FULL_STREET_ADDRESS", concat_ws(", ", col("STREET_NAME"), col("APT_NO"))) \
    .withColumn("CUST_PHONE", format_phone_udf(col("CUST_PHONE"))) \
    .select(
        "SSN", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "CREDIT_CARD_NO",
        "FULL_STREET_ADDRESS", "CUST_CITY", "CUST_STATE", "CUST_COUNTRY",
        "CUST_ZIP", "CUST_PHONE", "CUST_EMAIL", "LAST_UPDATED"
    )

# BRANCH ETL
branch_df = spark.read.option("multiLine", True).json(
    os.path.join(DATA_DIR, "cdw_sapp_branch.json")
)
# Transform the branch data
transformed_branch = branch_df \
    .withColumn("BRANCH_PHONE", format_phone_udf(col("BRANCH_PHONE"))) \
    .na.fill({"BRANCH_ZIP": "99999"}) \
    .select(
        "BRANCH_CODE", "BRANCH_NAME", "BRANCH_STREET", "BRANCH_CITY",
        "BRANCH_STATE", "BRANCH_ZIP", "BRANCH_PHONE", "LAST_UPDATED"
    )

# CREDIT CARD ETL
credit_df = spark.read.option("multiLine", True).json(
    os.path.join(DATA_DIR, "cdw_sapp_credit.json")
)
# Transform the credit card data
transformed_credit = credit_df \
    .withColumn("TIMEID",
        concat_ws("", 
            lpad(col("YEAR").cast("string"), 4, "0"),
            lpad(col("MONTH").cast("string"), 2, "0"),
            lpad(col("DAY").cast("string"), 2, "0"))
    ) \
    .select(
        "CREDIT_CARD_NO", "TIMEID", "CUST_SSN", "BRANCH_CODE",
        "TRANSACTION_TYPE", "TRANSACTION_VALUE", "TRANSACTION_ID"
    )

# WRITE TO MYSQL
def write_to_mysql(df, table_name):  # Function to write DataFrame to MySQL
    jdbc_url = f"jdbc:mysql://{DB_HOST}:{DB_PORT}/{DB_NAME}"
    df.write \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .option("dbtable", table_name) \
        .option("user", DB_USER) \
        .option("password", DB_PASSWORD) \
        .mode("append") \
        .save()

# Load all transformed tables
write_to_mysql(transformed_customer, "CDW_SAPP_CUSTOMER")
write_to_mysql(transformed_branch, "CDW_SAPP_BRANCH")
write_to_mysql(transformed_credit, "CDW_SAPP_CREDIT_CARD")
