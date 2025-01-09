from datetime import datetime, timedelta
from utils.data import Stock, TradingBot
from utils.stocks import return_stock_data
import matplotlib.pyplot as plt


def run_simulation(money: float = 10000.0, start_date: str = "2022-01-01", end_date: str = "2024-12-31", trade_interval: str = "1h"):
    total_profit = 0
    total_roi = 0
    profitable_simulations = 0
    all_results = []

    # Track best and worst simulations
    best_profit = float('-inf')
    worst_profit = float('inf')
    
    print(f"Running the simulation...")
    
    bot = TradingBot(money)

    # Simple moving average strategy
    def should_buy(stock: Stock) -> bool:
        if len(stock.history) < 20:  # Increased window for more stability
            return False
        current_price = stock.price
        avg_price = sum(stock.history[-20:]) / 20
        return current_price < avg_price * 0.90  # Buy when price is 2% below MA

    def should_sell(stock: Stock) -> bool:
        if len(stock.history) < 20:
            return False
        current_price = stock.price
        avg_price = sum(stock.history[-20:]) / 20
        return current_price > avg_price * 1.10  # Sell when price is 2% above MA

    # Run simulation
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    trading_days = len(next(iter(STOCK_DATA.values())))

    for day in range(trading_days):
        current_date = start_datetime + timedelta(days=day)

        # Update stock prices
        for symbol, stock in STOCKS.items():
            stock.update_price(current_date)

        # Make trading decisions
        for symbol, stock in STOCKS.items():
            if should_buy(stock):
                shares_to_buy = int(bot.balance * 0.1 / stock.price)
                if shares_to_buy > 0:
                    bot.buy(stock, shares_to_buy)
            elif should_sell(stock):
                shares_to_sell = bot.portfolio.get(symbol, 0)
                if shares_to_sell > 0:
                    bot.sell(stock, shares_to_sell)

        portfolio_value = bot.get_portfolio_value(STOCKS)
        bot.portfolio_history.append(portfolio_value)
        bot.portfolio_dates.append(current_date)

    # Calculate results for this simulation
    final_portfolio_value = bot.get_portfolio_value(STOCKS)
    sim_profit = final_portfolio_value - bot.initial_balance
    sim_roi = (sim_profit / bot.initial_balance) * 100

    # Track best and worst results
    if sim_profit >= best_profit:
        best_profit = sim_profit

    if sim_profit <= worst_profit:
        worst_profit = sim_profit

    total_profit += sim_profit
    total_roi += sim_roi
    if sim_profit > 0:
        profitable_simulations += 1

    all_results.append(sim_roi)

    # Calculate statistics
    avg_profit = total_profit
    avg_roi = total_roi
    roi_std = (sum((x - avg_roi) ** 2 for x in all_results)) ** 0.5

    # Calculate average trades per simulation
    avg_trades = bot.total_trades

    print("\nSimulation Results:")
    print(f"Period: {start_date} to {end_date}")
    print(f"Stonks: ${avg_profit:,.2f}")
    print(f"Average ROI: {avg_roi:.1f}%")
    print(f"ROI Standard Deviation: {roi_std:.1f}%")
    print(f"Trades per Simulation: {avg_trades:.1f}")
    print(f"Total Trades Across All Simulations: {bot.total_trades:,}")

    plt.figure(figsize=(12, 6))
    plt.plot(bot.portfolio_dates, bot.portfolio_history, label='Portfolio Value')
    plt.title('Portfolio Value Over Time')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value ($)')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    money = 10000
    start_date = "2024-01-01"
    end_date = "2025-01-07"
    trade_interval = "1d"

    STOCK_DATA, STOCKS = return_stock_data(start_date=start_date, end_date=end_date, trade_interval=trade_interval)
    run_simulation(
        money=money,
        start_date=start_date,
        end_date=end_date,
        trade_interval=trade_interval
    )
    # calculate_perfect_trades(STOCKS, money)