import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import pickle

df = pd.read_csv('Metro_Interstate_Traffic_Volume (1).csv')
df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

# Extract numerical features from time
df['hour'] = df['datetime'].dt.hour
df['day_of_week'] = df['datetime'].dt.dayofweek
df['month'] = df['datetime'].dt.month

# Encode categorical columns (Weather_Main and Weather_Description)
le_main = LabelEncoder()
df['Weather_Main'] = le_main.fit_transform(df['Weather_Main'])

le_desc = LabelEncoder()
df['Weather_Description'] = le_desc.fit_transform(df['Weather_Description'])

X = df.drop(['Traffic_Volume', 'Date', 'Time', 'datetime'], axis=1)
y = df['Traffic_Volume']

print("Training model...")
# Using n_estimators=100 for a balance of speed and accuracy during local execution
rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X, y)

print("Saving model and encoders...")
with open('Smart_Traffic_Prediction_System.pickle', 'wb') as f:
    pickle.dump({
        'model': rf,
        'le_main': le_main,
        'le_desc': le_desc,
        'features': X.columns.tolist()
    }, f)

print("Done.")