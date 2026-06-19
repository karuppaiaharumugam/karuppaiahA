# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Machine Learning libraries
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV

# Time series specific libraries
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import yfinance as yf

# Deep Learning for time series
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam

print("All libraries imported successfully!")
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
def time_series_analysis(data):
    """
    Perform time series analysis on gold prices
    """
    print("=== TIME SERIES ANALYSIS ===")
    
    # Seasonal decomposition
    decomposition = seasonal_decompose(data['Close'].resample('M').mean(), 
                                     period=12, model='additive')
    
    fig, axes = plt.subplots(4, 1, figsize=(15, 12))
    
    decomposition.observed.plot(ax=axes[0], title='Original Series', color='blue')
    decomposition.trend.plot(ax=axes[1], title='Trend', color='green')
    decomposition.seasonal.plot(ax=axes[2], title='Seasonality', color='red')
    decomposition.resid.plot(ax=axes[3], title='Residuals', color='purple')
    
    plt.tight_layout()
    plt.show()
    
    # Stationarity test (Augmented Dickey-Fuller test)
    print("\nStationarity Test (ADF):")
    adf_test = adfuller(data['Close'].dropna())
    print(f'ADF Statistic: {adf_test[0]:.6f}')
    print(f'p-value: {adf_test[1]:.6f}')
    print('Critical Values:')
    for key, value in adf_test[4].items():
        print(f'   {key}: {value:.3f}')
    
    if adf_test[1] <= 0.05:
        print("Series is stationary (reject null hypothesis)")
    else:
        print("Series is non-stationary (fail to reject null hypothesis)")
    
    # ACF and PACF plots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    plot_acf(data['Close'].diff().dropna(), ax=ax1, lags=40)
    plot_pacf(data['Close'].diff().dropna(), ax=ax2, lags=40)
    plt.tight_layout()
    plt.show()

# Perform time series analysis
time_series_analysis(gold_df)

def prepare_ml_data(df):
    """
    Prepare data for machine learning models
    """
    # Select features and target
    feature_columns = [col for col in df.columns if col not in ['Target', 'Close', 'Open', 'High', 'Low']]
    X = df[feature_columns]
    y = df['Target']
    
    # Split data (chronological split for time series)
    split_index = int(len(X) * 0.8)
    X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
    y_train, y_test = y.iloc[:split_index], y.iloc[split_index:]
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, feature_columns

def train_ml_models(X_train, X_test, y_train, y_test):
    """
    Train multiple machine learning models and compare performance
    """
    print("=== MACHINE LEARNING MODEL TRAINING ===")
    
    models = {
        'Linear Regression': LinearRegression(),
        'Lasso Regression': Lasso(alpha=0.1),
        'Ridge Regression': Ridge(alpha=0.1),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
        'Support Vector Regression': SVR(kernel='rbf', C=1.0, epsilon=0.1)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        
        # Train model
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        # Store results
        results[name] = {
            'model': model,
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'r2': r2,
            'predictions': y_pred
        }
        
        print(f"{name} Results:")
        print(f"  MAE: ${mae:.2f}")
        print(f"  RMSE: ${rmse:.2f}")
        print(f"  R² Score: {r2:.4f}")
    
    return results

# Prepare data and train models
X_train, X_test, y_train, y_test, scaler, feature_columns = prepare_ml_data(featured_gold_df)
ml_results = train_ml_models(X_train, X_test, y_train, y_test)