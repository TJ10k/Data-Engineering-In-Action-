import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

# Set Seaborn style

sns.set(style="whitegrid")

parser = argparse.ArgumentParser(
    description="Create visualizations from the Capstone data files"
)
parser.add_argument(
    "--data-dir",
    help="Directory containing JSON data files",
)
args = parser.parse_args()

DATA_DIR = args.data_dir or os.environ.get("CAPSTONE_DATA_DIR", "data")

# === LOAD FILES ===
try:
    loan_df = pd.read_json(os.path.join(DATA_DIR, "cdw_sapp_loan_data.json"))
    credit_df = pd.read_json(os.path.join(DATA_DIR, "cdw_sapp_credit.json"))
    customer_df = pd.read_json(os.path.join(DATA_DIR, "cdw_sapp_customer.json"))
    branch_df = pd.read_json(os.path.join(DATA_DIR, "cdw_sapp_branch.json"))
    print("All files loaded successfully.")
except Exception as e:
    print(f"Error loading files: {e}")
    exit()

# === SELF-EMPLOYED LOAN APPROVAL PIE CHART ===
try:
    self_emp = loan_df[loan_df["Self_Employed"].str.upper() == "YES"]
    approved = self_emp[self_emp["Application_Status"].str.upper() == "Y"].shape[0]
    rejected = self_emp[self_emp["Application_Status"].str.upper() == "N"].shape[0]

    labels = ['Approved', 'Rejected']
    sizes = [approved, rejected]
    colors = ['#008ebc', '#e90f73']

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
    plt.title('Loan Approval Rate for Self-Employed Applicants')
    plt.tight_layout()
    plt.savefig("self_employed_loan_approval.png")
    plt.show()
except Exception as e:
    print(f"Error creating self-employed loan pie chart: {e}")

# Trend: Self-employed applicants have a lower approval rate compared to others ✔ Action: Financial institutions can tailor loan products or support services for self-employed individuals

# === FIXED: TOP 10 STATES BY CUSTOMER COUNT ===

# Load Customer Data
customer_df = pd.read_json(os.path.join(DATA_DIR, "cdw_sapp_customer.json"))

# Count Customers by State & Select Top 10
state_counts = customer_df["CUST_STATE"].value_counts().reset_index()
state_counts.columns = ["State", "Customer_Count"]
top_states = state_counts.head(10)  # Select top 10 states

# Create Heatmap Dataframe
heatmap_data = top_states.set_index("State").T  # Transpose for heatmap formatting

# Plot Heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", linewidths=0.5, fmt="d", cbar_kws={"label": "Customer Count"})

# Formatting
plt.title("Top 10 States by Customer Count", fontsize=16)
plt.xlabel("State", fontsize=12)
plt.ylabel("Customer Count", fontsize=12)
plt.xticks(rotation=45)

# Save as PNG
plt.savefig("top_10_states_heatmap.png", dpi=300)
plt.show()


# Trend: Identifies states with the highest customer base  Action: Helps financial institutions target marketing efforts in high-density areas

# === Highest Count Transaction Types ===

# Load transaction data
credit_df = pd.read_json(os.path.join(DATA_DIR, "cdw_sapp_credit.json"))

# Group by Transaction Type & Count
transaction_counts = credit_df["TRANSACTION_TYPE"].value_counts()

# Plot Bar Chart
plt.figure(figsize=(10, 6))
sns.barplot(x=transaction_counts.index, y=transaction_counts.values, palette="coolwarm")

# Formatting
plt.title("Most Frequent Transaction Types")
plt.xlabel("Transaction Type")
plt.ylabel("Total Count")
plt.xticks(rotation=45)
plt.savefig("most_frequent_transaction_types.png")
plt.show()

# ✔ Trend: Identifies the most frequently used transaction types ✔ Action: Helps financial institutions optimize service offerings around high-frequency transactions

# === Top Spending Customers ===

merged_df = credit_df.merge(customer_df, on="CREDIT_CARD_NO")

# Create a Full Name Column
merged_df["Customer_Name"] = merged_df["FIRST_NAME"] + " " + merged_df["LAST_NAME"]

# Group by Full Name & Sum Spending
top_spenders = merged_df.groupby("Customer_Name")["TRANSACTION_VALUE"].sum().nlargest(10)

# Pie Chart
plt.figure(figsize=(8, 8))
plt.pie(top_spenders, labels=top_spenders.index, autopct="%1.1f%%", colors=sns.color_palette("coolwarm", len(top_spenders)))
plt.title("Top Spending Customers")
plt.savefig("top_spenders_pie.png")
plt.show()

# OR Column Chart
plt.figure(figsize=(10, 6))
sns.barplot(x=top_spenders.index, y=top_spenders.values, palette="coolwarm")

# Formatting
plt.title("Top Spending Customers")
plt.xlabel("Customer Name")
plt.ylabel("Total Spending")
plt.xticks(rotation=45)
plt.savefig("top_spenders_column.png")
plt.show()

# Trend: Identifies high-value customers for personalized offers or VIP services ✔ Action: Financial institutions can offer tailored rewards & incentives to reward top spenders


# === Monthly Spending Trends ===

# Create a datetime column from YEAR, MONTH, DAY
credit_df["TIMEID"] = pd.to_datetime(credit_df[["YEAR", "MONTH", "DAY"]])

# Aggregate transaction values by month
monthly_spending = credit_df.groupby(credit_df["TIMEID"].dt.to_period("M"))["TRANSACTION_VALUE"].sum()

# Plot Line Chart
plt.figure(figsize=(12, 6))
monthly_spending.plot(kind="line", marker="o", color="violet", linestyle='--')

# Formatting
plt.title("Monthly Spending Trends")
plt.xlabel("Month")
plt.ylabel("Total Spending ($)")
plt.xticks(rotation=45)
plt.grid(True)
plt.savefig("monthly_spending_trends.png")
plt.show()

# Trend: Shows how spending patterns change over time ✔ Action: Helps financial institutions identify seasonal trends & adjust marketing strategies accordingly

