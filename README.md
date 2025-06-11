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

To display a custom logo, place an image named `logo.png` inside
`web/static/`. It will appear in the site header on every page. You can modify
`web/static/style.css` to adjust the layout and colors.

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
These values are used by `main.py` and the ETL scripts when establishing a
database connection.

## Downloading Sample Data and Visualizations
To keep the repository small, the `data/` and `screenshots/` folders are not tracked in git. Use the helper script below to download and extract them:

```bash
bash scripts/download_assets.sh
```

Set the `ASSETS_URL` environment variable to point to an archive containing both directories if you host them elsewhere. Alternatively, run `python data/api_save.py` to fetch the loan dataset directly from its source.

