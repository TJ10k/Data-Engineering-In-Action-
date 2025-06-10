# Data-Engineering-In-Action-
Transforming raw financial data into actionable insights using Python, SQL, PySpark, and visualization tools.

To run the ETL and CLI please follow these instructions

#1 Download all files from the data folder if you would rather run the file to save the api its called api_save.py
#2 Head to db folder and run the schema
#3 Head to the etl folder and run both python scripts one at a time WARNING... change all file paths to your specific file paths
<<<<<<< HEAD
#4 Set the environment variable `CAPSTONE_DATA_DIR` to the location of the JSON data files
#   (or pass `--data-dir` when running `visualization_creation.py`).
#5 Set `VIS_LOG_FOLDER` to the folder where generated charts should be stored.
#6 Verify the data has been loaded and you can now run the cli and create visualizations and modify data in the database
=======
#4 make a folder called logs and put that folder path in the visualizer function to log your visualization
#5 Verify the data has been loaded and you can now run the cli and create visualizations and modify data in the database

## Environment Variables

The application reads MySQL connection details from the environment. Define the
following variables either in your shell, in AWS environment settings or in a
local `.env` file before running the ETL scripts or the CLI:

- `DB_HOST` – MySQL host (e.g. `localhost`)
- `DB_PORT` – MySQL port (e.g. `3306`)
- `DB_USER` – MySQL user
- `DB_PASSWORD` – MySQL password
- `DB_NAME` – Database name

These values are used by `main.py` and the ETL scripts when establishing a
database connection.
>>>>>>> master
