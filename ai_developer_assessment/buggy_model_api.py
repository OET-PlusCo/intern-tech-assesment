"""
Customer Churn Prediction API
A FastAPI service that serves a machine learning model for predicting customer churn.

CONTEXT FOR CANDIDATE:
This API was working in development but is now failing in production.
Your task: Find and fix as many issues as you can in 15 minutes.
Think aloud and explain your reasoning as you debug.
"""

from fastapi import FastAPI, HTTPException
from pydette import BaseModel
import pandas as pd
import pickle
import numpy as np
from typing import List, Dict
import logging

app = FastAPI()

# Load the trained model
model = pickle.load(open("churn_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# Expected feature names for the model
EXPECTED_FEATURES = [
    "tenure", "monthly_charges", "total_charges", 
    "contract_type", "payment_method", "internet_service"
]

class CustomerData(BaseModel):
    customer_id: str
    tenure: int
    monthly_charges: float
    total_charges: str
    contract_type: str
    payment_method: str
    internet_service: str


@app.post("/predict")
async def predict_churn(customer: CustomerData):
    """
    Predict whether a customer will churn
    Returns: Probability of churn (0-1)
    """
    try:
        # Convert input to dictionary
        data = customer.dict()
        
        # Extract features
        features = {
            "tenure": data["tenure"],
            "monthly_charges": data["monthly_charges"],
            "total_charges": float(data["total_charges"]),
            "contract_type": data["contract_type"],
            "payment_method": data["payment_method"],
            "internet_service": data["internet_service"]
        }
        
        # Convert to DataFrame
        df = pd.DataFrame([features])
        
        # One-hot encode categorical variables
        df_encoded = pd.get_dummies(df, columns=["contract_type", "payment_method", "internet_service"])
        
        # Scale numerical features
        numerical_features = ["tenure", "monthly_charges", "total_charges"]
        df_encoded[numerical_features] = scaler.transform(df_encoded[numerical_features])
        
        # Make prediction
        prediction = model.predict_proba(df_encoded)[0][1]
        
        return {
            "customer_id": data["customer_id"],
            "churn_probability": prediction,
            "churn_prediction": "Yes" if prediction > 0.5 else "No"
        }
        
    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction failed")


@app.post("/predict_batch")
async def predict_batch(customers: List[CustomerData]):
    """
    Predict churn for multiple customers
    """
    results = []
    for customer in customers:
        result = await predict_churn(customer)
        results.append(result)
    
    return {"predictions": results}


@app.get("/health")
async def health_check():
    """Check if the service is running"""
    return {"status": "healthy"}


@app.get("/model_info")
def get_model_info():
    """Return information about the loaded model"""
    return {
        "model_type": type(model).__name__,
        "expected_features": EXPECTED_FEATURES,
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

