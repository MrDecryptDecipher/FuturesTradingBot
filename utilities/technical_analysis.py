import numpy as np
import pandas as pd

# Moving Average
def moving_average(data, period=20, indicator_type='SMA'):
    if indicator_type == 'SMA':
        return data.rolling(window=period).mean()
    elif indicator_type == 'EMA':
        return data.ewm(span=period, adjust=False).mean()
    else:
        raise ValueError("Indicator type must be either 'SMA' or 'EMA'")

# RSI
def rsi(data, period=14):
    delta = data.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# MACD
def macd(data, slow=26, fast=12, signal=9):
    ema_fast = data.ewm(span=fast, adjust=False).mean()
    ema_slow = data.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return pd.DataFrame({'MACD': macd_line, 'Signal_Line': signal_line})

# Bollinger Bands
def bollinger_bands(data, period=20, num_std=2):
    sma = data.rolling(window=period).mean()
    std = data.rolling(window=period).std()
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    return pd.DataFrame({'Upper_Band': upper_band, 'Lower_Band': lower_band, 'MA': sma})

# ATR
def atr(data, period=14):
    high_low = data['High'] - data['Low']
    high_close = np.abs(data['High'] - data['Close'].shift())
    low_close = np.abs(data['Low'] - data['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    return true_range.rolling(window=period).mean()

# Stochastics
def stochastics(data, k_period=14, d_period=3):
    low_min = data['Low'].rolling(window=k_period).min()
    high_max = data['High'].rolling(window=k_period).max()
    k_line = 100 * ((data['Close'] - low_min) / (high_max - low_min))
    d_line = k_line.rolling(window=d_period).mean()
    return pd.DataFrame({'%K': k_line, '%D': d_line})

# Implementing candlestick patterns
def bullish_engulfing(data):
    pattern = (data['Close'].shift(1) < data['Open'].shift(1)) & \
              (data['Open'] < data['Close']) & \
              (data['Open'] < data['Close'].shift(1)) & \
              (data['Close'] > data['Open'].shift(1))
    return pattern

# Bearish Engulfing Pattern
def bearish_engulfing(data):
    pattern = (data['Open'].shift(1) < data['Close'].shift(1)) & \
              (data['Close'] < data['Open']) & \
              (data['Close'].shift(1) < data['Open']) & \
              (data['Open'].shift(1) < data['Close'])
    return pattern

# Hammer
def hammer(data):
    body_size = np.abs(data['Close'] - data['Open'])
    candle_size = data['High'] - data['Low']
    lower_shadow = data['Open'] - data['Low']
    pattern = (body_size <= candle_size * 0.3) & (lower_shadow >= candle_size * 0.4)
    return pattern

# Inverted Hammer
def inverted_hammer(data):
    body_size = np.abs(data['Close'] - data['Open'])
    candle_size = data['High'] - data['Low']
    upper_shadow = data['High'] - np.maximum(data['Close'], data['Open'])
    pattern = (body_size <= candle_size * 0.3) & (upper_shadow >= candle_size * 0.4)
    return pattern

# Doji
def doji(data):
    body_size = np.abs(data['Close'] - data['Open'])
    candle_size = data['High'] - data['Low']
    pattern = (body_size <= candle_size * 0.1)
    return pattern

# Morning Star
def morning_star(data):
    first_candle = data['Close'].shift(2) > data['Open'].shift(2)
    second_candle = (data['High'].shift(1) - np.maximum(data['Open'].shift(1), data['Close'].shift(1))) > \
                    (np.abs(data['Close'].shift(1) - data['Open'].shift(1))) * 2
    third_candle = (data['Close'] > data['Open']) & \
                   (data['Open'] > data['Close'].shift(1)) & \
                   (data['Close'].shift(2) > data['Close'])
    pattern = first_candle & second_candle & third_candle
    return pattern

# Evening Star
def evening_star(data):
    first_candle = data['Open'].shift(2) > data['Close'].shift(2)
    second_candle = (data['High'].shift(1) - np.maximum(data['Open'].shift(1), data['Close'].shift(1))) > \
                    (np.abs(data['Close'].shift(1) - data['Open'].shift(1))) * 2
    third_candle = (data['Open'] > data['Close']) & \
                   (data['Open'].shift(1) < data['Close'].shift(2)) & \
                   (data['Close'].shift(2) < data['Close'])
    pattern = first_candle & second_candle & third_candle
    return pattern

# Bullish Harami
def bullish_harami(data):
    pattern = (data['Open'].shift(1) > data['Close'].shift(1)) & \
              (data['Close'] > data['Open']) & \
              (data['Close'].shift(1) > data['Open']) & \
              (data['Close'] > data['Open'].shift(1))
    return pattern

# Bearish Harami
def bearish_harami(data):
    pattern = (data['Close'].shift(1) > data['Open'].shift(1)) & \
              (data['Open'] > data['Close']) & \
              (data['Open'].shift(1) > data['Close']) & \
              (data['Open'] > data['Close'].shift(1))
    return pattern

# Piercing Pattern
def piercing_pattern(data):
    pattern = (data['Close'].shift(1) < data['Open'].shift(1)) & \
              (data['Open'] < data['Low'].shift(1)) & \
              (data['Close'] > data['Open'].shift(1)) & \
              (data['Close'] > (data['Open'].shift(1) + (data['Close'].shift(1) - data['Open'].shift(1)) / 2))
    return pattern

# Dark Cloud Cover
def dark_cloud_cover(data):
    pattern = (data['Open'].shift(1) < data['Close'].shift(1)) & \
              (data['Open'] > data['High'].shift(1)) & \
              (data['Close'] < data['Open'].shift(1)) & \
              (data['Close'] < (data['Close'].shift(1) - (data['Close'].shift(1) - data['Open'].shift(1)) / 2))
    return pattern

# Bullish Engulfing Pattern (revised with more clarity)
def bullish_engulfing_revised(data):
    pattern = (data['Close'].shift(1) < data['Open'].shift(1)) & \
              (data['Close'] > data['Open']) & \
              (data['Open'] < data['Close'].shift(1)) & \
              (data['Close'] > data['Open'].shift(1))
    return pattern

# Shooting Star
def shooting_star(data):
    upper_shadow = data['High'] - np.maximum(data['Open'], data['Close'])
    body_size = np.abs(data['Close'] - data['Open'])
    lower_shadow = np.minimum(data['Open'], data['Close']) - data['Low']
    pattern = (upper_shadow > body_size * 2) & (lower_shadow < body_size * 0.5)
    return pattern

# Hanging Man
def hanging_man(data):
    lower_shadow = np.minimum(data['Open'], data['Close']) - data['Low']
    body_size = np.abs(data['Close'] - data['Open'])
    upper_shadow = data['High'] - np.maximum(data['Open'], data['Close'])
    pattern = (lower_shadow > body_size * 2) & (upper_shadow < body_size * 0.5)
    return pattern

# Morning Star
def morning_star_revised(data):
    first_candle = data['Close'].shift(2) > data['Open'].shift(2)
    second_candle_gap = (data['High'].shift(1) < data['Low'].shift(2)) & (data['High'] < data['Low'].shift(1))
    third_candle = (data['Close'] > data['Open']) & (data['Close'].shift(2) < data['Open'])
    pattern = first_candle & second_candle_gap & third_candle
    return pattern

# Evening Star
def evening_star_revised(data):
    first_candle = data['Open'].shift(2) < data['Close'].shift(2)
    second_candle_gap = (data['Low'].shift(1) > data['High'].shift(2)) & (data['Low'] > data['High'].shift(1))
    third_candle = (data['Open'] > data['Close']) & (data['Close'].shift(2) > data['Close'])
    pattern = first_candle & second_candle_gap & third_candle
    return pattern

# Bullish Kicker
def bullish_kicker(data):
    pattern = (data['Open'].shift(1) > data['Close'].shift(1)) & \
              (data['Open'] > data['High'].shift(1))
    return pattern

# Bearish Kicker
def bearish_kicker(data):
    pattern = (data['Close'].shift(1) > data['Open'].shift(1)) & \
              (data['Open'] < data['Low'].shift(1))
    return pattern

# Bullish Abandoned Baby
def bullish_abandoned_baby(data):
    pattern = (data['Close'].shift(2) < data['Open'].shift(2)) & \
              (data['High'].shift(1) < data['Low'].shift(2)) & \
              (data['High'].shift(1) < data['Low']) & \
              (data['Close'] > data['Open'])
    return pattern

# Bearish Abandoned Baby
def bearish_abandoned_baby(data):
    pattern = (data['Close'].shift(2) > data['Open'].shift(2)) & \
              (data['Low'].shift(1) > data['High'].shift(2)) & \
              (data['Low'].shift(1) > data['High']) & \
              (data['Open'] > data['Close'])
    return pattern

# Bullish Harami Cross
def bullish_harami_cross(data):
    pattern = (data['Close'].shift(1) < data['Open'].shift(1)) & \
              (data['High'].shift(1) - data['Low'].shift(1) > 3 * (data['Open'].shift(1) - data['Close'].shift(1))) & \
              (data['Close'] > data['Open']) & \
              (data['Open'].shift(1) > data['Close']) & \
              (data['Open'] < data['Close'].shift(1))
    return pattern

# Bearish Harami Cross
def bearish_harami_cross(data):
    pattern = (data['Open'].shift(1) < data['Close'].shift(1)) & \
              (data['High'].shift(1) - data['Low'].shift(1) > 3 * (data['Close'].shift(1) - data['Open'].shift(1))) & \
              (data['Open'] > data['Close']) & \
              (data['Close'].shift(1) > data['Open']) & \
              (data['Close'] < data['Open'].shift(1))
    return pattern

# Bullish Tri Star
def bullish_tri_star(data):
    pattern = (data['Close'].shift(2) < data['Open'].shift(2)) & \
              (data['Close'].shift(1) > data['Open'].shift(1)) & \
              (data['Open'].shift(1) < data['Low'].shift(2)) & \
              (data['Close'] < data['Open']) & \
              (data['High'].shift(1) < data['Low'])
    return pattern

# Bearish Tri Star
def bearish_tri_star(data):
    pattern = (data['Open'].shift(2) < data['Close'].shift(2)) & \
              (data['Open'].shift(1) > data['Close'].shift(1)) & \
              (data['Close'].shift(1) > data['High'].shift(2)) & \
              (data['Open'] > data['Close']) & \
              (data['Low'].shift(1) > data['High'])
    return pattern

# Long Bullish Day
def long_bullish_day(data, threshold=0.03):
    body = data['Close'] - data['Open']
    total_range = data['High'] - data['Low']
    pattern = (body > threshold * total_range) & (data['Close'] > data['Open'])
    return pattern

# Long Bearish Day
def long_bearish_day(data, threshold=0.03):
    body = data['Open'] - data['Close']
    total_range = data['High'] - data['Low']
    pattern = (body > threshold * total_range) & (data['Open'] > data['Close'])
    return pattern

# Short Day
def short_day(data, threshold=0.01):
    body = np.abs(data['Close'] - data['Open'])
    total_range = data['High'] - data['Low']
    pattern = (body < threshold * total_range)
    return pattern

# White Marubozu
def white_marubozu(data):
    pattern = (data['Close'] > data['Open']) & \
              (data['Close'] == data['High']) & \
              (data['Open'] == data['Low'])
    return pattern

# Black Marubozu
def black_marubozu(data):
    pattern = (data['Open'] > data['Close']) & \
              (data['Open'] == data['High']) & \
              (data['Close'] == data['Low'])
    return pattern

# Bullish Closing Marubozu
def bullish_closing_marubozu(data):
    pattern = (data['Close'] > data['Open']) & \
              (data['Close'] == data['High']) & \
              (np.abs(data['Close'] - data['Open']) > (data['High'] - data['Low']) * 0.8)
    return pattern

# Bearish Closing Marubozu
def bearish_closing_marubozu(data):
    pattern = (data['Open'] > data['Close']) & \
              (data['Close'] == data['Low']) & \
              (np.abs(data['Close'] - data['Open']) > (data['High'] - data['Low']) * 0.8)
    return pattern

# Bullish Opening Marubozu
def bullish_opening_marubozu(data):
    pattern = (data['Close'] > data['Open']) & \
              (data['Open'] == data['Low']) & \
              (np.abs(data['Close'] - data['Open']) > (data['High'] - data['Low']) * 0.8)
    return pattern

# Bearish Opening Marubozu
def bearish_opening_marubozu(data):
    pattern = (data['Open'] > data['Close']) & \
              (data['Open'] == data['High']) & \
              (np.abs(data['Close'] - data['Open']) > (data['High'] - data['Low']) * 0.8)
    return pattern

# Spinning Top
def spinning_top(data, body_threshold=0.1, shadow_threshold=0.1):
    body = np.abs(data['Close'] - data['Open'])
    total_range = data['High'] - data['Low']
    upper_shadow = data['High'] - np.maximum(data['Close'], data['Open'])
    lower_shadow = np.minimum(data['Close'], data['Open']) - data['Low']
    pattern = (body < body_threshold * total_range) & \
              (upper_shadow > shadow_threshold * total_range) & \
              (lower_shadow > shadow_threshold * total_range)
    return pattern

# Doji
def doji(data, threshold=0.005):
    body = np.abs(data['Close'] - data['Open'])
    total_range = data['High'] - data['Low']
    pattern = (body <= threshold * total_range)
    return pattern

# Long Legged Doji
def long_legged_doji(data, body_threshold=0.005, shadow_threshold=0.1):
    body = np.abs(data['Close'] - data['Open'])
    total_range = data['High'] - data['Low']
    upper_shadow = data['High'] - np.maximum(data['Close'], data['Open'])
    lower_shadow = np.minimum(data['Close'], data['Open']) - data['Low']
    pattern = (body <= body_threshold * total_range) & \
              (upper_shadow > shadow_threshold * total_range) & \
              (lower_shadow > shadow_threshold * total_range)
    return pattern

# Gravestone Doji
def gravestone_doji(data, body_threshold=0.005, shadow_threshold=0.1):
    body = np.abs(data['Close'] - data['Open'])
    total_range = data['High'] - data['Low']
    upper_shadow = data['High'] - np.maximum(data['Close'], data['Open'])
    lower_shadow = np.minimum(data['Close'], data['Open']) - data['Low']
    pattern = (body <= body_threshold * total_range) & \
              (upper_shadow > shadow_threshold * total_range) & \
              (lower_shadow <= body_threshold * total_range)
    return pattern

# Dragonfly Doji
def dragonfly_doji(data, body_threshold=0.005, shadow_threshold=0.1):
    body = np.abs(data['Close'] - data['Open'])
    total_range = data['High'] - data['Low']
    upper_shadow = data['High'] - np.maximum(data['Close'], data['Open'])
    lower_shadow = np.minimum(data['Close'], data['Open']) - data['Low']
    pattern = (body <= body_threshold * total_range) & \
              (lower_shadow > shadow_threshold * total_range) & \
              (upper_shadow <= body_threshold * total_range)
    return pattern

# Hammer
def hammer(data, body_threshold=0.03, shadow_threshold=0.2):
    body = np.abs(data['Close'] - data['Open'])
    total_range = data['High'] - data['Low']
    lower_shadow = np.minimum(data['Close'], data['Open']) - data['Low']
    upper_shadow = data['High'] - np.maximum(data['Close'], data['Open'])
    pattern = (body < body_threshold * total_range) & \
              (lower_shadow >= shadow_threshold * total_range) & \
              (upper_shadow < body_threshold * total_range) & \
              (data['Close'] > data['Open'])
    return pattern

# Inverted Hammer
def inverted_hammer(data, body_threshold=0.03, shadow_threshold=0.2):
    body = np.abs(data['Close'] - data['Open'])
    total_range = data['High'] - data['Low']
    upper_shadow = data['High'] - np.maximum(data['Close'], data['Open'])
    lower_shadow = np.minimum(data['Close'], data['Open']) - data['Low']
    pattern = (body < body_threshold * total_range) & \
              (upper_shadow >= shadow_threshold * total_range) & \
              (lower_shadow < body_threshold * total_range) & \
              (data['Close'] > data['Open'])
    return pattern


# Hanging Man
def hanging_man(data):
    body = np.abs(data['Close'] - data['Open'])
    total_range = data['High'] - data['Low']
    lower_shadow = data['Low'] - np.minimum(data['Close'], data['Open'])
    upper_shadow = np.maximum(data['Close'], data['Open']) - data['High']
    pattern = (lower_shadow > body * 2) & (upper_shadow < body) & (body < total_range * 0.2)
    return pattern

# Shooting Star
def shooting_star(data):
    body = np.abs(data['Close'] - data['Open'])
    total_range = data['High'] - data['Low']
    upper_shadow = data['High'] - np.maximum(data['Close'], data['Open'])
    lower_shadow = np.minimum(data['Close'], data['Open']) - data['Low']
    pattern = (upper_shadow > body * 2) & (lower_shadow < body) & (body < total_range * 0.2)
    return pattern

# Piercing Pattern
def piercing_pattern(data):
    pattern = (data['Close'].shift(1) < data['Open'].shift(1)) & \
              (data['Open'] < data['Low'].shift(1)) & \
              (data['Close'] > (data['Open'].shift(1) + (data['Close'].shift(1) - data['Open'].shift(1)) / 2)) & \
              (data['Close'] < data['Open'].shift(1))
    return pattern

# Dark Cloud Cover
def dark_cloud_cover(data):
    pattern = (data['Close'].shift(1) > data['Open'].shift(1)) & \
              (data['Open'] > data['Close'].shift(1)) & \
              (data['Close'] < (data['Open'].shift(1) + (data['Close'].shift(1) - data['Open'].shift(1)) / 2)) & \
              (data['Close'] > data['Open'])
    return pattern

# Morning Star
def morning_star(data):
    pattern = (data['Close'].shift(2) < data['Open'].shift(2)) & \
              (data['Close'].shift(1) < data['Open'].shift(1)) & \
              (data['Open'] < data['Close']) & \
              (data['Close'].shift(2) > data['Open']) & \
              (data['Open'].shift(1) < data['Close'].shift(2))
    return pattern

# Evening Star
def evening_star(data):
    pattern = (data['Close'].shift(2) > data['Open'].shift(2)) & \
              (data['Close'].shift(1) > data['Open'].shift(1)) & \
              (data['Open'] > data['Close']) & \
              (data['Close'].shift(2) < data['Open']) & \
              (data['Open'].shift(1) > data['Close'].shift(2))
    return pattern

# Upper Window (Gap Up)
def upper_window(data):
    pattern = data['Low'] > data['High'].shift(1)
    return pattern

# Lower Window (Gap Down)
def lower_window(data):
    pattern = data['High'] < data['Low'].shift(1)
    return pattern

# Morning Doji Star
def morning_doji_star(data):
    pattern = (data['Close'].shift(2) < data['Open'].shift(2)) & \
              (abs(data['Close'].shift(1) - data['Open'].shift(1)) <= (data['High'].shift(1) - data['Low'].shift(1)) * 0.1) & \
              (data['Close'] > data['Open']) & \
              (data['Open'].shift(1) < data['Close'].shift(2)) & \
              (data['Open'] < data['Open'].shift(1)) & \
              (data['Close'] > data['Close'].shift(1))
    return pattern

# Evening Doji Star
def evening_doji_star(data):
    pattern = (data['Close'].shift(2) > data['Open'].shift(2)) & \
              (abs(data['Close'].shift(1) - data['Open'].shift(1)) <= (data['High'].shift(1) - data['Low'].shift(1)) * 0.1) & \
              (data['Open'] > data['Close']) & \
              (data['Open'].shift(1) > data['Close'].shift(2)) & \
              (data['Open'] > data['Open'].shift(1)) & \
              (data['Close'] < data['Close'].shift(1))
    return pattern

# Bullish Doji Star
def bullish_doji_star(data):
    pattern = (data['Close'].shift(1) < data['Open'].shift(1)) & \
              (abs(data['Close'] - data['Open']) <= (data['High'] - data['Low']) * 0.1) & \
              (data['Low'] > data['High'].shift(1))
    return pattern

# Bearish Doji Star
def bearish_doji_star(data):
    pattern = (data['Open'].shift(1) < data['Close'].shift(1)) & \
              (abs(data['Close'] - data['Open']) <= (data['High'] - data['Low']) * 0.1) & \
              (data['High'] < data['Low'].shift(1))
    return pattern

# Three White Soldiers
def three_white_soldiers(data):
    pattern = (data['Close'] > data['Open']) & \
              (data['Close'].shift(1) > data['Open'].shift(1)) & \
              (data['Close'].shift(2) > data['Open'].shift(2)) & \
              (data['Close'] > data['Close'].shift(1)) & \
              (data['Close'].shift(1) > data['Close'].shift(2)) & \
              (data['Open'].shift(1) > data['Open'].shift(2)) & \
              (data['Open'] < data['Close'].shift(1)) & \
              (data['Open'].shift(1) < data['Close'].shift(2))
    return pattern

# Three Black Crows
def three_black_crows(data):
    pattern = (data['Open'] > data['Close']) & \
              (data['Open'].shift(1) > data['Close'].shift(1)) & \
              (data['Open'].shift(2) > data['Close'].shift(2)) & \
              (data['Close'] < data['Close'].shift(1)) & \
              (data['Close'].shift(1) < data['Close'].shift(2)) & \
              (data['Open'].shift(1) < data['Open'].shift(2)) & \
              (data['Open'] > data['Close'].shift(1)) & \
              (data['Open'].shift(1) > data['Close'].shift(2))
    return pattern

# Three Identical Crows
def three_identical_crows(data):
    pattern = (data['Open'] > data['Close']) & \
              (data['Open'].shift(1) > data['Close'].shift(1)) & \
              (data['Open'].shift(2) > data['Close'].shift(2)) & \
              (data['Close'] == data['Close'].shift(1)) & \
              (data['Close'].shift(1) == data['Close'].shift(2)) & \
              (data['Open'] > data['Open'].shift(1)) & \
              (data['Open'].shift(1) > data['Open'].shift(2))
    return pattern

# Two Crows
def two_crows(data):
    pattern = (data['Close'].shift(2) > data['Open'].shift(2)) & \
              (data['Open'].shift(1) < data['Close'].shift(2)) & \
              (data['Close'].shift(1) < data['Open'].shift(1)) & \
              (data['Close'].shift(1) > data['Open'].shift(2)) & \
              (data['Open'] < data['Close'].shift(1)) & \
              (data['Open'] > data['Close']) & \
              (data['Close'] > data['Open'].shift(2))
    return pattern

# Upside Gap Two Crows
def upside_gap_two_crows(data):
    pattern = (data['Close'].shift(2) > data['Open'].shift(2)) & \
              (data['Open'].shift(1) > data['Close'].shift(2)) & \
              (data['Close'].shift(1) < data['Open'].shift(1)) & \
              (data['Close'].shift(1) > data['Open'].shift(2)) & \
              (data['Open'] > data['Close']) & \
              (data['Open'] < data['Close'].shift(1)) & \
              (data['Close'] > data['Close'].shift(2))
    return pattern

# Unique Three River Bottom
def unique_three_river_bottom(data):
    pattern = (data['Close'].shift(2) < data['Open'].shift(2)) & \
              (data['High'].shift(1) < data['Low'].shift(2)) & \
              (data['Open'].shift(1) < data['Close'].shift(1)) & \
              (data['Open'].shift(1) < data['Low'].shift(2)) & \
              (data['Open'] < data['Close']) & \
              (data['Open'] < data['Low'].shift(1)) & \
              (data['Close'] > data['Close'].shift(1))
    return pattern

# Three Inside Up
def three_inside_up(data):
    pattern = (data['Close'].shift(2) < data['Open'].shift(2)) & \
              (data['Open'].shift(1) > data['Close'].shift(2)) & \
              (data['Close'].shift(1) < data['Open'].shift(1)) & \
              (data['Close'].shift(1) > data['Open'].shift(2)) & \
              (data['Close'] > data['Open']) & \
              (data['Close'] > data['High'].shift(1))
    return pattern

# Three Inside Down
def three_inside_down(data):
    pattern = (data['Close'].shift(2) > data['Open'].shift(2)) & \
              (data['Open'].shift(1) < data['Close'].shift(2)) & \
              (data['Close'].shift(1) > data['Open'].shift(1)) & \
              (data['Close'].shift(1) < data['Open'].shift(2)) & \
              (data['Open'] > data['Close']) & \
              (data['Open'] > data['High'].shift(1))
    return pattern

# Three Outside Up
def three_outside_up(data):
    pattern = (data['Open'].shift(1) > data['Close'].shift(1)) & \
              (data['Close'] > data['Open']) & \
              (data['Open'] < data['Close'].shift(1)) & \
              (data['Close'] > data['Open'].shift(1))
    return pattern

# Three Outside Down
def three_outside_down(data):
    pattern = (data['Close'].shift(1) > data['Open'].shift(1)) & \
              (data['Open'] > data['Close']) & \
              (data['Open'].shift(1) < data['Close']) & \
              (data['Close'].shift(1) < data['Open'])
    return pattern

# Bullish Meeting Line
def bullish_meeting_line(data):
    pattern = (data['Close'].shift(1) < data['Open'].shift(1)) & \
              (data['Close'] > data['Open']) & \
              (np.abs(data['Close'] - data['Close'].shift(1)) < (data['High'] - data['Low']) * 0.1)
    return pattern

# Bearish Meeting Line
def bearish_meeting_line(data):
    pattern = (data['Open'].shift(1) < data['Close'].shift(1)) & \
              (data['Open'] > data['Close']) & \
              (np.abs(data['Close'] - data['Close'].shift(1)) < (data['High'] - data['Low']) * 0.1)
    return pattern

# Bullish Belt Hold
def bullish_belt_hold(data):
    pattern = (data['Open'] == data['Low']) & \
              (data['Close'] > data['Open']) & \
              (data['Close'] != data['High']) & \
              (data['Open'].shift(1) > data['Close'].shift(1))
    return pattern

# Bearish Belt Hold
def bearish_belt_hold(data):
    pattern = (data['Open'] == data['High']) & \
              (data['Close'] < data['Open']) & \
              (data['Close'] != data['Low']) & \
              (data['Open'].shift(1) < data['Close'].shift(1))
    return pattern

# Three Stars In The South
def three_stars_in_the_south(data):
    first_candle = (data['Close'].shift(2) < data['Open'].shift(2)) & \
                   (data['Close'].shift(2) == data['Low'].shift(2))
    second_candle = (data['Close'].shift(1) < data['Open'].shift(1)) & \
                    (data['Low'].shift(1) > data['Low'].shift(2)) & \
                    (data['Close'].shift(1) < data['Open'].shift(2))
    third_candle = (data['Close'] < data['Open']) & \
                   (data['Low'] > data['Low'].shift(1)) & \
                   (data['Close'] < data['Open'].shift(1))
    pattern = first_candle & second_candle & third_candle
    return pattern

# Advance Block
def advance_block(data):
    first_candle = (data['Close'].shift(2) > data['Open'].shift(2)) & \
                   (data['Close'].shift(2) < data['High'].shift(2))
    second_candle = (data['Close'].shift(1) > data['Open'].shift(1)) & \
                    (data['Close'].shift(1) < data['High'].shift(1)) & \
                    (data['Close'].shift(1) > data['Close'].shift(2))
    third_candle = (data['Close'] > data['Open']) & \
                   (data['Close'] < data['High']) & \
                   (data['Close'] > data['Close'].shift(1))
    pattern = first_candle & second_candle & third_candle
    return pattern

# Deliberation
def deliberation(data):
    pattern = (data['Close'].shift(2) > data['Open'].shift(2)) & \
              (data['Close'].shift(1) > data['Open'].shift(1)) & \
              (data['Open'] > data['Close']) & \
              ((data['High'] - data['Low']) > 3 * (data['Open'] - data['Close']))
    return pattern

# Stick Sandwich
def stick_sandwich(data):
    pattern = (data['Open'].shift(2) > data['Close'].shift(2)) & \
              (data['Open'].shift(1) < data['Close'].shift(1)) & \
              (data['Open'] > data['Close']) & \
              (data['Close'].shift(2) == data['Close'])
    return pattern

# Homing Pigeon
def homing_pigeon(data):
    pattern = (data['Open'].shift(1) > data['Close'].shift(1)) & \
              (data['Open'] < data['Close']) & \
              (data['Open'] < data['Close'].shift(1)) & \
              (data['Close'] > data['Open'].shift(1))
    return pattern

# Matching Low
def matching_low(data):
    pattern = (data['Close'] == data['Low']) & \
              (data['Close'].shift(1) == data['Low'].shift(1))
    return pattern

# Matching High
def matching_high(data):
    pattern = (data['Close'] == data['High']) & \
              (data['Close'].shift(1) == data['High'].shift(1))
    return pattern

# Ladder Bottom
def ladder_bottom(data):
    pattern = (data['Close'].shift(3) < data['Open'].shift(3)) & \
              (data['Close'].shift(2) < data['Open'].shift(2)) & \
              (data['Close'].shift(1) < data['Open'].shift(1)) & \
              (data['Close'] > data['Open'])
    return pattern

# Concealing Baby Swallow
def concealing_baby_swallow(data):
    pattern = (data['Open'].shift(3) > data['Close'].shift(3)) & \
              (data['Open'].shift(2) > data['Close'].shift(2)) & \
              (data['Close'].shift(2) < data['Open'].shift(3)) & \
              (data['Open'].shift(1) < data['Close'].shift(2)) & \
              (data['Close'].shift(1) < data['Open'].shift(1)) & \
              (data['Close'] < data['Open']) & \
              (data['Close'] < data['Open'].shift(1))
    return pattern

# Bullish Breakaway
def bullish_breakaway(data):
    pattern = (data['Close'].shift(4) > data['Open'].shift(4)) & \
              (data['Close'].shift(3) < data['Open'].shift(3)) & \
              (data['Close'].shift(2) < data['Close'].shift(3)) & \
              (data['Close'].shift(1) < data['Close'].shift(2)) & \
              (data['Close'] > data['Open']) & \
              (data['Close'] > data['High'].shift(4))
    return pattern

# Bearish Breakaway
def bearish_breakaway(data):
    pattern = (data['Close'].shift(4) < data['Open'].shift(4)) & \
              (data['Close'].shift(3) > data['Open'].shift(3)) & \
              (data['Close'].shift(2) > data['Close'].shift(3)) & \
              (data['Close'].shift(1) > data['Close'].shift(2)) & \
              (data['Open'] > data['Close']) & \
              (data['Close'] < data['Low'].shift(4))
    return pattern

# Upside Tasuki Gap
def upside_tasuki_gap(data):
    pattern = (data['Close'].shift(2) > data['Open'].shift(2)) & \
              (data['Open'].shift(1) > data['Close'].shift(2)) & \
              (data['Close'].shift(1) > data['Open'].shift(1)) & \
              (data['Open'] < data['Close'].shift(1)) & \
              (data['Open'] > data['Close']) & \
              (data['Close'] > data['Open'].shift(1))
    return pattern

# Downside Tasuki Gap
def downside_tasuki_gap(data):
    pattern = (data['Open'].shift(2) > data['Close'].shift(2)) & \
              (data['Open'].shift(1) < data['Close'].shift(2)) & \
              (data['Close'].shift(1) < data['Open'].shift(1)) & \
              (data['Open'] > data['Close'].shift(1)) & \
              (data['Open'] < data['Close']) & \
              (data['Close'] < data['Open'].shift(1))
    return pattern

# On Neck Line
def on_neck_line(data):
    pattern = (data['Open'].shift(1) > data['Close'].shift(1)) & \
              (data['Open'] > data['Close']) & \
              (np.abs(data['Close'] - data['Low'].shift(1)) < (data['High'].shift(1) - data['Low'].shift(1)) * 0.1)
    return pattern

# In Neck Line
def in_neck_line(data):
    pattern = (data['Open'].shift(1) > data['Close'].shift(1)) & \
              (data['Open'] > data['Close']) & \
              (data['Close'] > data['Close'].shift(1)) & \
              (np.abs(data['Close'].shift(1) - data['Close']) < (data['High'].shift(1) - data['Low'].shift(1)) * 0.1)
    return pattern

# Thrusting
def thrusting(data):
    pattern = (data['Open'].shift(1) > data['Close'].shift(1)) & \
              (data['Open'] > data['Close']) & \
              (data['Close'] < data['High'].shift(1)) & \
              (data['Close'] > (data['Close'].shift(1) + data['Open'].shift(1)) / 2)
    return pattern

# Bullish Side By Side White Lines
def bullish_side_by_side_white_lines(data):
    pattern = (data['Close'].shift(2) < data['Open'].shift(2)) & \
              (data['Close'].shift(1) > data['Open'].shift(1)) & \
              (data['Close'] > data['Open']) & \
              (data['Open'].shift(1) == data['Open']) & \
              (data['Close'].shift(1) == data['Close'])
    return pattern

# Bearish Side By Side White Lines
def bearish_side_by_side_white_lines(data):
    pattern = (data['Open'].shift(2) > data['Close'].shift(2)) & \
              (data['Open'].shift(1) < data['Close'].shift(1)) & \
              (data['Open'] < data['Close']) & \
              (data['Close'].shift(1) == data['Close']) & \
              (data['Open'].shift(1) == data['Open'])
    return pattern

# Bullish Separating Lines
def bullish_separating_lines(data):
    pattern = (data['Close'].shift(1) < data['Open'].shift(1)) & \
              (data['Close'] > data['Open']) & \
              (data['Open'].shift(1) == data['Open'])
    return pattern

# Bearish Separating Lines
def bearish_separating_lines(data):
    pattern = (data['Open'].shift(1) < data['Close'].shift(1)) & \
              (data['Open'] > data['Close']) & \
              (data['Close'].shift(1) == data['Close'])
    return pattern

# Rising Three Method
def rising_three_method(data):
    pattern = (data['Close'].shift(3) > data['Open'].shift(3)) & \
              (data['Open'].shift(2) < data['Close'].shift(2)) & \
              (data['Open'].shift(1) < data['Close'].shift(1)) & \
              (data['Close'].shift(1) < data['Close'].shift(3)) & \
              (data['Close'] > data['High'].shift(2))
    return pattern

# Falling Three Method
def falling_three_method(data):
    pattern = (data['Open'].shift(3) > data['Close'].shift(3)) & \
              (data['Close'].shift(2) < data['Open'].shift(2)) & \
              (data['Close'].shift(1) < data['Open'].shift(1)) & \
              (data['Open'].shift(1) > data['Open'].shift(3)) & \
              (data['Close'] < data['Low'].shift(2))
    return pattern

# Mat Hold
def mat_hold(data):
    pattern = (data['Close'].shift(4) > data['Open'].shift(4)) & \
              (data['Close'].shift(3) < data['Open'].shift(3)) & \
              (data['Close'].shift(2) < data['Close'].shift(3)) & \
              (data['Close'].shift(1) < data['Close'].shift(2)) & \
              (data['Close'] > data['High'].shift(3))
    return pattern

# Bullish Three Line Strike
def bullish_three_line_strike(data):
    pattern = (data['Close'].shift(3) < data['Open'].shift(3)) & \
              (data['Close'].shift(2) < data['Close'].shift(3)) & \
              (data['Close'].shift(1) < data['Close'].shift(2)) & \
              (data['Open'] < data['Close'].shift(1)) & \
              (data['Close'] > data['Open'].shift(3))
    return pattern

# Bearish Three Line Strike
def bearish_three_line_strike(data):
    pattern = (data['Close'].shift(3) > data['Open'].shift(3)) & \
              (data['Close'].shift(2) > data['Close'].shift(3)) & \
              (data['Close'].shift(1) > data['Close'].shift(2)) & \
              (data['Open'] > data['Close'].shift(1)) & \
              (data['Close'] < data['Open'].shift(3))
    return pattern

# Upside Gap Three Method
def upside_gap_three_method(data):
    pattern = (data['Close'].shift(2) > data['Open'].shift(2)) & \
              (data['Low'].shift(1) > data['High'].shift(2)) & \
              (data['Close'].shift(1) > data['Open'].shift(1)) & \
              (data['Close'] > data['Open']) & \
              (data['Open'] > data['Close'].shift(1))
    return pattern

# Downside Gap Three Method
def downside_gap_three_method(data):
    pattern = (data['Open'].shift(2) > data['Close'].shift(2)) & \
              (data['High'].shift(1) < data['Low'].shift(2)) & \
              (data['Open'].shift(1) > data['Close'].shift(1)) & \
              (data['Open'] > data['Close']) & \
              (data['Close'] < data['Open'].shift(1))
    return pattern

# Tweezer Bottom
def tweezer_bottom(data):
    pattern = (data['Low'] == data['Low'].shift(1)) & \
              ((data['Open'] > data['Close']) & (data['Open'].shift(1) < data['Close'].shift(1)) | \
               (data['Open'] < data['Close']) & (data['Open'].shift(1) > data['Close'].shift(1)))
    return pattern

# Tweezer Top
def tweezer_top(data):
    pattern = (data['High'] == data['High'].shift(1)) & \
              ((data['Open'] > data['Close']) & (data['Open'].shift(1) < data['Close'].shift(1)) | \
               (data['Open'] < data['Close']) & (data['Open'].shift(1) > data['Close'].shift(1)))
    return pattern

