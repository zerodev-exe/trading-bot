import time
from utils.data import TradingBot
from utils.stocks import return_stock_data
from utils.logger import setup_logger

def run_live_trading(initial_balance=10000.0, scan_period: int = 30, trade_interval: str = "1d"):
    # Setup logger
    logger = setup_logger()
    logger.info("Starting Live Trading Bot")
    period = f"{scan_period}d"
    # Initialize trading bot
    bot = TradingBot(initial_balance)

    # Simple moving average strategy (copied from simulation)
    def should_buy(stock) -> bool:
        if len(stock.history) < 20:
            return False
        current_price = stock.price
        avg_price = sum(stock.history[-20:]) / 20
        return current_price < avg_price * 0.98

    def should_sell(stock) -> bool:
        if len(stock.history) < 20:
            return False
        current_price = stock.price
        avg_price = sum(stock.history[-20:]) / 20
        return current_price > avg_price * 1.02

    try:
        while True:
            # Update stock data
            STOCKS = return_stock_data(
                period=period,
                trade_interval=trade_interval
            )

            # Make trading decisions
            for symbol, stock in STOCKS.items():
                # Log current stock price and moving average
                if len(stock.history) >= 20:
                    avg_price = sum(stock.history[-20:]) / 20

                if should_buy(stock):
                    shares_to_buy = int(bot.balance * 0.1 / stock.price)
                    if shares_to_buy == 0:
                        continue
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
            time.sleep(60)

    except KeyboardInterrupt:
        logger.info("Trading bot stopped by user")
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
    finally:
        logger.info("Final Portfolio Status:")
        bot.log_portfolio_status(logger, STOCKS)

if __name__ == "__main__":
    run_live_trading(initial_balance=5000.0, scan_period=8, trade_interval="1m")
