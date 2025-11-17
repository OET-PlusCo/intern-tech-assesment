# Assessment #2 Alternative: Production ML API (Intermediate)

## 📋 Overview
**Time**: 10 minutes  
**Difficulty**: Intermediate  
**Type**: Debugging production ML code

## 🎯 Objective
Fix bugs in a FastAPI application that serves a fraud detection model for transaction monitoring. The code has production issues that prevent it from being deployment-ready.

**Important**: Most bugs have multiple valid solutions - choose your preferred approach and explain your reasoning!

## 🐛 What to Find
- **2 Critical bugs**: Cause major production issues (memory leaks, wrong results)
- **2 Subtle bugs**: Work but violate best practices (inefficiency, missing validations)

## 📂 Files
- `model_api.py` - FastAPI application (has bugs - **this is what you fix**)
- `test_api.py` - Test script to verify your fixes
- `requirements.txt` - Dependencies

## 🚀 How to Complete This Assessment

### Step 1: Review the Code (2-3 min)
```bash
# Open and read model_api.py
# Identify potential issues before running
```

### Step 2: Run the API (1 min)
```bash
# Install dependencies
pip install -r requirements.txt

# Start the API
python model_api.py
```

The API will run on `http://localhost:8000`

### Step 3: Test & Debug (5-6 min)
```bash
# In another terminal, run tests
python test_api.py
```

The test script will help you identify bugs:
- ✓ = Working correctly
- ⚠️ = Warning/issue detected

### Step 4: Fix Bugs (remaining time)
Edit `model_api.py` to fix all issues. Rerun tests to verify.

## 💡 Tips
- Read error messages and warnings carefully
- Check the API console output for hints
- Think about production best practices
- Consider: memory, efficiency, edge cases, correctness
- Some bugs are obvious when you run it, others require code review
- **Multiple solutions exist** - focus on explaining WHY you chose your approach

## ✅ Success Criteria
- API runs without crashing
- Predictions are logically correct
- No memory leaks
- Handles edge cases properly
- Batch processing is efficient
- Can explain why you chose your solution approach over alternatives

## 📊 What This Tests
- Production ML knowledge
- FastAPI/API design
- Memory management
- Code efficiency
- Error handling
- Data validation
- Security awareness

## 🔍 Categories of Bugs

### Critical (Must Fix)
These cause serious production problems:
- Memory leaks
- Logic errors producing wrong results

### Subtle (Best Practices)
These work but aren't production-ready:
- Inefficient code patterns
- Missing input validation

## 📝 Manual Testing Examples

You can also test manually with these examples:

### Health Check
```bash
curl http://localhost:8000/health
```

### Example 1: Low-Risk Transaction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "TXN001",
    "amount": 50.00,
    "merchant_category": "retail",
    "card_present": true,
    "international": false,
    "hour_of_day": 14,
    "days_since_last_transaction": 1.0,
    "num_transactions_24h": 2
  }'
```

### Example 2: High-Risk Transaction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "TXN002",
    "amount": 10000.00,
    "merchant_category": "online",
    "card_present": false,
    "international": true,
    "hour_of_day": 3,
    "days_since_last_transaction": 0.1,
    "num_transactions_24h": 15
  }'
```

### Example 3: International Transaction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "TXN003",
    "amount": 500.00,
    "merchant_category": "travel",
    "card_present": false,
    "international": true,
    "hour_of_day": 22,
    "days_since_last_transaction": 5.0,
    "num_transactions_24h": 1
  }'
```

### Example 4: Batch Prediction
```bash
curl -X POST http://localhost:8000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "transactions": [
      {
        "transaction_id": "BATCH001",
        "amount": 100.00,
        "merchant_category": "retail",
        "card_present": true,
        "international": false,
        "hour_of_day": 10,
        "days_since_last_transaction": 1.0,
        "num_transactions_24h": 1
      },
      {
        "transaction_id": "BATCH002",
        "amount": 5000.00,
        "merchant_category": "online",
        "card_present": false,
        "international": true,
        "hour_of_day": 2,
        "days_since_last_transaction": 0.5,
        "num_transactions_24h": 8
      }
    ]
  }'
```

### Check Cache Stats (Helpful for debugging)
```bash
curl http://localhost:8000/cache/stats
```

### Clear Cache
```bash
curl -X DELETE http://localhost:8000/cache/clear
```

### Interactive Documentation
Open in your browser for an interactive API interface:
```
http://localhost:8000/docs
```

Good luck! 🚀

