from datetime import datetime, timedelta
import time
from utils.data import TradingBot
from utils.stocks import return_stock_data
from utils.logger import setup_logger

def run_live_trading(initial_balance=10000.0, days: int = 30, trade_interval: str = "1d"):
    # Setup logger
    logger = setup_logger()
    logger.info("Starting Live Trading Bot")

    # Get initial stock data
    current_time = datetime.now()
    STOCK_DATA, STOCKS = return_stock_data(
        start_date=(current_time - timedelta(days=days)).strftime('%Y-%m-%d'),
        end_date=current_time.strftime('%Y-%m-%d'),
        trade_interval=trade_interval
    )
    # Initialize trading bot
    bot = TradingBot(initial_balance)

    # Simple moving average strategy (copied from simulation)
    def should_buy(stock):
        if len(stock.history) < 20:
            return False
        current_price = stock.price
        avg_price = sum(stock.history[-20:]) / 20
        return current_price < avg_price * 0.98

    def should_sell(stock):
        if len(stock.history) < 20:
            return False
        current_price = stock.price
        avg_price = sum(stock.history[-20:]) / 20
        return current_price > avg_price * 1.02

    # Make initial trading decisions based on historical data
    def make_initial_trades():
        logger.info("Making initial trading decisions...")
        for symbol, stock in STOCKS.items():
            if len(stock.history) >= 20:
                avg_price = sum(stock.history[-20:]) / 20
                logger.info(f"{symbol} - Initial Price: ${stock.price:.2f}, MA20: ${avg_price:.2f}")
                
                # Calculate potential position size (10% of portfolio per trade)
                shares_to_trade = int(bot.balance * 0.1 / stock.price)
                
                if stock.price < avg_price * 0.98:  # Price is below average - potential buy
                    if shares_to_trade > 0:
                        logger.info(f"Initial Buy Signal - Attempting to buy {shares_to_trade} shares of {symbol}")
                        if bot.buy(stock, shares_to_trade):
                            bot.log_trade(logger, "INITIAL BUY", stock, shares_to_trade, stock.price)
                
                elif stock.price > avg_price * 1.02:  # Price is above average - potential short
                    logger.info(f"Initial Sell Signal - No position to sell for {symbol}")

    # Execute initial trades
    make_initial_trades()

    # Log initial stock data
    logger.info("Initial Stock Data:")
    for symbol, stock in STOCKS.items():
        logger.info(f"{symbol}: ${stock.price:.2f} - History length: {len(stock.history)} - Last 5 prices: {stock.history[-5:] if len(stock.history) >= 5 else stock.history}")

    try:
        while True:
            current_time = datetime.now()
            
            # Update stock data
            STOCK_DATA, STOCKS = return_stock_data(
                start_date=(current_time - timedelta(days=days)).strftime('%Y-%m-%d'),
                end_date=current_time.strftime('%Y-%m-%d'),
                trade_interval=trade_interval
            )

            # Make trading decisions
            for symbol, stock in STOCKS.items():
                # Log current stock price and moving average
                if len(stock.history) >= 20:
                    avg_price = sum(stock.history[-20:]) / 20
                    logger.info(f"{symbol} - Current: ${stock.price:.2f}, MA20: ${avg_price:.2f}")

                if should_buy(stock):
                    shares_to_buy = int(bot.balance * 0.1 / stock.price)
                    logger.info(f"Attempting to buy {shares_to_buy} shares of {symbol}")
                    if shares_to_buy > 0:
                        if bot.buy(stock, shares_to_buy):
                            bot.log_trade(logger, "BUY", stock, shares_to_buy, stock.price)

                elif should_sell(stock):
                    shares_to_sell = bot.portfolio.get(symbol, 0)
                    if shares_to_sell > 0:
                        logger.info(f"Attempting to sell {shares_to_sell} shares of {symbol}")
                        if bot.sell(stock, shares_to_sell):
                            bot.log_trade(logger, "SELL", stock, shares_to_sell, stock.price)

            # Log portfolio status
            bot.log_portfolio_status(logger, STOCKS)

            # Wait for 60 seconds before next check
            time.sleep(10)

    except KeyboardInterrupt:
        logger.info("Trading bot stopped by user")
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
    finally:
        logger.info("Final Portfolio Status:")
        bot.log_portfolio_status(logger, STOCKS)

if __name__ == "__main__":
    run_live_trading(initial_balance=5000.0,days=30, trade_interval="5m")