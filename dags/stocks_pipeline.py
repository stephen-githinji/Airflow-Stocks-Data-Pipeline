from airflow.sdk import dag, task
from etl.extract import extract_stocks
from etl.transform import transform_stocks
from etl.load import load_stocks
from datetime import datetime, timedelta
import asyncio

defaults = {
    "owner":"who_else", 
    "retries":3, 
    "retries_delay":timedelta(25)}

@dag(
        dag_id="stocks_dag", 
        start_date=datetime(2026, 1, 1),
        schedule="@daily", 
        catchup=False, 
        default_args=defaults)
def stocks_data_pipeline():
    @task
    def extract():
        return asyncio.run(extract_stocks())
    @task
    def transform(raw_data):
        return transform_stocks(raw_data)
    @task
    def load(clean_data):
        return load_stocks(clean_data)
    
    raw_data = extract()
    clean_data = transform(raw_data=raw_data)
    load(clean_data=clean_data)

stocks_data_pipeline()



