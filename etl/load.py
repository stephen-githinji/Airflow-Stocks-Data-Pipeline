from sqlalchemy import create_engine 
import psycopg2
import config
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
import pandas as pd
import json

def load_stocks(transformed_data):
    clean_data = pd.DataFrame(json.loads(transformed_data))
    conn_engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    try:
        transformed_data.to_sql(name="stocks_data", con=conn_engine, if_exists="append", index= False)
        print("Data uploaded successfully!")

    except Exception as e:
        print(f"There was a problem loading data to the the DB!:\n{e}")

