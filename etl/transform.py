import pandas as pd

def transform_stocks(extracted_data):
    required_columns = ['name','symbol','from', 'open', 'high', 'low', 'close', 'volume', 'afterHours', 'preMarket']
    stocks_df = pd.DataFrame(extracted_data, columns=required_columns)
    #renaming the columns 
    stocks_df.rename(columns={'symbol':'ticker', 'from':'date'}, inplace=True)

    #storing the df into a parquet file
    # PROJECT_ROOT = path(__file__).resolve().parent().parent()
    # RAW_PATH = PROJECT_ROOT/"data"/"extracted.parquet"

    return stocks_df.to_json(orient='records')

