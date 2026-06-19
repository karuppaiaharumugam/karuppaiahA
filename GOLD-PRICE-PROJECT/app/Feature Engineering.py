import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
def create_technical_indicators(data):
    """
    Create technical indicators for gold price prediction
    """
    df = data.copy()
    
    # Price-based features
    df['Price_Range'] = df['High'] - df['Low']
    df['Price_Gap'] = df['Open'] - df['Close'].shift(1)
    
    # Moving averages
    df['MA_7'] = df['Close'].rolling(window=7).mean()
    df['MA_21'] = df['Close'].rolling(window=21).mean()
    df['MA_50'] = df['Close'].rolling(window=50).mean()
    
    # Price relative to moving averages
    df['Price_vs_MA7'] = df['Close'] / df['MA_7']
    df['Price_vs_MA21'] = df['Close'] / df['MA_21']
    
    # Volatility indicators
    df['Volatility_7'] = df['Close'].rolling(window=7).std()
    df['Volatility_21'] = df['Close'].rolling(window=21).std()
    
    # Momentum indicators
    df['Momentum_7'] = df['Close'] - df['Close'].shift(7)
    df['Momentum_21'] = df['Close'] - df['Close'].shift(21)
    
    # RSI (Relative Strength Index)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD (Moving Average Convergence Divergence)
    exp1 = df['Close'].ewm(span=12).mean()
    exp2 = df['Close'].ewm(span=26).mean()
    df['MACD'] = exp1 - exp2
    df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
    
    # Bollinger Bands
    df['BB_Middle'] = df['Close'].rolling(window=20).mean()
    bb_std = df['Close'].rolling(window=20).std()
    df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
    df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
    df['BB_Width'] = df['BB_Upper'] - df['BB_Lower']
    
    # Target variable (next day's closing price)
    df['Target'] = df['Close'].shift(-1)
    
    # Remove rows with NaN values
    df = df.dropna()
    
    print(f"Feature engineering completed. Total features: {len(df.columns)}")
    print("Features created:", list(df.columns))
    
    return df

# Apply feature engineering
featured_gold_df = create_technical_indicators(gold_df)