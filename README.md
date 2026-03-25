#  Data Engineering ETL Pipeline

##  Overview
This project is a production-style ETL pipeline that extracts data from an API, transforms it, and loads it into a SQLite database.

##  Architecture
API → Extract → Transform → Load → SQLite → Analysis

##  Features
- Incremental loading
- Deduplication using ROW_NUMBER()
- Logging system
- Scheduled execution

##  Tech Stack
- Python
- Pandas
- SQLite
- SQL

##  How to Run
pip install -r requirements.txt  
python main.py
