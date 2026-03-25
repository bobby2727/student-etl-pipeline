import logging
from datetime import datetime

def transform(df):
    logging.info("Transforming data")

    df = df.dropna()
    df = df.drop_duplicates()

    df["marks"] = df["id"] * 10
    df = df[df["marks"] > 70]

    df["grade"] = df["marks"].apply(lambda x: "A" if x > 85 else "B")
    df["processed_time"] = datetime.now()

    if df.empty:
        raise ValueError("No data after transformation")

    logging.info("Transformation complete")
    return df