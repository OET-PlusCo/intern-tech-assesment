"""
Assessment #2 Alternative: Production ML API (Intermediate)

This FastAPI application serves a fraud detection model for transaction monitoring.
Your task: Find and fix all bugs to make it production-ready.

Time: 10 minutes

Expected outcome:
- API runs without errors
- Predictions are accurate
- Code follows production best practices
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import pandas as pd
import numpy as np
import pickle
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Fraud Detection API")

# Model path
MODEL_PATH = Path(__file__).parent / "fraud_model.pkl"

# Global prediction cache - stores all predictions for "audit purposes"
PREDICTION_CACHE: Dict[str, dict] = {}


class TransactionFeatures(BaseModel):
    """Transaction features for fraud detection"""
    transaction_id: str
    amount: float
    merchant_category: str  # "retail", "online", "restaurant", "travel", "other"
    card_present: bool
    international: bool
    hour_of_day: int  # 0-23
    days_since_last_transaction: float
    num_transactions_24h: int


class FraudPredictionResponse(BaseModel):
    """Fraud prediction response"""
    transaction_id: str
    fraud_probability: float
    fraud_risk: str  # "low", "medium", "high", "critical"
    recommended_action: str  # "approve", "review", "decline"


class BatchPredictionRequest(BaseModel):
    """Batch prediction request"""
    transactions: List[TransactionFeatures]


# Load model once at startup
def load_model():
    """Load the trained fraud detection model"""
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
        X_dummy = np.random.rand(100, 7)
        y_dummy = np.random.randint(0, 2, 100)
        model.fit(X_dummy, y_dummy)
        logger.info("Using dummy model for assessment")
        return model


# Initialize model at module level
model = load_model()


def preprocess_features(transaction: TransactionFeatures) -> np.ndarray:
    """Preprocess transaction features for model input"""
    # Encode merchant category
    category_mapping = {
        "retail": 0,
        "online": 1,
        "restaurant": 2,
        "travel": 3,
        "other": 4
    }
    
    # BUG #4: No validation - accepts any category, allows negative amounts
    category_encoded = category_mapping.get(transaction.merchant_category, 4)
    
    features = np.array([
        transaction.amount,
        category_encoded,
        1 if transaction.card_present else 0,
        1 if transaction.international else 0,
        transaction.hour_of_day,
        transaction.days_since_last_transaction,
        transaction.num_transactions_24h
    ]).reshape(1, -1)
    
    return features


def calculate_fraud_risk_level(probability: float, amount: float) -> str:
    """
    Calculate fraud risk level from probability and transaction amount.
    Higher amounts should increase risk severity.
    """
    # BUG #2: Logic Error - Wrong aggregation/formula
    # Should consider BOTH probability AND amount, but uses wrong logic
    base_score = probability * 10
    amount_factor = amount / 100  # Wrong: divides when should multiply for high amounts
    
    # This makes high-value transactions appear LESS risky!
    risk_score = base_score - amount_factor  # BUG: Subtracts instead of adding weight
    
    print(f"[DEBUG] Prob: {probability:.2f}, Amount: ${amount:.2f}, Risk Score: {risk_score:.2f}")
    
    if risk_score < 2:
        return "low"
    elif risk_score < 5:
        return "medium"
    elif risk_score < 7:
        return "high"
    else:
        return "critical"


def determine_action(risk_level: str) -> str:
    """Determine recommended action based on risk level"""
    action_mapping = {
        "low": "approve",
        "medium": "review",
        "high": "decline",
        "critical": "decline"
    }
    return action_mapping.get(risk_level, "review")


@app.post("/predict", response_model=FraudPredictionResponse)
async def predict_fraud(transaction: TransactionFeatures):
    """Predict fraud probability for a single transaction"""
    try:
        # BUG #1: Growing cache memory leak
        # Cache is never cleared, grows indefinitely
        print(f"[WARNING] Cache size: {len(PREDICTION_CACHE)} entries (growing with each request!)")
        
        features = preprocess_features(transaction)
        
        fraud_prob = model.predict_proba(features)[0][1]
        risk_level = calculate_fraud_risk_level(fraud_prob, transaction.amount)
        action = determine_action(risk_level)
        
        response = FraudPredictionResponse(
            transaction_id=transaction.transaction_id,
            fraud_probability=float(fraud_prob),
            fraud_risk=risk_level,
            recommended_action=action
        )
        
        # BUG #1: Store prediction in cache that never gets cleared
        PREDICTION_CACHE[transaction.transaction_id] = {
            "timestamp": datetime.now().isoformat(),
            "features": transaction.dict(),
            "prediction": response.dict(),
            "model_version": "v1.0"
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/batch")
async def predict_batch(request: BatchPredictionRequest):
    """Predict fraud for multiple transactions"""
    try:
        print(f"[WARNING] Processing {len(request.transactions)} transactions...")
        
        results = []
        
        # BUG #3: Inefficient - recalculates merchant category stats in each iteration
        for transaction in request.transactions:
            # BUG #3: This computation should be done ONCE, not per transaction
            merchant_categories = [t.merchant_category for t in request.transactions]
            category_counts = {}
            for cat in merchant_categories:
                category_counts[cat] = category_counts.get(cat, 0) + 1
            
            print(f"[INEFFICIENT] Recalculated category stats {len(results) + 1} times: {category_counts}")
            
            features = preprocess_features(transaction)
            fraud_prob = model.predict_proba(features)[0][1]
            risk_level = calculate_fraud_risk_level(fraud_prob, transaction.amount)
            action = determine_action(risk_level)
            
            response = FraudPredictionResponse(
                transaction_id=transaction.transaction_id,
                fraud_probability=float(fraud_prob),
                fraud_risk=risk_level,
                recommended_action=action
            )
            
            # BUG #1: Cache grows with each transaction
            PREDICTION_CACHE[transaction.transaction_id] = {
                "timestamp": datetime.now().isoformat(),
                "features": transaction.dict(),
                "prediction": response.dict(),
                "model_version": "v1.0"
            }
            
            results.append(response)
        
        print(f"[INFO] Processed {len(results)} transactions. Cache now has {len(PREDICTION_CACHE)} entries.")
        
        return {"predictions": results}
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cache/stats")
async def cache_stats():
    """Get cache statistics (reveals the memory leak)"""
    return {
        "cache_size": len(PREDICTION_CACHE),
        "warning": "Cache is never cleared - memory leak!" if len(PREDICTION_CACHE) > 10 else "OK"
    }


@app.delete("/cache/clear")
async def clear_cache():
    """Clear the prediction cache"""
    global PREDICTION_CACHE
    cache_size = len(PREDICTION_CACHE)
    PREDICTION_CACHE = {}
    return {
        "message": f"Cleared {cache_size} cached predictions",
        "new_size": len(PREDICTION_CACHE)
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "cache_size": len(PREDICTION_CACHE)
    }


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Fraud Detection API",
        "endpoints": {
            "predict": "/predict",
            "batch_predict": "/predict/batch",
            "cache_stats": "/cache/stats",
            "clear_cache": "/cache/clear",
            "health": "/health"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

