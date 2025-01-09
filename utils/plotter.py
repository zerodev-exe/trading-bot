from typing import Dict
from utils.data import Stock, TradingBot
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt

def plot_results(stocks: Dict[str, Stock], bot: TradingBot):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    for symbol, stock in stocks.items():
        ax1.plot(stock.dates, stock.history, label=symbol)

        # Plot buy points with green triangles
        if stock.buy_dates:
            ax1.scatter(stock.buy_dates, stock.buy_prices, 
                       marker='^', color='green', s=100, 
                       label=f'{symbol} Buys')

        # Plot sell points with red triangles
        if stock.sell_dates:
            ax1.scatter(stock.sell_dates, stock.sell_prices, 
                       marker='v', color='red', s=100, 
                       label=f'{symbol} Sells')

    ax1.set_title('Stock Prices Over Time')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price ($)')
    ax1.legend()
    ax1.grid(True)
    ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

    ax2.plot(bot.portfolio_dates, bot.portfolio_history, label='Portfolio Value', color='green')
    ax2.set_title('Portfolio Value Over Time')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Value ($)')
    ax2.legend()
    ax2.grid(True)
    ax2.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

    plt.tight_layout()
    plt.show()
