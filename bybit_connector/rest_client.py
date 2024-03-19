import logging
import requests
import time
import hmac
import hashlib
import os
from datetime import datetime, timedelta

class BybitRESTClient:
    """REST client for interacting with the Bybit API."""

    def __init__(self, base_url="https://api.bybit.com", api_key=None, api_secret=None):
        # Allow for both constructor injection and environment variable usage
        self.api_key = api_key or os.getenv('BYBIT_API_KEY')
        self.api_secret = api_secret or os.getenv('BYBIT_API_SECRET')
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)  # Initialize logger

    def _generate_signature(self, params: dict) -> str:
        """Generates a signed query string for authenticated requests."""
        query_string = '&'.join([f"{key}={params[key]}" for key in sorted(params)])
        return hmac.new(self.api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

    def _make_request(self, endpoint: str, method: str, params: dict) -> dict:
        """Makes a REST API request with error handling and retries."""
        for attempt in range(3):
            try:
                if method == "GET":
                    response = requests.get(self.base_url + endpoint, params=params)
                elif method == "POST":
                    response = requests.post(self.base_url + endpoint, params=params)
                response.raise_for_status()  # Raise an exception for non-200 status codes
                self.logger.debug(f"API request successful: {endpoint} ({method})")
                return response.json()
            except requests.exceptions.RequestException as e:
                self.logger.error(f"API request failed (attempt {attempt+1}): {e}")
                time.sleep(2 ** attempt)  # Exponential backoff
        raise RuntimeError(f"API request failed after 3 retries: {endpoint}")

    def place_order(self, symbol: str, side: str, order_type: str, qty: float, price: float = None, stop_loss: float = None, take_profit: float = None, time_in_force="GoodTillCancel", leverage: int = 16) -> dict:
        """Places an order with optional stop loss, take profit, and leverage."""
        endpoint = "/v2/private/order/create"
        params = {
            "api_key": self.api_key,
            "timestamp": int(time.time() * 1000),
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "qty": qty,
            "time_in_force": time_in_force,
            "leverage": leverage,
        }

        if price:
            params["price"] = price

        if stop_loss:
            params["stop_loss"] = stop_loss

        if take_profit:
            params["take_profit"] = take_profit

        params["sign"] = self._generate_signature(params)
        return self._make_request(endpoint, "POST", params)

    def get_order_status(self, order_id: str) -> dict:
        """Gets the status of an order."""
        endpoint = f"/v2/private/order/search?order_id={order_id}"
        params = {
            "api_key": self.api_key,
            "timestamp": int(time.time() * 1000),
        }
        params["sign"] = self._generate_signature(params)
        return self._make_request(endpoint, "GET", params)

    def cancel_order(self, order_id: str) -> dict:
        """Cancels an order."""
        endpoint = "/v2/private/order/cancel"
        params = {
            "api_key": self.api_key,
            "timestamp": int(time.time() * 1000),
            "order_id": order_id,
        }
        params["sign"] = self._generate_signature(params)
        return self._make_request(endpoint, "POST", params)

def get_account_info(self) -> dict:
    """Gets account information (balance, positions, etc.)."""
    endpoint = "/v2/private/wallet/info"
    params = {
        "api_key": self.api_key,
        "timestamp": int(time.time() * 1000),
    }
    params["sign"] = self._generate_signature(params)
    return self._make_request(endpoint, "GET", params)

def get_active_orders(self, symbol: str = None) -> list[dict]:
    """Gets a list of your active (open) orders."""
    endpoint = "/v2/private/order/list"
    params = {
        "api_key": self.api_key,
        "timestamp": int(time.time() * 1000),
        "status": "Open"  # Filter for open orders only
    }
    if symbol:
        params["symbol"] = symbol
    params["sign"] = self._generate_signature(params)
    return self._make_request(endpoint, "GET", params)

def get_historical_data(self, symbol: str, start_time: datetime, end_time: datetime, interval: str) -> list[dict]:
    """Retrieves historical candlestick data for backtesting and training."""
    endpoint = "/v2/public/kline/list"
    params = {
        "symbol": symbol,
        "interval": interval,
        "from": int(start_time.timestamp() * 1000),
        "to": int(end_time.timestamp() * 1000),
    }
    return self._make_request(endpoint, "GET", params)

def adjust_stop_loss(self, order_id: str, new_stop_loss: float) -> dict:
    """Adjusts the stop-loss level for an open order.

    This functionality is not directly supported by Bybit's REST API.
    It's implemented by canceling the existing order and placing a new one
    with the updated stop-loss level.
    """
    current_order = self.get_order_status(order_id)
    if current_order["order_status"] != "Open":
        raise ValueError("Order is not open and cannot be adjusted")

    # Cancel the existing order
    self.cancel_order(order_id)
    self.logger.info(f"Canceled order {order_id} to adjust stop-loss")

    # Place a new order with the updated stop-loss
    new_order_params = {
        "symbol": current_order["symbol"],
        "side": current_order["side"],
        "order_type": current_order["order_type"],
        "qty": current_order["orig_qty"],
        "price": current_order.get("price"),  # Preserve original price if any
        "stop_loss": new_stop_loss,
    }
    new_order = self.place_order(**new_order_params)
    self.logger.info(f"Placed new order {new_order['order_id']} with adjusted stop-loss")

    return new_order

def execute_kill_switch(self) -> None:
    """Closes all open positions and stops trading.

    This iterates over active orders, canceling them and potentially adding logic
    to close existing positions by placing market orders in the opposite direction.
    """
    active_orders = self.get_active_orders()
    for order in active_orders:
        self.cancel_order(order["order_id"])
        self.logger.info(f"Canceled order {order['order_id']} during kill switch")

        # Add logic to close positions based on your risk management strategy
        # (e.g., place market orders in the opposite direction)
        # ... (your position closing logic)

# Example usage:
if __name__ == "__main__":
    # Today's date in Indian Standard Time (IST)
    today = datetime.now(timezone(timedelta(hours=5, minutes=30)))  # Adjust for IST

    # Get a list of your active LSK/USDT orders
    client = BybitRESTClient()
    active_orders = client.get_active_orders(symbol="LSKUSDT")
    print(active_orders)

    # Retrieve historical data for backtesting (example for past month)
    start_time = today - timedelta(days=30)
    end_time = today
    interval = "1d"  # Daily candlesticks
    historical_data = client.get_historical_data("LSKUSDT", start_time, end_time, interval)
    print(historical_data)

