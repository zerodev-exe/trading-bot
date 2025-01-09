from typing import List, Dict
import pandas as pd
from datetime import datetime

class Stock:
    def __init__(self, symbol: str, data: pd.DataFrame):
        self.symbol = symbol
        self.data = data
        self.current_idx = 0
        self.price = data['Close'].iloc[0]
        self.history: List[float] = data['Close'].tolist()
        self.dates: List[datetime] = data.index.tolist()
        self.buy_dates: List[datetime] = []
        self.buy_prices: List[float] = []
        self.sell_dates: List[datetime] = []
        self.sell_prices: List[float] = []
        
    def update_price(self, current_date: datetime) -> float:
        if self.current_idx < len(self.data):
            self.price = self.data['Close'].iloc[self.current_idx]
            self.history.append(self.price)
            self.dates.append(current_date)
            self.current_idx += 1
        return self.price

class TradingBot:
    def __init__(self, initial_balance: float):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.portfolio: Dict[str, int] = {}
        self.trade_history: List[str] = []
        self.portfolio_history: List[float] = [initial_balance]
        self.portfolio_dates: List[datetime] = [datetime.now()]
        self.total_trades = 0

    def buy(self, stock: Stock, quantity: int) -> bool:
        cost = stock.price * quantity
        if cost <= self.balance:
            self.balance -= cost
            self.portfolio[stock.symbol] = self.portfolio.get(stock.symbol, 0) + quantity
            self.trade_history.append(f"Bought {quantity} shares of {stock.symbol} at ${stock.price:.2f}")
            stock.buy_dates.append(stock.dates[-1])
            stock.buy_prices.append(stock.price)
            self.total_trades += 1
            return True
        return False
    
    def sell(self, stock: Stock, quantity: int) -> bool:
        if stock.symbol in self.portfolio and self.portfolio[stock.symbol] >= quantity:
            self.balance += stock.price * quantity
            self.portfolio[stock.symbol] -= quantity
            self.trade_history.append(f"Sold {quantity} shares of {stock.symbol} at ${stock.price:.2f}")
            stock.sell_dates.append(stock.dates[-1])
            stock.sell_prices.append(stock.price)
            self.total_trades += 1
            return True
        return False
    
    def get_portfolio_value(self, stocks: Dict[str, Stock]) -> float:
        total = self.balance
        for symbol, quantity in self.portfolio.items():
            total += stocks[symbol].price * quantity
        return total

    def log_portfolio_status(self, logger, stocks):
        logger.info(f"Current Balance: ${self.balance:.2f}")
        logger.info("Current Portfolio:")
        for symbol, quantity in self.portfolio.items():
            logger.info(f"  {symbol}: {quantity} shares")
        logger.info(f"Total Portfolio Value: ${self.get_portfolio_value(stocks):.2f}")
        logger.info("-" * 50)

    def log_trade(self, logger, action, stock, quantity, price):
        total = price * quantity
        logger.info(f"{action}: {quantity} shares of {stock.symbol} @ ${price:.2f} (Total: ${total:.2f})")
