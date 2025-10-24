"""
Test script for the Churn Prediction API

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
    """Test single customer prediction"""
    print("\n" + "="*50)
    print("TEST 1: Single Customer Prediction")
    print("="*50)
    
    customer = {
        "customer_id": "CUST001",
        "tenure_months": 12,
        "monthly_charges": 75.50,
        "total_charges": 906.00,
        "contract_type": "month-to-month",
        "num_services": 3,
        "support_calls": 2
    }
    
    try:
        response = requests.post(f"{API_URL}/predict", json=customer)
        response.raise_for_status()
        result = response.json()
        
        print(f"✓ Prediction successful!")
        print(f"  Customer: {result['customer_id']}")
        print(f"  Churn Probability: {result['churn_probability']:.2%}")
        print(f"  Risk Level: {result['churn_risk']}")
        
        # Check if risk level makes sense
        prob = result['churn_probability']
        risk = result['churn_risk']
        
        # Logic check for Bug #2
        if prob > 0.7 and risk != "high":
            print(f"  ⚠️  WARNING: High probability ({prob:.2%}) but risk is '{risk}' - check logic!")
        elif prob < 0.3 and risk != "low":
            print(f"  ⚠️  WARNING: Low probability ({prob:.2%}) but risk is '{risk}' - check logic!")
        else:
            print(f"  ✓ Risk level logic looks correct!")
            
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")


def test_edge_cases():
    """Test edge cases"""
    print("\n" + "="*50)
    print("TEST 2: Edge Case Handling")
    print("="*50)
    
    # Test with invalid contract type
    print("\nTesting invalid contract type...")
    invalid_customer = {
        "customer_id": "CUST002",
        "tenure_months": 6,
        "monthly_charges": 50.00,
        "total_charges": 300.00,
        "contract_type": "invalid-type",  # Invalid!
        "num_services": 2,
        "support_calls": 1
    }
    
    try:
        response = requests.post(f"{API_URL}/predict", json=invalid_customer)
        result = response.json()
        if response.status_code == 500:
            print(f"  ⚠️  WARNING: API crashes on invalid input - needs better validation!")
        else:
            print(f"  ✓ Handled gracefully with proper error")
    except Exception as e:
        print(f"  ⚠️  WARNING: Exception raised - needs better edge case handling: {str(e)}")
    
    # Test with negative values
    print("\nTesting negative values...")
    negative_customer = {
        "customer_id": "CUST003",
        "tenure_months": -5,  # Negative!
        "monthly_charges": -10.00,  # Negative!
        "total_charges": 100.00,
        "contract_type": "one-year",
        "num_services": 2,
        "support_calls": 1
    }
    
    try:
        response = requests.post(f"{API_URL}/predict", json=negative_customer)
        result = response.json()
        if response.status_code == 200:
            print(f"  ⚠️  WARNING: Accepts negative values - should validate!")
        else:
            print(f"  ✓ Properly validates negative values")
    except Exception as e:
        print(f"  ⚠️  WARNING: No validation for negative values")


def test_batch_efficiency():
    """Test batch prediction efficiency"""
    print("\n" + "="*50)
    print("TEST 3: Batch Prediction Efficiency")
    print("="*50)
    
    # Create 50 customers
    customers = []
    for i in range(50):
        customers.append({
            "customer_id": f"CUST{i:03d}",
            "tenure_months": 10 + i,
            "monthly_charges": 50.0 + i,
            "total_charges": 500.0 + i * 10,
            "contract_type": "month-to-month",
            "num_services": 2,
            "support_calls": 1
        })
    
    try:
        start_time = time()
        response = requests.post(
            f"{API_URL}/predict/batch",
            json={"customers": customers}
        )
        elapsed = time() - start_time
        
        response.raise_for_status()
        result = response.json()
        
        print(f"✓ Batch prediction successful!")
        print(f"  Processed: {len(result['predictions'])} customers")
        print(f"  Time: {elapsed:.2f} seconds")
        print(f"  Average: {elapsed/len(customers)*1000:.1f} ms per customer")
        
        if elapsed > 2.0:
            print(f"  ⚠️  WARNING: Batch processing seems slow - check for inefficiencies!")
        else:
            print(f"  ✓ Batch processing is efficient!")
            
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")


def test_memory():
    """Test for memory leaks (multiple requests)"""
    print("\n" + "="*50)
    print("TEST 4: Memory Leak Check")
    print("="*50)
    
    customer = {
        "customer_id": "CUST_TEST",
        "tenure_months": 12,
        "monthly_charges": 75.50,
        "total_charges": 906.00,
        "contract_type": "month-to-month",
        "num_services": 3,
        "support_calls": 2
    }
    
    print("\nMaking 10 consecutive requests...")
    start_time = time()
    
    for i in range(10):
        try:
            response = requests.post(f"{API_URL}/predict", json=customer)
            response.raise_for_status()
        except Exception as e:
            print(f"✗ Request {i+1} failed: {str(e)}")
            return
    
    elapsed = time() - start_time
    avg_time = elapsed / 10
    
    print(f"✓ All requests completed!")
    print(f"  Total time: {elapsed:.2f} seconds")
    print(f"  Average: {avg_time*1000:.0f} ms per request")
    
    if avg_time > 0.5:
        print(f"  ⚠️  WARNING: Requests are slow - possible memory leak from reloading model!")
    else:
        print(f"  ✓ Request time looks reasonable!")


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  CHURN PREDICTION API - TEST SUITE")
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
    test_edge_cases()
    test_batch_efficiency()
    test_memory()
    
    print("\n" + "="*70)
    print("  TESTS COMPLETED")
    print("="*70)
    print("\nReview the warnings above to identify remaining bugs.")
    print("\n")


if __name__ == "__main__":
    main()


