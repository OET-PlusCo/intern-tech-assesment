#!/usr/bin/env python3
"""
Setup script for Data Science Intern Assessment
This script prepares everything needed for the technical assessment
"""

import os
import urllib.request
import pandas as pd
import sys

def setup_assessment_environment():
    """
    Set up the assessment environment
    """
    print("Setting up Data Science Intern Assessment Environment...")
    print("=" * 60)
    
    # Create assessment directory structure
    directories = [
        'datasets',
        'candidate_work',
        'results'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created directory: {directory}")
        else:
            print(f"✓ Directory already exists: {directory}")
    
    print("\n" + "=" * 60)
    print("DATASET DOWNLOAD INSTRUCTIONS")
    print("=" * 60)
    
    print("\nOption 1: Telco Customer Churn (Recommended)")
    print("-" * 50)
    print("1. Go to: https://www.kaggle.com/datasets/blastchar/telco-customer-churn")
    print("2. Download 'WA_Fn-UseC_-Telco-Customer-Churn.csv'")
    print("3. Save it as 'datasets/telco_churn.csv'")
    print("4. Dataset size: ~7,000 rows, 21 columns")
    print("5. Perfect for 40-minute assessment")
    
    print("\nOption 2: House Prices")
    print("-" * 50)
    print("1. Go to: https://www.kaggle.com/c/house-prices-advanced-regression-techniques")
    print("2. Download 'train.csv'")
    print("3. Save it as 'datasets/house_prices.csv'")
    print("4. More complex - use for advanced candidates only")
    
    print("\nOption 3: Wine Quality (Hugging Face)")
    print("-" * 50)
    print("1. Use: datasets library from Hugging Face")
    print("2. Code: from datasets import load_dataset")
    print("3. dataset = load_dataset('mstz/wine_quality')")
    print("4. Simpler dataset - good for basic assessment")
    
    # Create sample data if no real dataset available
    create_sample_dataset()
    
    print("\n" + "=" * 60)
    print("ENVIRONMENT CHECK")
    print("=" * 60)
    
    # Check required packages
    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 
        'scikit-learn', 'jupyter'
    ]
    
    print("\nChecking required packages...")
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nTo install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
    
    print("\n" + "=" * 60)
    print("ASSESSMENT FILES CREATED")
    print("=" * 60)
    
    file_structure = """
    inter-tech-assessment/
    ├── data_science_intern_assessment.md    # Main assessment guide
    ├── sample_solution_notebook.py          # Reference solution
    ├── setup_assessment.py                  # This setup script
    ├── datasets/                           # Data files go here
    │   └── sample_telco_data.csv           # Sample dataset created
    ├── candidate_work/                     # Candidate's work folder
    └── results/                           # Assessment results
    """
    
    print(file_structure)
    
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("1. Download your preferred dataset (Option 1 recommended)")
    print("2. Review 'data_science_intern_assessment.md'")
    print("3. Run 'sample_solution_notebook.py' to see expected approach")
    print("4. Set up video call environment for live coding")
    print("5. Prepare backup datasets in case of technical issues")
    
    print("\n✓ Assessment environment setup complete!")

def create_sample_dataset():
    """
    Create a sample dataset for testing if no real dataset is available
    """
    import numpy as np
    
    print("\nCreating sample dataset for testing...")
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate sample data similar to Telco Churn
    n_samples = 2000
    
    # Customer demographics
    gender = np.random.choice(['Male', 'Female'], n_samples)
    senior_citizen = np.random.choice([0, 1], n_samples, p=[0.8, 0.2])
    partner = np.random.choice(['Yes', 'No'], n_samples)
    dependents = np.random.choice(['Yes', 'No'], n_samples, p=[0.3, 0.7])
    
    # Account information
    tenure = np.random.exponential(24, n_samples).astype(int)
    tenure = np.clip(tenure, 0, 72)  # Cap at 72 months
    
    contract = np.random.choice(['Month-to-month', 'One year', 'Two year'], 
                               n_samples, p=[0.5, 0.3, 0.2])
    paperless_billing = np.random.choice(['Yes', 'No'], n_samples, p=[0.6, 0.4])
    payment_method = np.random.choice([
        'Electronic check', 'Mailed check', 'Bank transfer (automatic)', 
        'Credit card (automatic)'
    ], n_samples)
    
    # Services
    phone_service = np.random.choice(['Yes', 'No'], n_samples, p=[0.9, 0.1])
    internet_service = np.random.choice(['DSL', 'Fiber optic', 'No'], 
                                       n_samples, p=[0.4, 0.4, 0.2])
    
    # Charges (with some logic)
    monthly_charges = np.random.normal(65, 20, n_samples)
    monthly_charges = np.clip(monthly_charges, 18.25, 118.75)
    
    total_charges = tenure * monthly_charges + np.random.normal(0, 100, n_samples)
    total_charges = np.clip(total_charges, 0, None)
    
    # Target variable (churn) - create some logical relationships
    churn_prob = 0.2  # base probability
    
    # Increase churn probability based on features
    churn_prob_individual = np.full(n_samples, churn_prob)
    churn_prob_individual[contract == 'Month-to-month'] += 0.2
    churn_prob_individual[tenure < 12] += 0.25
    churn_prob_individual[monthly_charges > 80] += 0.15
    churn_prob_individual[senior_citizen == 1] += 0.1
    
    churn_prob_individual = np.clip(churn_prob_individual, 0, 1)
    churn = np.random.binomial(1, churn_prob_individual, n_samples)
    churn = np.where(churn == 1, 'Yes', 'No')
    
    # Create DataFrame
    sample_data = pd.DataFrame({
        'customerID': [f'CUST_{i:04d}' for i in range(n_samples)],
        'gender': gender,
        'SeniorCitizen': senior_citizen,
        'Partner': partner,
        'Dependents': dependents,
        'tenure': tenure,
        'PhoneService': phone_service,
        'InternetService': internet_service,
        'Contract': contract,
        'PaperlessBilling': paperless_billing,
        'PaymentMethod': payment_method,
        'MonthlyCharges': np.round(monthly_charges, 2),
        'TotalCharges': np.round(total_charges, 2),
        'Churn': churn
    })
    
    # Add some missing values to make it more realistic
    missing_indices = np.random.choice(n_samples, size=int(0.001 * n_samples), replace=False)
    sample_data.loc[missing_indices, 'TotalCharges'] = ' '  # Common issue in real dataset
    
    # Save sample dataset
    sample_data.to_csv('datasets/sample_telco_data.csv', index=False)
    print(f"✓ Created sample dataset: datasets/sample_telco_data.csv")
    print(f"  - {n_samples} samples, {len(sample_data.columns)} features")
    print(f"  - Churn rate: {(sample_data['Churn'] == 'Yes').mean():.1%}")
    
    return sample_data

def validate_dataset(file_path):
    """
    Validate that a dataset is suitable for the assessment
    """
    try:
        df = pd.read_csv(file_path)
        
        print(f"\nDataset validation: {file_path}")
        print("-" * 40)
        print(f"Shape: {df.shape}")
        print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
        
        # Check if suitable for 40-minute assessment
        if df.shape[0] > 50000:
            print("⚠️  Large dataset - might be challenging for 40-minute session")
        elif df.shape[0] < 500:
            print("⚠️  Small dataset - might be too simple")
        else:
            print("✓ Good size for assessment")
        
        if df.shape[1] > 50:
            print("⚠️  Many features - consider feature selection guidance")
        elif df.shape[1] < 5:
            print("⚠️  Few features - might limit analysis opportunities")
        else:
            print("✓ Good number of features")
        
        # Check data types
        print(f"\nData types:")
        print(f"- Numerical: {df.select_dtypes(include=['number']).shape[1]}")
        print(f"- Categorical: {df.select_dtypes(include=['object']).shape[1]}")
        
        # Check missing values
        missing_pct = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
        print(f"- Missing values: {missing_pct:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Error validating dataset: {e}")
        return False

if __name__ == '__main__':
    setup_assessment_environment()
    
    # If sample dataset was created, validate it
    if os.path.exists('datasets/sample_telco_data.csv'):
        validate_dataset('datasets/sample_telco_data.csv') 