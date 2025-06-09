import requests
import json

# Replace this with your actual API URL
url = "https://raw.githubusercontent.com/platformps/LoanDataset/main/loan_data.json"

# Send GET request to API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Save the JSON data to a local file
    with open("data/loan_data.json", "w") as f:
        json.dump(data, f, indent=4)
    
    print("Data saved successfully.")
else:
    print("Failed to fetch data:", response.status_code)
