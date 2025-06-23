# Interviewer Quick Reference Guide

## Pre-Session Checklist (5 minutes before)
- [ ] Dataset ready (`datasets/sample_telco_data.csv` or real dataset)
- [ ] Candidate has Python environment (Jupyter/Colab) ready
- [ ] Screen sharing tested
- [ ] Backup environment prepared (Google Colab link ready)
- [ ] Assessment timer set to 40 minutes

## Opening Script (2 minutes)
*"Hi [Name], welcome to the technical assessment. Today we'll be working with a customer churn dataset for about 40 minutes. This is meant to be collaborative - please think out loud, ask questions, and don't worry about getting everything perfect. We're more interested in your thought process than the final results. Ready to start?"*

## Phase 1: Data Exploration (15 min) - What to Look For

### ✅ **Excellent Indicators:**
- Starts with `df.head()`, `df.info()`, `df.describe()`
- Asks about business context
- Identifies target variable quickly
- Checks data types and missing values systematically
- Comments on data quality issues

### ⚠️ **Concerning Signs:**
- Jumps straight to visualizations without understanding data
- Doesn't check for missing values
- No questions about business context
- Can't identify what the target variable is

### **Key Questions to Ask:**
- *"What's your first impression of this data?"*
- *"What would you want to know from the business team?"*
- *"How would you handle the missing values?"*

## Phase 2: Analysis & Insights (15 min) - What to Look For

### ✅ **Excellent Indicators:**
- Creates relevant visualizations (churn distribution, feature relationships)
- Interprets plots correctly
- Notices patterns (e.g., month-to-month customers churn more)
- Handles data preprocessing intelligently
- Asks about correlation vs causation

### ⚠️ **Concerning Signs:**
- Random/meaningless visualizations
- Can't interpret their own plots
- Doesn't notice obvious patterns
- Struggles with basic pandas operations

### **Key Questions to Ask:**
- *"What patterns do you see here?"*
- *"Which features seem most important for churn?"*
- *"How would you validate this finding?"*

## Phase 3: Modeling (10 min) - What to Look For

### ✅ **Excellent Indicators:**
- Justifies model choice (e.g., "logistic regression for interpretability")
- Handles categorical variables properly
- Discusses train/test split
- Considers appropriate metrics beyond accuracy
- Mentions limitations and improvements

### ⚠️ **Concerning Signs:**
- No justification for model choice
- Doesn't handle categorical variables
- Only looks at accuracy
- Can't explain model results

### **Key Questions to Ask:**
- *"Why did you choose this model?"*
- *"How would you explain this to a business stakeholder?"*
- *"What would you do differently with more time?"*

## Time Management
- **0-15 min:** Data exploration
- **15-30 min:** Analysis & visualization  
- **30-40 min:** Modeling & discussion
- **40+ min:** Wrap-up questions

## Common Issues & Solutions

| **Issue** | **Gentle Guidance** |
|-----------|-------------------|
| Stuck on loading data | *"The dataset is in the datasets folder"* |
| No clear approach | *"What would be your first step with any new dataset?"* |
| Too focused on code | *"Can you explain what you're thinking here?"* |
| Running out of time | *"Let's focus on the key insights rather than perfect code"* |
| Perfect code, no insights | *"What does this tell us about the business problem?"* |

## Scoring Quick Reference

**🌟 Excellent (90-100%):**
- Systematic data exploration
- Meaningful insights with business context
- Clear communication throughout
- Appropriate modeling choices

**👍 Good (75-89%):**
- Covers technical basics well
- Some good insights
- Generally clear communication
- Reasonable modeling approach

**👌 Satisfactory (60-74%):**
- Basic technical competency
- Limited insights
- Needs some guidance
- Simple modeling approach

**❌ Needs Improvement (<60%):**
- Struggles with basics
- No clear methodology
- Poor communication
- Inappropriate or no modeling

## Wrap-up Questions (Last 5 minutes)
1. *"How would you present these findings to executives?"*
2. *"What business actions would you recommend?"*  
3. *"What additional data would help?"*
4. *"Any concerns about deploying this model?"*

## Red Flags - End Interview Early
- Cannot load or explore data after 10 minutes
- No logical thought process 
- Cannot explain any of their code
- Hostile or uncooperative attitude

## Notes Template
```
Candidate: _______________
Date: _______________

Technical Skills (40%):     /10
- Data manipulation:        /10
- Visualization:           /10
- Modeling:               /10

Analytical Thinking (35%):  /10
- Problem approach:        /10
- Insights:               /10
- Critical thinking:       /10

Communication (25%):        /10
- Explanation:            /10
- Questions asked:        /10
- Adaptability:           /10

Overall Score: ___/100
Recommendation: HIRE / NO HIRE / BORDERLINE

Key Strengths:
-
-

Areas for Improvement:
-
-

Additional Notes:
``` 