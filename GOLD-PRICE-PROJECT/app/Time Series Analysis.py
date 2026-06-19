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