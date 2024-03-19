import os
import sys
sys.path.append('bybit_connector')  # Ensure modules in bybit_connector are accessible
sys.path.append('data_management')  # Ensure modules in data_management are accessible
sys.path.append('execution')        # Ensure modules in execution are accessible
sys.path.append('strategy')         # Ensure modules in strategy are accessible
sys.path.append('utilities')        # Ensure modules in utilities are accessible

from strategy.trading_bot_core import TradingBot  # Assuming TradingBot is the main class of your strategy

def main():
    # Initialize the trading bot
    bot = TradingBot()

    # Run the trading bot
    bot.run()

    print("Bot execution started. Monitoring trades...")

if __name__ == "__main__":
    main()
