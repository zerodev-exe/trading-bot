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
    # Get historical data once
    STOCK_DATA = {
        "AAPL": get_stock_data("AAPL", start_date, end_date, trade_interval=trade_interval),  # Apple
        "MSFT": get_stock_data("MSFT", start_date, end_date, trade_interval=trade_interval),  # Microsoft 
        "AMZN": get_stock_data("AMZN", start_date, end_date, trade_interval=trade_interval),  # Amazon
        "GOOGL": get_stock_data("GOOGL", start_date, end_date, trade_interval=trade_interval), # Alphabet
        "NVDA": get_stock_data("NVDA", start_date, end_date, trade_interval=trade_interval),  # NVIDIA
        "META": get_stock_data("META", start_date, end_date, trade_interval=trade_interval),  # Meta Platforms
        "BRK-B": get_stock_data("BRK-B", start_date, end_date, trade_interval=trade_interval), # Berkshire Hathaway
        "TSLA": get_stock_data("TSLA", start_date, end_date, trade_interval=trade_interval),  # Tesla
        "LLY": get_stock_data("LLY", start_date, end_date, trade_interval=trade_interval),    # Eli Lilly
        "V": get_stock_data("V", start_date, end_date, trade_interval=trade_interval),        # Visa
        "UNH": get_stock_data("UNH", start_date, end_date, trade_interval=trade_interval),    # UnitedHealth
        "JPM": get_stock_data("JPM", start_date, end_date, trade_interval=trade_interval),    # JPMorgan Chase
        "JNJ": get_stock_data("JNJ", start_date, end_date, trade_interval=trade_interval),    # Johnson & Johnson
        "XOM": get_stock_data("XOM", start_date, end_date, trade_interval=trade_interval),    # ExxonMobil
        "WMT": get_stock_data("WMT", start_date, end_date, trade_interval=trade_interval),    # Walmart
        "MA": get_stock_data("MA", start_date, end_date, trade_interval=trade_interval),      # Mastercard
        "PG": get_stock_data("PG", start_date, end_date, trade_interval=trade_interval),      # Procter & Gamble
        "HD": get_stock_data("HD", start_date, end_date, trade_interval=trade_interval),      # Home Depot
        "CVX": get_stock_data("CVX", start_date, end_date, trade_interval=trade_interval),    # Chevron
        "AVGO": get_stock_data("AVGO", start_date, end_date, trade_interval=trade_interval),  # Broadcom
        "QCOM": get_stock_data("QCOM", start_date, end_date, trade_interval=trade_interval),  # Qualcom
        "PLTR": get_stock_data("PLTR", start_date, end_date, trade_interval=trade_interval),  # Qualcom
        "BITF": get_stock_data("BITF", start_date, end_date, trade_interval=trade_interval),  # Qualcom
    }

    # Initialize stocks with historical data
    STOCKS = {
        symbol: Stock(symbol, data) 
        for symbol, data in STOCK_DATA.items()
    }

    return STOCK_DATA, STOCKS