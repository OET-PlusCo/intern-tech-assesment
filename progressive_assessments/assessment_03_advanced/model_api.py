"""
Production ML API for containerized deployment

This is the same API from Assessment #2, but now needs to be containerized properly.
Your focus should be on fixing the Dockerfile and docker-compose.yml.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
import numpy as np
import pickle
import logging
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Churn Prediction API - Containerized")

# Load secrets from environment (but they're exposed in Dockerfile!)
API_KEY = os.getenv("API_KEY", "default-key")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "default-password")
JWT_SECRET = os.getenv("JWT_SECRET", "default-jwt-secret")

# Global model variable
model = None


class CustomerFeatures(BaseModel):
    """Customer features for churn prediction"""
    customer_id: str
    tenure_months: int
    monthly_charges: float
    total_charges: float
    contract_type: str
    num_services: int
    support_calls: int


class PredictionResponse(BaseModel):
    """Prediction response"""
    customer_id: str
    churn_probability: float
    churn_risk: str


def load_model():
    """Load the trained model"""
    try:
        model_path = Path(__file__).parent / "churn_model.pkl"
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        logger.info("Model loaded successfully")
        return model
    except FileNotFoundError:
        logger.warning("Model file not found, creating dummy model")
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        X_dummy = np.random.rand(100, 6)
        y_dummy = np.random.randint(0, 2, 100)
        model.fit(X_dummy, y_dummy)
        return model


@app.on_event("startup")
async def startup_event():
    """Load model at startup"""
    global model
    model = load_model()
    logger.info("API startup complete")


def preprocess_features(customer: CustomerFeatures) -> np.ndarray:
    """Preprocess customer features"""
    contract_mapping = {
        "month-to-month": 0,
        "one-year": 1,
        "two-year": 2
    }
    
    if customer.contract_type not in contract_mapping:
        raise ValueError(f"Invalid contract_type: {customer.contract_type}")
    
    contract_encoded = contract_mapping[customer.contract_type]
    
    features = np.array([
        customer.tenure_months,
        customer.monthly_charges,
        customer.total_charges,
        contract_encoded,
        customer.num_services,
        customer.support_calls
    ]).reshape(1, -1)
    
    return features


def calculate_risk_level(probability: float) -> str:
    """Calculate risk level from churn probability"""
    if probability < 0.3:
        return "low"
    elif probability < 0.7:
        return "medium"
    else:
        return "high"


@app.post("/predict", response_model=PredictionResponse)
async def predict_churn(customer: CustomerFeatures):
    """Predict churn probability for a single customer"""
    try:
        features = preprocess_features(customer)
        churn_prob = model.predict_proba(features)[0][1]
        risk_level = calculate_risk_level(churn_prob)
        
        return PredictionResponse(
            customer_id=customer.customer_id,
            churn_probability=float(churn_prob),
            churn_risk=risk_level
        )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "api_key_set": API_KEY != "default-key"
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Churn Prediction API - Containerized",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict",
            "health": "/health"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


