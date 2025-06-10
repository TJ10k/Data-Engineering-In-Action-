# Data-Engineering-In-Action-
Transforming raw financial data into actionable insights using Python, SQL, PySpark, and visualization tools.

To run the ETL and CLI please follow these instructions

#1 Download all files from the data folder if you would rather run the file to save the api its called api_save.py
#2 Head to db folder and run the schema
#3 Head to the etl folder and run both python scripts one at a time WARNING... change all file paths to your specific file paths
#4 make a folder called logs and put that folder path in the visualizer function to log your visualization
#5 Verify the data has been loaded and you can now run the cli and create visualizations and modify data in the database

## Running the Flask Web App

The `web/` directory contains a small Flask application that exposes the same
operations as the CLI. Make sure Python and `pip` are installed and then
install the required packages:

```bash
pip install flask mysql-connector-python pandas
```

### Local execution

1. Export the database connection details if they differ from the defaults:

```bash
export DB_HOST=<your_host>
export DB_PORT=<port>
export DB_USER=<user>
export DB_PASSWORD=<password>
export DB_NAME=creditcard_capstone
```

2. Start the application:

```bash
python web/app.py
```

The app will be available at `http://localhost:5000`.

### AWS deployment (EC2 example)

1. Provision an EC2 instance with Python installed and clone this repository.
2. Install the dependencies as shown above.
3. Set the environment variables for your RDS or database instance.
4. Run `python web/app.py` and configure security groups to allow inbound
   traffic on port 5000 (or use a reverse proxy such as Nginx for production).

