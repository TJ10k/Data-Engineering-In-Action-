# Data Engineering in Action

This repository contains a command line interface for querying a MySQL database, ETL scripts to load sample data, and utilities for creating visualizations.

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
