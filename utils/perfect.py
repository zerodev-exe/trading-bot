from typing import List, Dict
import pandas as pd
from datetime import datetime

class Stock:
    def __init__(self, symbol: str, data: pd.DataFrame):
        self.symbol = symbol
        self.data = data
        self.current_idx = 0
        self.price = data['Close'].iloc[0]
        self.history: List[float] = []
        self.dates: List[datetime] = []
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


def calculate_perfect_trades(stocks: Dict[str, Stock], initial_balance: float) -> None:
    print("\nPerfect Trading Analysis:")
    print("-" * 50)
    
    total_profit = 0
    trades = []
    
    for symbol, stock in stocks.items():
        # Get all prices and dates
        prices = stock.history
        dates = stock.dates
        
        if not prices:
            continue
            
        # Find best buy-sell combinations
        max_profit = 0
        best_buy_date = None
        best_sell_date = None
        best_buy_price = 0
        best_sell_price = 0
        
        for buy_idx in range(len(prices)):
            for sell_idx in range(buy_idx + 1, len(prices)):
                buy_price = prices[buy_idx]
                sell_price = prices[sell_idx]
                profit = sell_price - buy_price
                
                if profit > max_profit:
                    max_profit = profit
                    best_buy_date = dates[buy_idx]
                    best_sell_date = dates[sell_idx]
                    best_buy_price = buy_price
                    best_sell_price = sell_price
        
        if max_profit > 0:
            # Calculate maximum shares possible with initial balance
            max_shares = int(initial_balance / best_buy_price)
            potential_profit = max_shares * max_profit
            total_profit += potential_profit
            
            trades.append({
                'symbol': symbol,
                'buy_date': best_buy_date,
                'sell_date': best_sell_date,
                'buy_price': best_buy_price,
                'sell_price': best_sell_price,
                'profit_per_share': max_profit,
                'max_shares': max_shares,
                'potential_profit': potential_profit
            })
    
    # Sort trades by potential profit
    trades.sort(key=lambda x: x['potential_profit'], reverse=True)
    
    # Print results
    for trade in trades:
        print(f"\n{trade['symbol']}:")
        print(f"Buy Date: {trade['buy_date'].strftime('%Y-%m-%d')}")
        print(f"Buy Price: ${trade['buy_price']:.2f}")
        print(f"Sell Date: {trade['sell_date'].strftime('%Y-%m-%d')}")
        print(f"Sell Price: ${trade['sell_price']:.2f}")
        print(f"Profit per Share: ${trade['profit_per_share']:.2f}")
        print(f"Maximum Shares Possible: {trade['max_shares']:,}")
        print(f"Potential Profit: ${trade['potential_profit']:,.2f}")
    
    print("\nSummary:")
    print("-" * 50)
    print(f"Total Potential Profit: ${total_profit:,.2f}")
    print(f"Return on Investment: {(total_profit/initial_balance)*100:.1f}%")
