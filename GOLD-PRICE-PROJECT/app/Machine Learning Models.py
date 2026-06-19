
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