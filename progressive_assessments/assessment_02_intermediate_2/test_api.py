"""
Test script for the Fraud Detection API

Use this to verify your fixes:
1. Start the API: python model_api.py
2. Run this script: python test_api.py

This will help you identify if bugs are fixed.
"""

import requests
import json
from time import time

API_URL = "http://localhost:8000"


def test_single_prediction():
    """Test single transaction prediction"""
    print("\n" + "="*50)
    print("TEST 1: Single Transaction Prediction")
    print("="*50)
    
    # Test with high-value international transaction
    transaction = {
        "transaction_id": "TXN001",
        "amount": 5000.00,  # High amount
        "merchant_category": "online",
        "card_present": False,
        "international": True,
        "hour_of_day": 2,  # Late night
        "days_since_last_transaction": 0.5,
        "num_transactions_24h": 8  # Many transactions
    }
    
    try:
        response = requests.post(f"{API_URL}/predict", json=transaction)
        response.raise_for_status()
        result = response.json()
        
        print(f"✓ Prediction successful!")
        print(f"  Transaction: {result['transaction_id']}")
        print(f"  Amount: ${transaction['amount']:.2f}")
        print(f"  Fraud Probability: {result['fraud_probability']:.2%}")
        print(f"  Risk Level: {result['fraud_risk']}")
        print(f"  Action: {result['recommended_action']}")
        
        # Check cache
        cache_response = requests.get(f"{API_URL}/cache/stats")
        cache_data = cache_response.json()
        print(f"\n  Cache size: {cache_data['cache_size']} entries")
        
        # Logic check for Bug #2
        prob = result['fraud_probability']
        amount = transaction['amount']
        risk = result['fraud_risk']
        
        # High amount + high probability should be very risky
        if amount > 1000 and prob > 0.6 and risk == "low":
            print(f"  ⚠️  WARNING: High amount (${amount}) + high probability ({prob:.2%}) but risk is '{risk}' - check logic!")
        else:
            print(f"  ✓ Risk level calculation looks reasonable")
            
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")


def test_risk_calculation():
    """Test risk calculation logic with different scenarios"""
    print("\n" + "="*50)
    print("TEST 2: Risk Calculation Logic")
    print("="*50)
    
    test_cases = [
        {
            "name": "Low amount, low risk",
            "transaction": {
                "transaction_id": "TXN_LOW",
                "amount": 50.00,
                "merchant_category": "retail",
                "card_present": True,
                "international": False,
                "hour_of_day": 14,
                "days_since_last_transaction": 1.0,
                "num_transactions_24h": 2
            },
            "expected": "Should be low risk"
        },
        {
            "name": "High amount, high risk indicators",
            "transaction": {
                "transaction_id": "TXN_HIGH",
                "amount": 10000.00,  # Very high amount
                "merchant_category": "online",
                "card_present": False,
                "international": True,
                "hour_of_day": 3,
                "days_since_last_transaction": 0.1,
                "num_transactions_24h": 15
            },
            "expected": "Should be high/critical risk"
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTest: {test_case['name']}")
        print(f"  Amount: ${test_case['transaction']['amount']:.2f}")
        print(f"  Expected: {test_case['expected']}")
        
        try:
            response = requests.post(f"{API_URL}/predict", json=test_case['transaction'])
            result = response.json()
            
            print(f"  Got: {result['fraud_risk']} risk, action: {result['recommended_action']}")
            
            # Check if high amounts are treated seriously
            if test_case['transaction']['amount'] > 5000:
                if result['fraud_risk'] in ['low', 'medium']:
                    print(f"  ⚠️  WARNING: Very high amount but only '{result['fraud_risk']}' risk - check calculation!")
                else:
                    print(f"  ✓ High-value transaction properly flagged as risky")
                    
        except Exception as e:
            print(f"  ✗ Test failed: {str(e)}")


def test_input_validation():
    """Test input validation"""
    print("\n" + "="*50)
    print("TEST 3: Input Validation")
    print("="*50)
    
    # Test with negative amount
    print("\nTesting negative transaction amount...")
    invalid_transaction = {
        "transaction_id": "TXN_NEG",
        "amount": -500.00,  # Negative!
        "merchant_category": "online",
        "card_present": False,
        "international": False,
        "hour_of_day": 10,
        "days_since_last_transaction": 1.0,
        "num_transactions_24h": 1
    }
    
    try:
        response = requests.post(f"{API_URL}/predict", json=invalid_transaction)
        result = response.json()
        if response.status_code == 200:
            print(f"  ⚠️  WARNING: Accepts negative amounts - should validate!")
        else:
            print(f"  ✓ Properly validates negative amounts")
    except Exception as e:
        print(f"  ⚠️  WARNING: No validation for negative amounts")
    
    # Test with invalid merchant category
    print("\nTesting invalid merchant category...")
    invalid_category = {
        "transaction_id": "TXN_CAT",
        "amount": 100.00,
        "merchant_category": "invalid-category",  # Invalid!
        "card_present": True,
        "international": False,
        "hour_of_day": 10,
        "days_since_last_transaction": 1.0,
        "num_transactions_24h": 1
    }
    
    try:
        response = requests.post(f"{API_URL}/predict", json=invalid_category)
        result = response.json()
        if response.status_code == 200:
            print(f"  ⚠️  WARNING: Accepts invalid merchant categories - should validate!")
        else:
            print(f"  ✓ Properly validates merchant categories")
    except Exception as e:
        print(f"  ⚠️  WARNING: Should handle invalid categories gracefully")
    
    # Test with invalid hour
    print("\nTesting invalid hour_of_day...")
    invalid_hour = {
        "transaction_id": "TXN_HOUR",
        "amount": 100.00,
        "merchant_category": "retail",
        "card_present": True,
        "international": False,
        "hour_of_day": 25,  # Invalid! Should be 0-23
        "days_since_last_transaction": 1.0,
        "num_transactions_24h": 1
    }
    
    try:
        response = requests.post(f"{API_URL}/predict", json=invalid_hour)
        result = response.json()
        if response.status_code == 200:
            print(f"  ⚠️  WARNING: Accepts hour_of_day > 23 - should validate range!")
        else:
            print(f"  ✓ Properly validates hour range")
    except Exception as e:
        print(f"  ⚠️  WARNING: Should validate hour_of_day range (0-23)")


def test_memory_leak():
    """Test for memory leak (growing cache)"""
    print("\n" + "="*50)
    print("TEST 4: Memory Leak Check")
    print("="*50)
    
    # Clear cache first
    print("\nClearing cache...")
    clear_response = requests.delete(f"{API_URL}/cache/clear")
    print(f"  {clear_response.json()['message']}")
    
    # Check initial cache size
    cache_response = requests.get(f"{API_URL}/cache/stats")
    initial_size = cache_response.json()['cache_size']
    print(f"\nInitial cache size: {initial_size}")
    
    # Make multiple requests
    print(f"\nMaking 20 predictions...")
    for i in range(20):
        transaction = {
            "transaction_id": f"TXN_LEAK_{i:03d}",
            "amount": 100.00 + i,
            "merchant_category": "retail",
            "card_present": True,
            "international": False,
            "hour_of_day": 10,
            "days_since_last_transaction": 1.0,
            "num_transactions_24h": 1
        }
        
        try:
            response = requests.post(f"{API_URL}/predict", json=transaction)
            response.raise_for_status()
        except Exception as e:
            print(f"  ✗ Request {i+1} failed: {str(e)}")
            return
    
    # Check final cache size
    cache_response = requests.get(f"{API_URL}/cache/stats")
    cache_data = cache_response.json()
    final_size = cache_data['cache_size']
    
    print(f"\n✓ All requests completed!")
    print(f"  Initial cache size: {initial_size}")
    print(f"  Final cache size: {final_size}")
    print(f"  Cache growth: +{final_size - initial_size} entries")
    
    if final_size > initial_size + 10:
        print(f"\n  ⚠️  WARNING: Cache is growing unbounded - memory leak!")
        print(f"  ⚠️  In production, this would consume all available memory!")
    else:
        print(f"\n  ✓ Cache is properly managed (not growing)")


def test_batch_efficiency():
    """Test batch prediction efficiency"""
    print("\n" + "="*50)
    print("TEST 5: Batch Processing Efficiency")
    print("="*50)
    
    # Create 30 transactions
    transactions = []
    for i in range(30):
        transactions.append({
            "transaction_id": f"BATCH_{i:03d}",
            "amount": 100.0 + i * 10,
            "merchant_category": ["retail", "online", "restaurant"][i % 3],
            "card_present": i % 2 == 0,
            "international": i % 5 == 0,
            "hour_of_day": (i % 24),
            "days_since_last_transaction": float(i % 7),
            "num_transactions_24h": (i % 10) + 1
        })
    
    try:
        print(f"\nProcessing {len(transactions)} transactions in batch...")
        start_time = time()
        response = requests.post(
            f"{API_URL}/predict/batch",
            json={"transactions": transactions}
        )
        elapsed = time() - start_time
        
        response.raise_for_status()
        result = response.json()
        
        print(f"✓ Batch prediction successful!")
        print(f"  Processed: {len(result['predictions'])} transactions")
        print(f"  Time: {elapsed:.3f} seconds")
        print(f"  Average: {elapsed/len(transactions)*1000:.1f} ms per transaction")
        
        # Check for inefficiency warnings in the output
        print(f"\n  ⚠️  Check the API console output for inefficiency warnings!")
        print(f"  ⚠️  Look for repeated calculations that should be done once.")
        
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  FRAUD DETECTION API - TEST SUITE")
    print("="*70)
    print("\nThis will help you identify bugs in the API.")
    print("Make sure the API is running: python model_api.py")
    print("\nPress Enter to start tests...")
    input()
    
    # Check if API is running
    try:
        response = requests.get(f"{API_URL}/health")
        response.raise_for_status()
        print("\n✓ API is running!\n")
    except Exception as e:
        print(f"\n✗ Cannot connect to API. Make sure it's running on {API_URL}")
        print(f"  Error: {str(e)}\n")
        return
    
    # Run tests
    test_single_prediction()
    test_risk_calculation()
    test_input_validation()
    test_memory_leak()
    test_batch_efficiency()
    
    print("\n" + "="*70)
    print("  TESTS COMPLETED")
    print("="*70)
    print("\nBug Summary:")
    print("1. ⚠️  Memory Leak: Cache grows without limit")
    print("2. ⚠️  Logic Error: High-value transactions not properly risk-assessed")
    print("3. ⚠️  Performance: Repeated calculations in batch processing")
    print("4. ⚠️  Validation: No input validation for amounts, categories, ranges")
    print("\nReview the warnings above and fix the bugs in model_api.py")
    print("\n")


if __name__ == "__main__":
    main()

