# Data-Engineering-In-Action-
Transforming raw financial data into actionable insights using Python, SQL, PySpark, and visualization tools.

To run the ETL and CLI please follow these instructions

#1 Download all files from the data folder if you would rather run the file to save the api its called api_save.py
#2 Head to db folder and run the schema
#3 Head to the etl folder and run both python scripts one at a time WARNING... change all file paths to your specific file paths
#4 make a folder called logs and put that folder path in the visualizer function to log your visualization
#5 Verify the data has been loaded and you can now run the cli and create visualizations and modify data in the database

## Installing Dependencies

1. Ensure Python 3 is available on your system.
2. Install the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Running in AWS

You can deploy the application on an Amazon EC2 instance or using Elastic Beanstalk.

### EC2

1. Launch an EC2 instance and connect to it via SSH.
2. Clone this repository to the instance.
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables for database connectivity and any other secrets. For example:
   ```bash
   export DB_HOST=<your-database-host>
   export DB_USER=<your-database-user>
   export DB_PASSWORD=<your-database-password>
   export DB_NAME=creditcard_capstone
   ```
   These variables keep credentials outside of the code base and comply with sandbox restrictions.
5. Run the application:
   ```bash
   python main.py
   ```

### Elastic Beanstalk

1. Create a new Elastic Beanstalk Python application.
2. Include this repository's contents in a deployment bundle along with `requirements.txt`.
3. In the Elastic Beanstalk console, configure environment variables (e.g., `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`).
4. Deploy the bundle. Beanstalk will install the packages from `requirements.txt` and start the application.

