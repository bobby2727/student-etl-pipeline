import requests
import pandas as pd
import logging
import config

def extract():
    logging.info("Extracting data from API")

    for i in range(3):  ##retry 
        try:
            response = requests.get(config.API_URL, timeout=5)
            response.raise_for_status()

            data = response.json()
            df = pd.DataFrame(data)

            logging.info("Extraction successful")
            return df

        except Exception as e:
            logging.warning(f"Retry {i+1} failed: {e}")

    raise Exception("API failed after retries")