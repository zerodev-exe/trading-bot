import pandas as pd
import yfinance as yf
from utils.data import Stock

def get_stock_data(symbol: str, start_date: str, end_date: str, trade_interval: str = "1h") -> pd.DataFrame:
    try:
        stock = yf.Ticker(symbol)
        # Using daily data instead of minute data for more reliable results
        data = stock.history(start=start_date, end=end_date, interval=trade_interval)

        if data.empty:
            print(f"Warning: No data found for {symbol}")
            return pd.DataFrame()

        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return pd.DataFrame()


def return_stock_data(start_date, end_date, trade_interval):
    # Read stock symbols from CSV file
    stocks_df = pd.read_csv('stocks.csv')
    symbols = stocks_df['Ticker'].tolist()

    # Get historical data for each symbol
    STOCK_DATA = {}
    for symbol in symbols:
        data = get_stock_data(symbol, start_date, end_date, trade_interval=trade_interval)
        if not data.empty:
            STOCK_DATA[symbol] = data

    # Initialize stocks with historical data 
    STOCKS = {
        symbol: Stock(symbol, data)
        for symbol, data in STOCK_DATA.items()
    }

    return STOCKS