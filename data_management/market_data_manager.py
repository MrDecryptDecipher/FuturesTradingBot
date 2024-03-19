import os
import requests
import pandas as pd
from datetime import datetime, timedelta

class MarketDataManager:
    def __init__(self):
        self.symbol = 'LSKUSDT'
        self.api_key = os.getenv('BYBIT_API_KEY')
        self.base_url = "https://api.bybit.com"
        self.leverage = 16

    def fetch_historical_data(self, lookback_minutes=1440):
        """Fetches historical 1-minute kline data for the LSK/USDT pair."""
        end_time = int(datetime.now().timestamp())
        start_time = end_time - (lookback_minutes * 60)  # Calculate lookback period in seconds
        endpoint = f"{self.base_url}/public/linear/kline"
        params = {
            'symbol': self.symbol,
            'interval': 1,  # 1-minute interval
            'from': start_time,
            'limit': 200  # Maximum number of results (adjust as needed)
        }
        response = requests.get(endpoint, params=params).json()
        if response['ret_code'] == 0:
            # Ensure the 'result' key exists and it has a 'data' key
            if 'result' in response and 'data' in response['result']:
                data = pd.DataFrame(response['result']['data'])
                data['timestamp'] = pd.to_datetime(data['open_time'], unit='s')
                return data
            else:
                print("Unexpected response structure.")
                return pd.DataFrame()
        else:
            print("Failed to fetch historical data. Error:", response['ret_msg'])
            return pd.DataFrame()

    def fetch_live_data(self):
        """Fetches the latest market data snapshot for the LSK/USDT pair."""
        endpoint = f"{self.base_url}/v2/public/tickers"
        params = {'symbol': self.symbol}
        response = requests.get(endpoint, params=params).json()
        if response['ret_code'] == 0:
            data = pd.DataFrame([response['result']])
            return data
        else:
            print("Failed to fetch live data. Error:", response['ret_msg'])
            return pd.DataFrame()

    def save_data_to_csv(self, data, filename):
        """Saves the data to a CSV file."""
        filepath = os.path.join('data', f"{filename}.csv")  # Adjust the path according to your project structure
        data.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")

# Example usage
if __name__ == "__main__":
    manager = MarketDataManager()
    historical_data = manager.fetch_historical_data()
    live_data = manager.fetch_live_data()

    # Save fetched data for later use
    manager.save_data_to_csv(historical_data, "historical_data_LSKUSDT")
    manager.save_data_to_csv(live_data, "live_data_LSKUSDT")
