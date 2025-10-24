# AI Developer Interview - Debugging Exercise

## 🎯 Context

You're reviewing code for a FastAPI service that predicts customer churn. This service worked in development but is now experiencing issues in production.

## 📋 Your Task

Review the file `buggy_model_api.py` and:
1. **Find as many bugs/issues as you can**
2. **Explain what each issue is and its impact**
3. **Describe how you would fix it**

Your interviewer will let you know how much time you have.

## 📖 Guidelines

- **Think aloud**: Explain your reasoning as you work
- **Ask questions**: If requirements are unclear, please ask!
- **Prioritize**: Focus on the most critical issues first
- **Be honest**: It's okay to say "I'm not sure" or "I'd need to research this"
- **No need to actually run the code**: Focus on analyzing the logic

## 🔍 What We're Looking For

We want to see:
- ✅ Your debugging process and systematic thinking
- ✅ How you prioritize issues by severity
- ✅ Your understanding of production ML systems
- ✅ Your communication style and clarity
- ✅ How you handle ambiguity and missing information

## 💻 The Code

The file `buggy_model_api.py` contains a FastAPI application that:
- Loads a pre-trained churn prediction model and scaler from pickle files
- Provides a `/predict` endpoint for single customer predictions
- Provides a `/predict_batch` endpoint for multiple predictions
- Has `/health` and `/model_info` endpoints

**The code should be production-ready, but it's not!**

## 💡 Tips

- You don't need to find every single issue - we're more interested in your approach
- Consider multiple categories of issues:
  - Code that won't run at all
  - Issues that will cause crashes in production
  - ML-specific problems (training vs serving)
  - Performance and efficiency concerns
  - Production best practices
- Think about: data quality, error handling, API design, scalability

## ❓ Questions?

Feel free to ask your interviewer any clarifying questions before or during the exercise.

**Good luck! 🚀**

