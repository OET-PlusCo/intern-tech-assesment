# Data Science Intern Technical Assessment

## Overview
**Duration:** 40 minutes  
**Format:** Live coding session  
**Objective:** Assess analytical thinking, data manipulation skills, and problem-solving approach

---

## Dataset Selection Options

### Option 1: Customer Churn Prediction (Recommended)
- **Source:** Kaggle - Telco Customer Churn Dataset
- **Size:** ~7,000 records, 21 features
- **URL:** https://www.kaggle.com/datasets/blastchar/telco-customer-churn
- **Why this dataset:** Clean, manageable size, real business problem, good for EDA and basic modeling

### Option 2: House Prices Prediction
- **Source:** Kaggle - House Prices Advanced Regression Techniques  
- **Size:** ~1,400 records, 81 features
- **URL:** https://www.kaggle.com/c/house-prices-advanced-regression-techniques
- **Why this dataset:** Popular, well-documented, good for feature engineering discussion

### Option 3: Wine Quality Assessment
- **Source:** Hugging Face - Wine Quality Dataset
- **Size:** ~6,500 records, 12 features
- **URL:** https://huggingface.co/datasets/mstz/wine_quality
- **Why this dataset:** Straightforward, good for classification/regression discussion

---

## Assessment Structure (40 minutes total)

### Phase 1: Data Exploration & Understanding (15 minutes)
**Objective:** Test how the candidate approaches unknown data

**Tasks:**
1. **Initial Data Loading** (3 minutes)
   - Load the dataset using pandas
   - Display basic information about the dataset
   
2. **Data Overview** (5 minutes)
   - Examine the shape, columns, and data types
   - Identify the target variable
   - Check for missing values
   
3. **Quick EDA** (7 minutes)
   - Generate basic statistical summaries
   - Identify potential data quality issues
   - Ask: "What's your first impression of this data?"

**What to observe:**
- Do they start with `.info()`, `.describe()`, `.head()`?
- Do they ask clarifying questions about the business context?
- How do they handle missing values discovery?

### Phase 2: Data Analysis & Insights (15 minutes)
**Objective:** Assess analytical thinking and visualization skills

**Tasks:**
1. **Missing Data Strategy** (5 minutes)
   - How would you handle missing values in this dataset?
   - Implement their chosen approach
   
2. **Feature Analysis** (7 minutes)
   - Identify the most important features for the target variable
   - Create 2-3 meaningful visualizations
   - Ask: "What patterns do you notice?"
   
3. **Data Quality Assessment** (3 minutes)
   - Check for outliers or anomalies
   - Suggest data cleaning steps

**What to observe:**
- Choice of visualization types
- Ability to interpret plots and draw insights
- Understanding of data distributions and relationships

### Phase 3: Problem-Solving & Modeling Approach (10 minutes)
**Objective:** Test modeling intuition and problem-solving logic

**Tasks:**
1. **Problem Framing** (3 minutes)
   - "How would you approach building a predictive model for this problem?"
   - Discuss model selection reasoning
   
2. **Feature Engineering** (4 minutes)
   - Identify potential feature engineering opportunities
   - Implement 1-2 simple feature transformations
   
3. **Model Implementation** (3 minutes)
   - Build a simple baseline model (logistic regression or decision tree)
   - Evaluate model performance
   - Ask: "How would you improve this model?"

**What to observe:**
- Understanding of different model types and when to use them
- Approach to feature engineering
- Understanding of model evaluation metrics

---

## Evaluation Criteria

### Technical Skills (40%)
- [ ] **Data Manipulation:** Proficient with pandas operations
- [ ] **Data Visualization:** Creates appropriate and informative plots
- [ ] **Statistical Understanding:** Demonstrates basic statistical concepts
- [ ] **Coding Practices:** Clean, readable code with good structure

### Analytical Thinking (35%)
- [ ] **Problem Approach:** Systematic approach to data exploration
- [ ] **Insight Generation:** Ability to extract meaningful insights from data
- [ ] **Critical Thinking:** Questions assumptions and validates findings
- [ ] **Business Context:** Considers practical implications of findings

### Communication & Collaboration (25%)
- [ ] **Explanation Skills:** Can clearly explain their thought process
- [ ] **Question Asking:** Asks relevant clarifying questions
- [ ] **Adaptability:** Responds well to guidance and feedback
- [ ] **Time Management:** Works efficiently within time constraints

---

## Interviewer Guidelines

### Setup Instructions
1. **Pre-session (5 minutes before):**
   - Ensure candidate has Python environment ready (Jupyter/Colab)
   - Share dataset link and basic libraries to import
   - Test screen sharing capability

2. **Introduction (2 minutes):**
   - Explain the format and timeline
   - Encourage thinking out loud
   - Mention that asking questions is encouraged

### Key Questions to Ask
- "Walk me through your thought process here"
- "What would you do if you had more time?"
- "How would you validate this assumption?"
- "What concerns you about this data/approach?"
- "How would you present this to a non-technical stakeholder?"

### Red Flags to Watch For
- Jumping into modeling without understanding the data
- Not checking for data quality issues
- Unable to explain their code or decisions
- Doesn't ask any clarifying questions
- Gives up easily when encountering issues

### Positive Indicators
- Systematic approach to data exploration
- Asks relevant business context questions
- Explains trade-offs in their decisions
- Shows curiosity about unexpected findings
- Adapts approach based on data discoveries

---

## Starter Code Template

```python
# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

# Load the dataset
# df = pd.read_csv('your_dataset.csv')

# Your analysis starts here...
```

---

## Follow-up Questions for Strong Candidates

If the candidate finishes early or performs exceptionally well:

1. **Scalability:** "How would your approach change with 10x more data?"
2. **Production:** "What considerations would you have for deploying this model?"
3. **Bias & Fairness:** "What potential biases might exist in this dataset?"
4. **A/B Testing:** "How would you test this model's performance in production?"
5. **Feature Importance:** "How would you explain feature importance to stakeholders?"

---

## Alternative Datasets (Backup Options)

If technical issues arise with the primary dataset:

1. **Iris Dataset** (built-in sklearn) - Classic, simple, always works
2. **Boston Housing** (sklearn) - Regression problem, good for quick analysis
3. **Titanic Dataset** (Kaggle) - Well-known, good for classification

---

## Assessment Scoring

**Excellent (90-100%):** Systematic approach, insightful analysis, clean code, great communication  
**Good (75-89%):** Solid technical skills, reasonable insights, some communication gaps  
**Satisfactory (60-74%):** Basic technical competency, limited insights, needs guidance  
**Needs Improvement (<60%):** Significant gaps in technical skills or analytical thinking

---

## Notes Section
Use this space during the interview to capture:
- Specific strengths observed
- Areas for improvement
- Interesting insights or approaches
- Questions asked by candidate
- Overall impression and recommendation 