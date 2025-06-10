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
