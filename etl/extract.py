from config import MASSIVE_API_KEY
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import time
#packages for asynchronous development
import asyncio
import aiohttp
from aiolimiter import AsyncLimiter

test_date = date(2026, 5, 20)

current_date = datetime.now().date()
one_month_ago = current_date - relativedelta(months=1)

url = "https://api.massive.com/v1/open-close"

parameters = {
    "apiKey" : MASSIVE_API_KEY
}

tickers = {
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corp',
    'AMZN': 'Amazon.Com Inc',
    'GOOGL': 'Alphabet Inc. Class A Common Stock',
    'NVDA': 'Nvidia Corp',
    'TSLA': 'Tesla, Inc. Common Stock',
    'META': 'Meta Platforms, Inc. Class A Common Stock',
    'NFLX': 'NetFlix Inc',
    'DIS': 'The Walt Disney Company',
    'BRK.B': 'BERKSHIRE HATHAWAY Class B'
}


limiter = AsyncLimiter(3, 35)
async def get_stock_task(session, url, ticker):
    async with limiter:
        async with session.get(f"{url}/{ticker}/{test_date}", params= parameters) as response:
            response.raise_for_status()
            print(f"{ticker} data extracted successfully!")
            stock = await response.json()
            stock['name'] = tickers[ticker]
            return stock
        
async def extract_stocks():
    start = time.perf_counter()
    async with aiohttp.ClientSession() as session:
        if limiter.has_capacity():
            tasks = [get_stock_task(session, url, ticker) for ticker in list(tickers.keys())]
            stocks = await asyncio.gather(*tasks)

    print(f"Time taken : {time.perf_counter() - start}")
    return stocks

