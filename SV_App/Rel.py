# predict_price.py
import numpy as np
import pandas as pd
from keras.models import load_model
import pickle
import os
from . import DBMS
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client['AI']
collection = db['Data_Stock']

def pred_Rel():
    # ========================
    # 1. Define Features and Look-Back Period
    # ========================

    doc={"Symbol":"RELIANCE.BO"}
    record=collection.find_one(doc)


    features = ['Open', 'High', 'Low', 'P/E Ratio', 'Google Trends', 'Price Change']
    look_back = 60  # Must match the look-back period used during training

    # ========================
    # 2. Load the Trained Model and Scalers
    # ========================
    try:
        m_path=r"D:\Vasu\MP HMR\Models\trained_model_Rel.h5"
        model = load_model(m_path)
        print("Model loaded successfully.")
    except Exception as e:
        raise ValueError(f"Error loading model: {e}")

    try:
        xp_path=r"D:\Vasu\MP HMR\Pfiles\scaler_X_Rel.pkl"
        with open(xp_path, 'rb') as f:
            scaler_X = pickle.load(f)
        print("Scaler_X loaded successfully.")
    except Exception as e:
        raise ValueError(f"Error loading scaler_X: {e}")

    try:
        yp_path=r"D:\Vasu\MP HMR\Pfiles\scaler_y_Rel.pkl"
        with open(yp_path, 'rb') as f:
            scaler_y = pickle.load(f)
        print("Scaler_y loaded successfully.")
    except Exception as e:
        raise ValueError(f"Error loading scaler_y: {e}")

    # ========================
    # 3. Load or Create Historical Data
    # ========================
    historical_file = 'historical_data_rel.csv'

    if not os.path.isfile(historical_file):
        print(f"'{historical_file}' not found. Creating it from 'Reliance-Stock.csv'.")
        data_path="D:\Vasu\MP HMR\Data\Reliance-Stock-data.csv"
        data = pd.read_csv(data_path)

        # Ensure the Date column is in datetime format
        if 'Date' in data.columns:
            data['Date'] = pd.to_datetime(data['Date'])

        # Sort the data by date if not already sorted
        data = data.sort_values('Date')

        # Convert features to numeric, coercing errors to NaN
        for col in features:
            data[col] = pd.to_numeric(data[col], errors='coerce')

        # Handle missing values
        data = data.fillna(method='ffill').fillna(method='bfill')

        # Verify no NaN or infinite values
        if data[features].isnull().sum().any():
            raise ValueError("Historical data contains NaN values even after filling. Please check your data.")
        if np.isinf(data[features].values).any():
            raise ValueError("Historical data contains infinite values. Please check and handle them.")

        # Get the last look_back days of data
        historical_data = data[features].iloc[-look_back:]
        
        # Save to CSV
        historical_data.to_csv(historical_file, index=False)
        print(f"'{historical_file}' has been created with the last {look_back} records.")
    else:
        # Load historical data
        historical_data = pd.read_csv(historical_file)
        print(f"Loaded '{historical_file}' successfully.")

    # ========================
    # 4. Validate Historical Data
    # ========================
    # Ensure that historical data has the required features
    missing_features = [f for f in features if f not in historical_data.columns]
    if missing_features:
        raise ValueError(f"Missing features in historical data: {missing_features}")
    print("Historical data contains all required features.")

    # Ensure historical data has exactly look_back rows
    if len(historical_data) != look_back:
        if len(historical_data) > look_back:
            historical_data = historical_data.iloc[-look_back:]
            print(f"Historical data trimmed to the last {look_back} records.")
        else:
            raise ValueError(f"Historical data must contain exactly {look_back} rows, but has {len(historical_data)}.")
    else:
        print(f"Historical data has {look_back} records as expected.")

    # Convert features to numeric
    for col in features:
        historical_data[col] = pd.to_numeric(historical_data[col], errors='coerce')

    # Handle missing values
    historical_data = historical_data.fillna(method='ffill').fillna(method='bfill')

    # Verify no NaN or infinite values
    if historical_data.isnull().sum().any():
        raise ValueError("Historical data contains NaN values after filling. Please check your data.")
    if np.isinf(historical_data.values).any():
        raise ValueError("Historical data contains infinite values. Please check and handle them.")

    print("Historical data is clean and ready for prediction.")

    # ========================
    # 5. Collect User Input for the Latest Day
    # ========================
    print("\nPlease enter the latest day's data for prediction.")
    latest_day_data = {}
    symbol="RELIANCE.BO"
    query="RELIANCE"
    DBMS.store_data(symbol,query)
    for feature in features:
        while True:
            try:
                value = float(record[f"{feature}"])
                latest_day_data[feature] = value
                break
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

    # ========================
    # 6. Append Latest Day Data to Historical Data
    # ========================
    latest_day_df = pd.DataFrame([latest_day_data])
    input_data = pd.concat([historical_data, latest_day_df], ignore_index=True)
    print("Latest day's data appended to historical data.")

    # ========================
    # 7. Scale the Input Data
    # ========================
    try:
        input_data_scaled = scaler_X.transform(input_data[features])
        print("Input data scaled successfully.")
    except Exception as e:
        raise ValueError(f"Error during scaling input data: {e}")

    # ========================
    # 8. Validate Scaled Input Data
    # ========================
    print(f"Scaled input data range for features: min={input_data_scaled.min()}, max={input_data_scaled.max()}")

    # ========================
    # 9. Prepare Input Sequence for Prediction
    # ========================
    # Ensure that we have exactly look_back + 1 records after appending the latest day
    if input_data_scaled.shape[0] != look_back + 1:
        raise ValueError(f"Expected {look_back + 1} rows after appending, but got {input_data_scaled.shape[0]} rows.")

    # Extract the last look_back records for prediction
    input_sequence = input_data_scaled[-look_back:].reshape(1, look_back, len(features))
    print(f"Input sequence shape: {input_sequence.shape}")

    # ========================
    # 10. Make the Prediction
    # ========================
    predicted_price_scaled = model.predict(input_sequence)
    print(f"Model prediction (scaled): {predicted_price_scaled}")

    # Check if prediction is within [0,1]
    if np.any(predicted_price_scaled < 0) or np.any(predicted_price_scaled > 1):
        print("Warning: Model prediction is outside the [0,1] range.")
    else:
        print("Model prediction is within the [0,1] range.")

    # ========================
    # 11. Inverse Transform the Prediction
    # ========================
    predicted_closing_price = scaler_y.inverse_transform(predicted_price_scaled)[0][0]
    print(f"\nPredicted Closing Price: {predicted_closing_price:.2f}")
    filter = {'Symbol': 'RELIANCE.BO'}
    new_field = {'$set': {'Predicted Price':f'{predicted_closing_price:.2f}'}}
    collection.update_one(filter, new_field)