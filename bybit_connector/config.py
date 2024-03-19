# config.py

# Base API configurations
API_BASE_URL = "https://api.bybit.com"
WS_PUBLIC_URL = "wss://stream.bybit.com/realtime_public"
WS_PRIVATE_URL = "wss://stream.bybit.com/realtime_private"

# Endpoints
ORDER_ENDPOINT = "/v2/private/order/create"
QUERY_ENDPOINT = "/v2/private/order/list"

# Timeouts (in seconds)
REQUEST_TIMEOUT = 10

# Rate limiting settings
RATE_LIMIT = 600  # Max requests per time frame
TIME_FRAME = 5  # Time frame in seconds

# Trading pairs of interest
TRADING_PAIRS = ["LSKUSDT"]

# WebSocket configurations
WS_PING_INTERVAL = 30  # Ping interval in seconds for keeping the connection alive
WS_RECONNECT_DELAY = 5  # Delay in seconds before attempting to reconnect

# Logging settings
LOGGING_LEVEL = "INFO"
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Adjust and add more configurations as needed
