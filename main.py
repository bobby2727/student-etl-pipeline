import logging
import os
import schedule
import time
import sqlite3
import traceback

from extract import extract
from transform import transform
from load import load
import config


os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_analysis():
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT grade, COUNT(*) 
        FROM students 
        GROUP BY grade
    """)
    print("Grade Count:", cursor.fetchall())

    cursor.execute("""
        SELECT id, marks 
        FROM students 
        ORDER BY marks DESC 
        LIMIT 5
    """)
    print("Top Students:", cursor.fetchall())

    cursor.execute("""
        SELECT AVG(marks) FROM students
    """)
    print("Average Marks:", cursor.fetchone())

    cursor.close()
    conn.close()



def main():
    logging.info("Pipeline started")

    try:
        data = extract()
        clean = transform(data)
        load(clean)
        run_analysis()

        logging.info("Pipeline completed successfully")

    except Exception:
        logging.error(traceback.format_exc())
        print("Full Error:\n", traceback.format_exc())



def job():
    logging.info("Scheduled job started")
    main()


if __name__ == "__main__":
    main()

    schedule.every(1).minutes.do(job)

    logging.info("Scheduler started... Running every 1 minute")

    try:
        while True:
            schedule.run_pending()   
            time.sleep(1)
    except KeyboardInterrupt:
        print("Pipeline stopped by user")