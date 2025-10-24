"""
Assessment #2: Production ML API (Intermediate)

This FastAPI application serves a customer churn prediction model.
Your task: Find and fix all bugs to make it production-ready.

Time: 10 minutes

Expected outcome:
- API runs without errors
- Predictions are accurate
- Code follows production best practices
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np
import pickle
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Churn Prediction API")

# Model path
MODEL_PATH = Path(__file__).parent / "churn_model.pkl"


class CustomerFeatures(BaseModel):
    """Customer features for churn prediction"""
    customer_id: str
    tenure_months: int
    monthly_charges: float
    total_charges: float
    contract_type: str  # "month-to-month", "one-year", "two-year"
    num_services: int
    support_calls: int
    

class PredictionResponse(BaseModel):
    """Prediction response"""
    customer_id: str
    churn_probability: float
    churn_risk: str  # "low", "medium", "high"


class BatchPredictionRequest(BaseModel):
    """Batch prediction request"""
    customers: List[CustomerFeatures]


MODEL_LOAD_COUNTER = 0

def load_model():
    """Load the trained model"""
    global MODEL_LOAD_COUNTER
    MODEL_LOAD_COUNTER += 1
    print(f"[WARNING] Model loaded {MODEL_LOAD_COUNTER} times! This is a memory leak!")
    logger.warning(f"Model load count: {MODEL_LOAD_COUNTER}")
    
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        logger.info("Model loaded successfully")
        return model
    except FileNotFoundError:
        logger.error(f"Model file not found at {MODEL_PATH}")
        # For this assessment, we'll create a dummy model
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        # Dummy training
        X_dummy = np.random.rand(100, 6)
        y_dummy = np.random.randint(0, 2, 100)
        model.fit(X_dummy, y_dummy)
        logger.info("Using dummy model for assessment")
        return model


def preprocess_features(customer: CustomerFeatures) -> np.ndarray:
    """Preprocess customer features for model input"""
    contract_mapping = {
        "month-to-month": 0,
        "one-year": 1,
        "two-year": 2
    }
    
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
        return "high"
    elif probability < 0.7:
        return "medium"
    else:
        if probability > 0.9:
            print(f"[CRITICAL ERROR] Probability {probability:.2f} is very high but returning 'low' risk!")
            raise ValueError(f"Logic error detected! Probability {probability:.2f} > 0.9 but would return 'low' risk. This is backwards!")
        return "low"


@app.post("/predict", response_model=PredictionResponse)
async def predict_churn(customer: CustomerFeatures):
    """Predict churn probability for a single customer"""
    try:
        model = load_model()
        
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


@app.post("/predict/batch")
async def predict_batch(request: BatchPredictionRequest):
    """Predict churn for multiple customers"""
    try:
        model = load_model()
        
        results = []
        
        import time
        print(f"[WARNING] Processing {len(request.customers)} customers one-by-one (SLOW!)")
        
        for customer in request.customers:
            time.sleep(0.1)
            
            features = preprocess_features(customer)
            churn_prob = model.predict_proba(features)[0][1]
            risk_level = calculate_risk_level(churn_prob)
            
            results.append(PredictionResponse(
                customer_id=customer.customer_id,
                churn_probability=float(churn_prob),
                churn_risk=risk_level
            ))
        
        print(f"[INFO] Batch took extra time due to processing one-by-one instead of vectorized batch!")
        return {"predictions": results}
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": True
    }


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Churn Prediction API",
        "endpoints": {
            "predict": "/predict",
            "batch_predict": "/predict/batch",
            "health": "/health"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


