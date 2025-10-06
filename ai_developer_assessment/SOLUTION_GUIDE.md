# Solution Guide - Debugging Exercise

## Bugs in `buggy_model_api.py`

This guide lists all intentional bugs and what they test. Use this to evaluate the candidate's debugging skills.

---

## Critical Bugs (Must Find)

### 🐛 Bug #1: Typo in Import Statement
**Line 7**: `from pydette import BaseModel`

**Issue**: Should be `from pydantic import BaseModel` (not "pydette")

**Impact**: Code won't run at all - ImportError

**Tests**: 
- Attention to detail
- Python basics
- Whether they try to run the code

**Expected Fix**:
```python
from pydantic import BaseModel
```

---

### 🐛 Bug #2: Unsafe File Loading
**Lines 14-15**: Model and scaler files loaded without error handling

**Issue**: 
- Files may not exist
- No `rb` mode error handling
- Should use context manager or check file existence
- Vulnerable to pickle exploits (security concern)

**Impact**: Code crashes on startup if files missing

**Tests**:
- Production readiness mindset
- Error handling awareness
- Security awareness (bonus)

**Expected Fix**:
```python
import os

MODEL_PATH = os.getenv("MODEL_PATH", "churn_model.pkl")
SCALER_PATH = os.getenv("SCALER_PATH", "scaler.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
if not os.path.exists(SCALER_PATH):
    raise FileNotFoundError(f"Scaler file not found: {SCALER_PATH}")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)
with open(SCALER_PATH, "rb") as f:
    scaler = pickle.load(f)
```

---

### 🐛 Bug #3: Training/Serving Skew - Feature Mismatch
**Lines 49-50**: One-hot encoding in production doesn't match training

**Issue**: 
- `pd.get_dummies()` creates different columns based on values seen
- If production data has different categories than training, features won't match
- Column order might differ
- Missing categories will be absent

**Impact**: Model receives wrong features → bad predictions or crashes

**Tests**:
- Understanding of ML production issues
- Training/serving consistency
- This is a CLASSIC production ML bug

**Expected Discussion**:
- Should save category mappings from training
- Use scikit-learn's `OneHotEncoder` with saved categories
- Or maintain a feature alignment function
- Need to handle unknown categories

**Expected Fix**:
```python
# Should have a predefined set of columns from training
TRAINING_COLUMNS = [
    'tenure', 'monthly_charges', 'total_charges',
    'contract_type_Month-to-month', 'contract_type_One year',
    'contract_type_Two year', 'payment_method_Bank transfer',
    # ... all columns from training
]

# After encoding
df_encoded = pd.get_dummies(df, columns=["contract_type", "payment_method", "internet_service"])

# Align with training columns
for col in TRAINING_COLUMNS:
    if col not in df_encoded.columns:
        df_encoded[col] = 0
df_encoded = df_encoded[TRAINING_COLUMNS]
```

---

### 🐛 Bug #4: Data Type Conversion Without Validation
**Line 42**: `total_charges` converted from string to float without validation

**Issue**:
- `total_charges` is a string in input
- Might contain " ", "N/A", or other non-numeric values
- Will crash with ValueError

**Impact**: API crashes on invalid input

**Tests**:
- Data validation awareness
- Input sanitization
- Real-world data messiness

**Expected Fix**:
```python
try:
    total_charges = float(data["total_charges"])
except ValueError:
    raise HTTPException(
        status_code=400, 
        detail=f"Invalid total_charges value: {data['total_charges']}"
    )
```

Or use Pydantic validation:
```python
class CustomerData(BaseModel):
    customer_id: str
    tenure: int
    monthly_charges: float
    total_charges: float  # Change from str to float, Pydantic will validate
    # ... other fields
```

---

## Important Bugs (Good to Find)

### 🐛 Bug #5: Inefficient Batch Prediction
**Lines 65-70**: Batch endpoint calls single prediction in a loop

**Issue**:
- Inefficient: makes N model calls instead of 1 batch call
- Defeats the purpose of batch prediction
- High latency for large batches

**Impact**: Poor performance, high latency

**Tests**:
- Performance awareness
- Understanding of ML inference optimization

**Expected Fix**:
```python
@app.post("/predict_batch")
async def predict_batch(customers: List[CustomerData]):
    """Predict churn for multiple customers efficiently"""
    # Collect all data
    data_list = [customer.dict() for customer in customers]
    
    # Process as batch DataFrame
    df = pd.DataFrame(data_list)
    
    # ... process entire DataFrame at once
    
    predictions = model.predict_proba(df_processed)
    
    results = [
        {
            "customer_id": customers[i].customer_id,
            "churn_probability": float(predictions[i][1]),
            "churn_prediction": "Yes" if predictions[i][1] > 0.5 else "No"
        }
        for i in range(len(customers))
    ]
    
    return {"predictions": results}
```

---

### 🐛 Bug #6: Poor Error Handling
**Lines 58-60**: Generic exception handling loses information

**Issue**:
- Catches all exceptions with generic message
- Doesn't differentiate between error types
- Hard to debug production issues
- Logging happens but response is unhelpful

**Impact**: Poor debugging experience, unclear errors

**Tests**:
- Production debugging mindset
- API design quality

**Expected Fix**:
```python
except ValueError as e:
    logging.error(f"Validation error for customer {data['customer_id']}: {str(e)}")
    raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
except Exception as e:
    logging.error(f"Prediction error for customer {data['customer_id']}: {str(e)}", exc_info=True)
    raise HTTPException(status_code=500, detail="Internal prediction error")
```

---

### 🐛 Bug #7: Logging Not Configured
**Line 60**: Uses `logging.error()` but logging is never configured

**Issue**:
- Logging module imported but not configured
- Logs might not appear or go to wrong destination
- No log level, format, or handlers set

**Impact**: Missing logs in production

**Tests**:
- Observability awareness
- Production best practices

**Expected Fix**:
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Then use logger instead of logging
logger.error(f"Prediction error: {str(e)}")
```

---

## Nice-to-Have Observations (Senior Level)

### 🔍 Observation #8: Missing Health Check Depth
**Lines 73-76**: Health check doesn't verify model is loaded

**Issue**:
- Health check only verifies API is running
- Doesn't check if model/scaler are actually loaded
- Kubernetes/load balancers can't detect if model is broken

**Tests**:
- Production deployment experience
- Understanding of liveness vs. readiness probes

**Expected Enhancement**:
```python
@app.get("/health")
async def health_check():
    """Check if the service and model are ready"""
    try:
        # Verify model is loaded and can make predictions
        assert model is not None, "Model not loaded"
        assert scaler is not None, "Scaler not loaded"
        return {"status": "healthy", "model_loaded": True}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")
```

---

## Other Potential Improvements (Bonus Points)

1. **Input Validation**: Add more validation in Pydantic model
   ```python
   class CustomerData(BaseModel):
       tenure: int = Field(ge=0, description="Tenure in months")
       monthly_charges: float = Field(gt=0)
       # ... etc
   ```

2. **Request ID for Tracing**: Add request ID for debugging
   ```python
   import uuid
   request_id = str(uuid.uuid4())
   logger.info(f"Request {request_id}: Processing prediction")
   ```

3. **Caching**: Cache predictions for identical requests

4. **Rate Limiting**: Protect API from abuse

5. **Async Model Loading**: Load model asynchronously on startup

6. **Metrics**: Add Prometheus metrics for monitoring

7. **API Versioning**: Version the API endpoints (`/v1/predict`)

---

## Evaluation Criteria

### Score Breakdown

| Bugs Found | Score | Level |
|------------|-------|-------|
| Bug #1 (Import) | 5 pts | Must find (basic) |
| Bug #2 (File handling) | 5 pts | Must find |
| Bug #3 (Feature mismatch) | 10 pts | **Most important** - tests ML production knowledge |
| Bug #4 (Data validation) | 5 pts | Important |
| Bug #5 (Batch inefficiency) | 3 pts | Good to find |
| Bug #6 (Error handling) | 3 pts | Good to find |
| Bug #7 (Logging config) | 2 pts | Nice to have |
| Bug #8 (Health check) | 2 pts | Senior level |

**Total**: 35 points possible

### Rating Scale
- **30-35 pts**: Exceptional - Deep production ML experience
- **20-29 pts**: Strong - Solid production awareness
- **15-19 pts**: Adequate - Meets minimum requirements
- **10-14 pts**: Weak - Significant gaps
- **<10 pts**: Insufficient - Does not meet requirements

---

## Candidate Behavior Assessment

### Green Flags ✅
- Asks about the production environment
- Questions about input data format/validation
- Mentions testing strategy
- Discusses monitoring and alerting
- Explains trade-offs in their fixes
- Prioritizes bugs by severity
- Thinks about end-users and business impact

### Red Flags 🚩
- Fixes syntax errors but misses logic bugs
- Doesn't run or test the code mentally
- Doesn't ask any clarifying questions
- Makes assumptions without stating them
- Gives up after finding one bug
- Can't explain the impact of bugs
- Blames the original developer excessively

---

## Follow-Up Questions (If Time)

After debugging, ask:

1. **"How would you test your fixes?"**
   - Unit tests, integration tests, load tests
   - Test data quality issues specifically

2. **"What monitoring would you add to catch these issues in production?"**
   - Feature distribution monitoring
   - Prediction distribution tracking
   - Error rate alerts
   - Latency monitoring

3. **"If you had to prioritize fixing these bugs with limited time, what order would you choose?"**
   - Tests prioritization skills and business thinking

