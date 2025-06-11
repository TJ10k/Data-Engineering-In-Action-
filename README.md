# Data Engineering in Action

This project provides a command line interface, ETL scripts and a simple Flask application for working with a MySQL database that stores credit card and loan data.

## Prerequisites

* Python 3
* Install dependencies with:
  ```bash
  pip install -r requirements.txt
  ```

## Environment Variables

Set the following variables so the ETL scripts, CLI and web app can locate files and connect to the database:

* `CAPSTONE_HOME` – optional base directory where data files and logs are stored. Defaults to the repository directory.
* `DB_HOST` – database host (default `localhost`)
* `DB_PORT` – database port (default `3306`)
* `DB_USER` – MySQL user
* `DB_PASSWORD` – MySQL password
* `DB_NAME` – database name (default `creditcard_capstone`)

Example setup:
```bash
export CAPSTONE_HOME=/opt/capstone
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=secret
export DB_NAME=creditcard_capstone
```

Data files should be placed in `$CAPSTONE_HOME/data` and visualizations will be written to `$CAPSTONE_HOME/logs/visualizations`.

## Loading Data

Run the ETL scripts from the repository root to populate the database:
```bash
python etl/load_json_to_mysql.py   # loads customer and transaction JSON files
python etl/loan_api_to_mysql.py    # loads loan application data from an API
```

## Running the CLI

After loading the data, start the interactive console application with:
```bash
python main.py
```

## Running the Web App

The Flask app exposes similar functionality via a browser. Launch it with:
```bash
python -m web.app
```
The site will be available at `http://localhost:5000`.

## Example Workflow

Typical steps for a fresh environment:
```bash
export CAPSTONE_HOME=/opt/capstone
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=secret
export DB_NAME=creditcard_capstone
python etl/load_json_to_mysql.py
python etl/loan_api_to_mysql.py
python main.py    # or `python -m web.app` to launch the web interface
```
