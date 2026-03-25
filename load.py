import sqlite3
import logging
import os
import config

def load(df):
    logging.info("Loading data (Incremental + Deduplication)")

    os.makedirs("data", exist_ok=True)

    # Save files
    df.to_csv(config.CSV_PATH, index=False)
    df.to_json("data/data.json", orient="records", date_format="iso")

    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()

    # Create main table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER,
            marks INTEGER,
            grade TEXT,
            processed_time TIMESTAMP
        )
    """)

    # Drop temp table
    cursor.execute("DROP TABLE IF EXISTS temp_students")

    # Create temp table
    cursor.execute("""
        CREATE TABLE temp_students (
            id INTEGER,
            marks INTEGER,
            grade TEXT,
            processed_time TIMESTAMP
        )
    """)

    # Ensure correct columns
    df = df[["id", "marks", "grade", "processed_time"]]

    # Debug 
    print("Columns being inserted:", df.columns)

    #  Insert into temp table (FIXED INDENTATION)
    df.to_sql("temp_students", conn, if_exists="append", index=False)

    # Incremental + Deduplication
    cursor.execute("""
        INSERT INTO students (id, marks, grade, processed_time)
        SELECT id, marks, grade, processed_time
        FROM (
            SELECT *,
                   ROW_NUMBER() OVER (
                       PARTITION BY id 
                       ORDER BY processed_time DESC
                   ) as rn
            FROM temp_students
        ) t
        WHERE rn = 1
        AND NOT EXISTS (
            SELECT 1 FROM students s
            WHERE s.id = t.id 
              AND s.processed_time = t.processed_time
        )
    """)

    # Index
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_students_id 
        ON students(id)
    """)

    conn.commit()
    conn.close()

    logging.info("Data loaded successfully")