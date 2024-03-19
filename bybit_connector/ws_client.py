import websocket
import json
import hmac
import hashlib
import time
import logging
import os
from backoff import expo  # for backoff strategy

# Configure logging from separate file (logging.ini)
logging.config.fileConfig('logging.ini')
logger = logging.getLogger(__name__)

API_KEY = os.getenv('BYBIT_API_KEY')
API_SECRET = os.getenv('BYBIT_API_SECRET')
RECONNECT_ATTEMPTS = 5  # Number of reconnection attempts
CHANNEL = "trade.LSKUSDT"  # Example channel (can be customized)


def generate_signature(secret, message):
    return hmac.new(bytes(secret, 'utf-8'), msg=bytes(message, 'utf-8'), digestmod=hashlib.sha256).hexdigest()


def on_message(ws, message):
    """Parses and processes incoming messages."""
    try:
        data = json.loads(message)
        if data["op"] == "ping":
            # Respond to pings from server to keep connection alive
            ws.send(json.dumps({"op": "pong"}))
        elif data["op"] == "subscribe":
            # Handle successful subscription confirmation
            logger.info(f"Subscribed to channel: {data['args'][0]}")
        elif data["op"] == "request.error":
            # Log errors received from the server
            logger.error(f"Request error: {data['error']['message']}")
        else:
            # Extract relevant data for your trading bot (e.g., trade details)
            # ... your data processing logic here ...
            logger.debug(f"Received data: {data}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")


@expo  # Use exponential backoff for reconnection attempts
def connect(ws):
    """Connects to the Bybit WebSocket endpoint with retries."""
    try:
        ws.connect("wss://stream.bybit.com/realtime_public")
    except Exception as e:
        logger.error(f"Connection error: {e}")
        raise


def on_error(ws, error):
    """Handles errors and triggers reconnection."""
    logger.error(f"WebSocket error: {error}")
    ws.close()  # Close the current connection


def on_close(ws):
    """Handles connection closure and triggers reconnection."""
    logger.info("Connection closed. Attempting reconnection...")
    ws.run_forever()  # Restart the connection loop


def on_open(ws):
    """Performs authentication and subscribes to channels upon connection."""
    logger.info("Opened connection")

    timestamp = int(time.time() * 1000)
    params = f'api_key={API_KEY}&timestamp={timestamp}'
    signature = generate_signature(API_SECRET, params)

    auth_data = {
        "op": "auth",
        "args": [API_KEY, timestamp, signature]
    }

    ws.send(json.dumps(auth_data))

    # Subscribe to the desired channel
    subscribe_message = {
        "op": "subscribe",
        "args": [CHANNEL]
    }
    ws.send(json.dumps(subscribe_message))


if __name__ == "__main__":
    for attempt in range(RECONNECT_ATTEMPTS):
        try:
            ws = websocket.WebSocketApp(
                "wss://stream.bybit.com/realtime_public",
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            ws.on_open = on_open
            ws.run_forever()
            break  # Exit the loop on successful connection
        except Exception as e:
            logger.error(f"Connection failed (attempt {attempt + 1}/{RECONNECT_ATTEMPTS}). Error: {e}")
            time.sleep(expo(base=2, max_value=10))  # Backoff before retry

    if attempt == RECONNECT_ATTEMPTS - 1:
        logger.error("Failed to connect after all attempts. Exiting.")
