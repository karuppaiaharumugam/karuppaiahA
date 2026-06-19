# Comprehensive EDA function
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
def perform_eda(data):
    """
    Perform exploratory data analysis on gold price data
    """
    print("=== EXPLORATORY DATA ANALYSIS ===")
    
    # Basic information
    print("\n1. Dataset Info:")
    print(f"Shape: {data.shape}")
    print(f"Date Range: {data.index.min()} to {data.index.max()}")
    print(f"Total Days: {len(data)}")
    
    # Statistical summary
    print("\n2. Statistical Summary:")
    print(data.describe())
    
    # Check for missing values
    print("\n3. Missing Values:")
    print(data.isnull().sum())
    
    # Create visualization subplots
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('Gold Price Analysis - Comprehensive EDA', fontsize=16)
    
    # Price trend
    axes[0, 0].plot(data.index, data['Close'], color='gold', linewidth=1)
    axes[0, 0].set_title('Gold Price Trend Over Time')
    axes[0, 0].set_ylabel('Price ($)')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Distribution of closing prices
    axes[0, 1].hist(data['Close'], bins=50, color='gold', alpha=0.7, edgecolor='black')
    axes[0, 1].set_title('Distribution of Closing Prices')
    axes[0, 1].set_xlabel('Price ($)')
    axes[0, 1].set_ylabel('Frequency')
    
    # Monthly average prices
    monthly_avg = data['Close'].resample('M').mean()
    axes[0, 2].plot(monthly_avg.index, monthly_avg.values, color='darkorange', linewidth=2)
    axes[0, 2].set_title('Monthly Average Gold Prices')
    axes[0, 2].set_ylabel('Price ($)')
    axes[0, 2].grid(True, alpha=0.3)
    
    # Volatility (rolling standard deviation)
    rolling_volatility = data['Close'].rolling(window=30).std()
    axes[1, 0].plot(rolling_volatility.index, rolling_volatility.values, color='red', linewidth=1)
    axes[1, 0].set_title('30-Day Rolling Volatility')
    axes[1, 0].set_ylabel('Volatility')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Correlation heatmap
    correlation_matrix = data.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=axes[1, 1])
    axes[1, 1].set_title('Feature Correlation Matrix')
    
    # Daily returns
    daily_returns = data['Close'].pct_change().dropna()
    axes[1, 2].hist(daily_returns, bins=100, color='lightblue', alpha=0.7, edgecolor='black')
    axes[1, 2].set_title('Distribution of Daily Returns')
    axes[1, 2].set_xlabel('Daily Return')
    axes[1, 2].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.show()
    
    return data

# Perform EDA
gold_df = perform_eda(gold_df)