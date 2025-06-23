# Sample Solution: Data Science Intern Assessment
# Dataset: Telco Customer Churn
# This demonstrates what a strong candidate's approach might look like

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# ================================================================================
# PHASE 1: Data Exploration & Understanding (15 minutes)
# ================================================================================

def load_and_explore_data():
    """
    Load the dataset and perform initial exploration
    Expected candidate approach: systematic data discovery
    """
    # Load dataset (assuming it's already downloaded)
    # df = pd.read_csv('Telco-Customer-Churn.csv')
    
    # For demonstration, we'll create a similar dataset structure
    print("PHASE 1: DATA EXPLORATION")
    print("=" * 50)
    
    # Show what candidate should do:
    print("1. Loading data and checking basic info...")
    # df.info()
    # df.head()
    # df.shape
    
    print("Expected candidate actions:")
    print("- Use df.info() to check data types and missing values")
    print("- Use df.head() to see first few rows")
    print("- Check df.shape for dataset size")
    print("- Identify target variable (likely 'Churn')")
    
    print("\n2. Checking for missing values...")
    # df.isnull().sum()
    
    print("Expected candidate actions:")
    print("- Use df.isnull().sum() or df.info() to identify missing data")
    print("- Ask: 'What do these missing values represent?'")
    
    print("\n3. Basic statistical summary...")
    # df.describe()
    # df.describe(include='object')  # for categorical variables
    
    print("Expected candidate actions:")
    print("- Use df.describe() for numerical features")
    print("- Use df.describe(include='object') for categorical features")
    print("- Ask about business context and feature meanings")

def demonstrate_good_eda_approach():
    """
    Demonstrate what good EDA looks like for this assessment
    """
    print("\nGOOD CANDIDATE OBSERVATIONS:")
    print("-" * 40)
    print("• Dataset has mix of numerical and categorical features")
    print("• Target variable is binary (Churn: Yes/No)")
    print("• Some features might need encoding (gender, Partner, etc.)")
    print("• TotalCharges might be object type - needs investigation")
    print("• Should check class balance in target variable")
    print("• Customer demographics vs usage patterns - interesting split")

# ================================================================================
# PHASE 2: Data Analysis & Insights (15 minutes)  
# ================================================================================

def demonstrate_data_analysis():
    """
    Show expected analytical approach
    """
    print("\n\nPHASE 2: DATA ANALYSIS & INSIGHTS")
    print("=" * 50)
    
    print("1. Missing Data Strategy...")
    print("Expected candidate reasoning:")
    print("- Investigate TotalCharges column (likely has ' ' instead of 0)")
    print("- Convert to numeric and handle appropriately")
    print("- For other missing values: consider business logic")
    print("- Document assumptions made")
    
    print("\n2. Feature Analysis...")
    print("Expected visualizations:")
    print("- Target variable distribution (class balance)")
    print("- Numerical features: histograms/boxplots")
    print("- Categorical features: count plots")
    print("- Correlation heatmap for numerical features")
    print("- Churn rate by categorical features")
    
    print("\n3. Key Insights to Look For:")
    print("- Which customer segments have higher churn?")
    print("- Relationship between tenure and churn")
    print("- Payment method impact on churn")
    print("- Contract type vs churn rate")
    print("- Service usage patterns")

def show_visualization_examples():
    """
    Examples of good visualizations a candidate might create
    """
    # Create sample data for demonstration
    np.random.seed(42)
    sample_data = {
        'Churn': np.random.choice(['Yes', 'No'], 1000, p=[0.3, 0.7]),
        'tenure': np.random.exponential(24, 1000),
        'MonthlyCharges': np.random.normal(65, 20, 1000),
        'Contract': np.random.choice(['Month-to-month', 'One year', 'Two year'], 1000, p=[0.5, 0.3, 0.2])
    }
    df_sample = pd.DataFrame(sample_data)
    
    plt.figure(figsize=(15, 10))
    
    # 1. Churn distribution
    plt.subplot(2, 3, 1)
    df_sample['Churn'].value_counts().plot(kind='bar', color=['skyblue', 'salmon'])
    plt.title('Churn Distribution')
    plt.ylabel('Count')
    
    # 2. Tenure vs Churn
    plt.subplot(2, 3, 2)
    df_sample.boxplot(column='tenure', by='Churn', ax=plt.gca())
    plt.title('Tenure by Churn Status')
    plt.suptitle('')
    
    # 3. Monthly Charges vs Churn  
    plt.subplot(2, 3, 3)
    df_sample.boxplot(column='MonthlyCharges', by='Churn', ax=plt.gca())
    plt.title('Monthly Charges by Churn')
    plt.suptitle('')
    
    # 4. Contract vs Churn Rate
    plt.subplot(2, 3, 4)
    churn_by_contract = df_sample.groupby('Contract')['Churn'].apply(lambda x: (x=='Yes').mean())
    churn_by_contract.plot(kind='bar', color='coral')
    plt.title('Churn Rate by Contract Type')
    plt.ylabel('Churn Rate')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('sample_eda_plots.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print("EXPECTED INSIGHTS FROM VISUALIZATIONS:")
    print("- Month-to-month contracts likely have higher churn")
    print("- New customers (low tenure) more likely to churn")
    print("- Higher monthly charges might correlate with churn")
    print("- Need to investigate correlation vs causation")

# ================================================================================
# PHASE 3: Problem-Solving & Modeling Approach (10 minutes)
# ================================================================================

def demonstrate_modeling_approach():
    """
    Show expected modeling thought process
    """
    print("\n\nPHASE 3: MODELING APPROACH")
    print("=" * 50)
    
    print("1. Problem Framing...")
    print("Expected candidate reasoning:")
    print("- This is a binary classification problem")
    print("- Goal: Predict if customer will churn")
    print("- Business impact: Retention strategies, cost of acquisition")
    print("- Need to balance precision vs recall based on business cost")
    
    print("\n2. Feature Engineering Ideas...")
    print("Good candidates might suggest:")
    print("- Tenure categories (new, mid, long-term customers)")
    print("- Charges per service ratios")
    print("- Total services count")
    print("- Customer lifetime value estimation")
    print("- Interaction features (tenure * contract type)")
    
    print("\n3. Model Selection Reasoning...")
    print("Expected thought process:")
    print("- Start simple: Logistic Regression (interpretable)")
    print("- Consider: Decision Trees (handle categorical well)")
    print("- Advanced: Random Forest if time permits")
    print("- Avoid: Complex models without justification")

def show_baseline_model():
    """
    Demonstrate a simple baseline model implementation
    """
    # Create sample processed data
    np.random.seed(42)
    n_samples = 1000
    
    # Simulate processed features
    X = np.random.randn(n_samples, 5)  # 5 features after preprocessing
    y = (X[:, 0] + X[:, 1] - X[:, 2] + np.random.randn(n_samples) * 0.5 > 0).astype(int)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = LogisticRegression(random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Predictions
    y_pred = model.predict(X_test_scaled)
    
    # Evaluation
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nBASELINE MODEL RESULTS:")
    print(f"Accuracy: {accuracy:.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    print("\nEXPECTED CANDIDATE DISCUSSION:")
    print("- 'Accuracy alone might not be the best metric'")
    print("- 'Should consider precision/recall trade-off'") 
    print("- 'Would need to validate on business metrics'")
    print("- 'Feature importance would help explain predictions'")

def improvement_suggestions():
    """
    What good candidates might suggest for improvements
    """
    print("\nMODEL IMPROVEMENT IDEAS (Good Candidates):")
    print("=" * 50)
    print("1. Feature Engineering:")
    print("   - Create interaction terms")
    print("   - Polynomial features for key variables")
    print("   - Domain-specific feature creation")
    
    print("\n2. Model Selection:")
    print("   - Try Random Forest for non-linear patterns")
    print("   - Cross-validation for better evaluation")
    print("   - Ensemble methods")
    
    print("\n3. Evaluation:")
    print("   - ROC-AUC curve analysis")
    print("   - Precision-Recall curve")
    print("   - Business-focused metrics")
    
    print("\n4. Deployment Considerations:")
    print("   - Model interpretability for business")
    print("   - Prediction confidence intervals")
    print("   - Monitoring for data drift")

# ================================================================================
# ASSESSMENT SCORING EXAMPLES
# ================================================================================

def scoring_examples():
    """
    Examples of how different candidate levels might perform
    """
    print("\n\nSCORING EXAMPLES")
    print("=" * 50)
    
    print("EXCELLENT CANDIDATE (90-100%):")
    print("- Asks about business context immediately")
    print("- Systematic EDA with meaningful insights")
    print("- Thoughtful handling of missing data")
    print("- Creates informative visualizations")
    print("- Justifies modeling choices")
    print("- Discusses trade-offs and limitations")
    print("- Thinks about production deployment")
    
    print("\nGOOD CANDIDATE (75-89%):")
    print("- Covers all technical basics correctly")
    print("- Some good insights but misses a few key patterns")
    print("- Standard visualizations, adequately interpreted")
    print("- Basic modeling approach with reasonable evaluation")
    print("- Can explain their work when prompted")
    
    print("\nSATISFACTORY CANDIDATE (60-74%):")
    print("- Gets through basic data loading and exploration")
    print("- Limited insights, focuses on technical execution")
    print("- Standard plots without deep interpretation")
    print("- Basic model but limited evaluation discussion")
    print("- Needs guidance for next steps")
    
    print("\nNEEDS IMPROVEMENT (<60%):")
    print("- Struggles with basic pandas operations")
    print("- No clear approach or methodology")
    print("- Cannot interpret visualizations meaningfully")
    print("- Jumps to modeling without understanding data")
    print("- Cannot explain their reasoning")

def interviewer_tips():
    """
    Tips for conducting the assessment
    """
    print("\n\nINTERVIEWER TIPS")
    print("=" * 50)
    print("1. PREPARATION:")
    print("   - Download dataset beforehand")
    print("   - Test your own environment")
    print("   - Have backup datasets ready")
    print("   - Prepare follow-up questions")
    
    print("\n2. DURING THE SESSION:")
    print("   - Let them drive, but guide when stuck")
    print("   - Ask 'why' questions frequently")
    print("   - Note their problem-solving approach")
    print("   - Focus on thinking process over perfect results")
    
    print("\n3. KEY OBSERVATION POINTS:")
    print("   - Do they start with data understanding?")
    print("   - How do they handle unexpected issues?")
    print("   - Can they explain complex concepts simply?")
    print("   - Do they consider business implications?")
    
    print("\n4. COMMON PITFALLS TO WATCH FOR:")
    print("   - Rushing to modeling without EDA")
    print("   - Not validating data assumptions")
    print("   - Over-engineering for a simple problem")
    print("   - Cannot explain their code/decisions")

if __name__ == "__main__":
    print("DATA SCIENCE INTERN ASSESSMENT - SAMPLE SOLUTION")
    print("=" * 60)
    print("This demonstrates expected candidate approaches and outcomes")
    print("=" * 60)
    
    # Run demonstration
    load_and_explore_data()
    demonstrate_good_eda_approach()
    demonstrate_data_analysis()
    show_visualization_examples()
    demonstrate_modeling_approach()
    show_baseline_model()
    improvement_suggestions()
    scoring_examples()
    interviewer_tips()
    
    print("\n" + "=" * 60)
    print("END OF SAMPLE SOLUTION")
    print("Use this as a reference for what to expect from candidates")
    print("=" * 60) 