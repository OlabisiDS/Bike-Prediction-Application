import streamlit as st
import numpy as np
import pandas as pd
import xgboost as xgb
import joblib

# Load the trained model and test data
model = joblib.load("bike_model")
X_test = joblib.load("bike_X_test.pkl")
y_test = joblib.load("bike_y_test.pkl")

# Function to preprocess inputs
def preprocess_inputs(inputs):
    # Convert inputs to a DataFrame for consistency with model training
    df_inputs = pd.DataFrame(inputs, columns=["yr", "mnth", "hr", "holiday", "weekday", "workingday", "weathersit", "temp", "hum", "windspeed"])
    return df_inputs

# Function to make predictions
def predict(inputs):
    preprocessed_inputs = preprocess_inputs(inputs)
    log_predictions = model.predict(preprocessed_inputs)
    predictions = np.expm1(log_predictions) 
    return predictions

# Streamlit UI
st.title("Bike Sharing Demand Prediction")

# User inputs
yr = st.selectbox("Year", options=[2011, 2012])
mnth = st.selectbox("Month", options=list(range(1, 13)))
hr = st.slider("Hour", 0, 23)
holiday = st.selectbox("Holiday", options=[0, 1])
weekday = st.selectbox("Weekday", options=list(range(0, 7)))
workingday = st.selectbox("Working Day", options=[0, 1])
weathersit = st.selectbox("Weather Situation", options=[1, 2, 3, 4])
temp = st.number_input("Temperature (normalized)", 0.0, 1.0)
hum = st.number_input("Humidity (normalized)", 0.0, 1.0)
windspeed = st.number_input("Wind Speed (normalized)", 0.0, 1.0)

# Button to make prediction
if st.button("Predict"):
    inputs = np.array([[yr, mnth, hr, holiday, weekday, workingday, weathersit, temp, hum, windspeed]])
    prediction = predict(inputs)
    st.write(f"Predicted Bike Rentals: {prediction[0]:.2f}")
