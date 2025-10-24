# Assessment #2: Production ML API (Intermediate)

## 📋 Overview
**Time**: 10 minutes  
**Difficulty**: Intermediate  
**Type**: Debugging production ML code

## 🎯 Objective
Fix bugs in a FastAPI application that serves a churn prediction model. The code has production issues that prevent it from being deployment-ready.

**Important**: Most bugs have multiple valid solutions - choose your preferred approach and explain your reasoning!

## 🐛 What to Find
- **2 Critical bugs**: Cause major production issues (memory leaks, wrong results)
- **2 Subtle bugs**: Work but violate best practices (inefficiency, missing validations)

## 📂 Files
- `model_api.py` - FastAPI application (has bugs - **this is what you fix**)
- `test_api.py` - Test script to verify your fixes
- `sample_requests.json` - Example API requests
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

### Example 1: Single Customer Prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST001",
    "tenure_months": 24,
    "monthly_charges": 85.50,
    "total_charges": 2052.00,
    "contract_type": "two-year",
    "num_services": 5,
    "support_calls": 1
  }'
```

### Example 2: Month-to-Month Customer
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST002",
    "tenure_months": 12,
    "monthly_charges": 75.50,
    "total_charges": 906.00,
    "contract_type": "month-to-month",
    "num_services": 3,
    "support_calls": 2
  }'
```

### Example 3: New Customer
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST003",
    "tenure_months": 1,
    "monthly_charges": 150.00,
    "total_charges": 150.00,
    "contract_type": "month-to-month",
    "num_services": 10,
    "support_calls": 15
  }'
```

### Example 4: One-Year Contract Customer
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST004",
    "tenure_months": 6,
    "monthly_charges": 65.00,
    "total_charges": 390.00,
    "contract_type": "one-year",
    "num_services": 2,
    "support_calls": 3
  }'
```

### Example 5: Batch Prediction
```bash
curl -X POST http://localhost:8000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "customers": [
      {
        "customer_id": "BATCH001",
        "tenure_months": 12,
        "monthly_charges": 75.50,
        "total_charges": 906.00,
        "contract_type": "month-to-month",
        "num_services": 3,
        "support_calls": 2
      },
      {
        "customer_id": "BATCH002",
        "tenure_months": 24,
        "monthly_charges": 85.50,
        "total_charges": 2052.00,
        "contract_type": "two-year",
        "num_services": 5,
        "support_calls": 1
      },
      {
        "customer_id": "BATCH003",
        "tenure_months": 6,
        "monthly_charges": 65.00,
        "total_charges": 390.00,
        "contract_type": "one-year",
        "num_services": 2,
        "support_calls": 3
      }
    ]
  }'
```

### Interactive Documentation
Open in your browser for an interactive API interface:
```
http://localhost:8000/docs
```

Good luck! 🚀


