# Data Engineering in Action

This repository contains a command line interface for querying a MySQL database, ETL scripts to load sample data, and utilities for creating visualizations.


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

=======
#4 Set the environment variable `CAPSTONE_DATA_DIR` to the location of the JSON data files
#   (or pass `--data-dir` when running `visualization_creation.py`).
#5 Set `VIS_LOG_FOLDER` to the folder where generated charts should be stored.
#6 Verify the data has been loaded and you can now run the cli and create visualizations and modify data in the database
=======
## Prerequisites

Install the required Python packages:

```bash
pip install mysql-connector-python pandas matplotlib pyspark
```

## Configuration

Before running the scripts, set the following environment variables so the tools can connect to MySQL:

- `DB_HOST` – database host (e.g., `localhost`)
- `DB_PORT` – database port (e.g., `3306`)
- `DB_USER` – MySQL username
- `DB_PASSWORD` – MySQL password
- `DB_NAME` – target database name (default is `creditcard_capstone`)

Example configuration on Linux/macOS:

```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=secret
export DB_NAME=creditcard_capstone
```

## Loading Data

The `etl` directory contains scripts to populate the database:

```bash
python etl/load_json_to_mysql.py   # load local JSON files
python etl/loan_api_to_mysql.py    # load loan application data from API
```

## Running the CLI

After the data is loaded, launch the console application with:

```bash
python main.py
```

## Example Workflow

Below is a typical sequence to prepare the environment, load the data and start the CLI:

```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=secret
export DB_NAME=creditcard_capstone
python etl/load_json_to_mysql.py
python etl/loan_api_to_mysql.py
python main.py
```
=======
# Data Engineering In Action

This project contains utilities for loading and analyzing credit card and loan data.

## Base Directory

Scripts look for data files and store generated visualizations relative to a base directory. By default this is the repository location, but it can be overridden with the `CAPSTONE_HOME` environment variable.

Example:

```bash
export CAPSTONE_HOME=/opt/capstone
python main.py
```

Data files should be stored in `$CAPSTONE_HOME/data` and visualizations will be written to `$CAPSTONE_HOME/logs/visualizations`.
