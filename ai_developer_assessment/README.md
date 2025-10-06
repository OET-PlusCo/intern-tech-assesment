# AI Developer Interview Assessment Package

A comprehensive 60-minute live interview assessment designed to evaluate AI Developer candidates on technical skills, problem-solving ability, and soft skills like transparency, assertiveness, and end-to-end ownership.

---

## 📋 Assessment Overview

**Total Time**: 60 minutes live interview

**Structure**:
- **15 min**: Live debugging exercise (buggy ML API)
- **45 min**: Technical interview questions (system design, MLOps, problem-solving)

**Key Competencies Tested**:
- ✅ End-to-end ML development
- ✅ Production ML awareness (training/serving skew, deployment)
- ✅ MLOps & automation
- ✅ Problem-solving & debugging
- ✅ Transparency & communication
- ✅ Assertiveness & ownership

---

## 📁 Files in This Package

### For the Interviewer (You)

| File | Purpose | When to Use |
|------|---------|-------------|
| `QUICK_START.md` | **Start here!** 5-min prep checklist | Before the interview |
| `README_HIRING_MANAGER.md` | Full assessment guide & rubric | Reference during interview |
| `INTERVIEW_SCORECARD.md` | Scoring sheet to fill during interview | During the interview |
| `INTERVIEW_QUESTIONS.md` | All questions with what to listen for | During technical Q&A |
| `SOLUTION_GUIDE.md` | Answer key for debugging exercise | During debugging portion |

### For the Candidate

| File | Purpose |
|------|---------|
| `CANDIDATE_INSTRUCTIONS.md` | Instructions for the debugging exercise |
| `buggy_model_api.py` | The broken code to debug |
| `requirements.txt` | Dependencies (for context) |

---

## 🚀 Quick Start

### 1. Prep (5 minutes before interview)
1. Open `QUICK_START.md`
2. Print or open `INTERVIEW_SCORECARD.md` for scoring
3. Have `SOLUTION_GUIDE.md` and `INTERVIEW_QUESTIONS.md` ready as tabs

### 2. During Interview (60 minutes)

**Debugging Exercise (15 min)**:
- Share `buggy_model_api.py` with candidate
- Read them `CANDIDATE_INSTRUCTIONS.md` or send it
- Watch them debug while scoring on `INTERVIEW_SCORECARD.md`
- Refer to `SOLUTION_GUIDE.md` for bug answers

**Technical Questions (45 min)**:
- Use questions from `INTERVIEW_QUESTIONS.md`
- Score on `INTERVIEW_SCORECARD.md` as you go

### 3. After Interview (5 minutes)
- Complete `INTERVIEW_SCORECARD.md`
- Calculate total score
- Make hire/no-hire decision

---

## 🎯 What This Assessment Measures

### Technical Skills
- **ML Production Knowledge**: Training/serving skew, feature engineering, model serving
- **Software Engineering**: API design, error handling, testing
- **MLOps**: Deployment strategies, monitoring, automation, CI/CD
- **System Design**: Scalability, architecture, trade-offs

### Soft Skills (Critical for This Role!)
- **Transparency**: Admits uncertainty, asks clarifying questions
- **Assertiveness**: Raises concerns, pushes back on unrealistic requirements
- **Ownership**: End-to-end thinking, takes responsibility
- **Communication**: Clear explanations, collaborative mindset
- **Problem-Solving**: Systematic approach, prioritization

---

## 📊 Scoring Guide

| Score | Recommendation | Description |
|-------|----------------|-------------|
| 90-100 | **Strong Hire** | Exceptional candidate - hire immediately |
| 75-89 | **Hire** | Solid candidate with minor gaps |
| 60-74 | **Maybe** | Has potential but significant concerns |
| <60 | **No Hire** | Does not meet requirements |

---

## 🔍 The Debugging Exercise

### What's Being Tested
The `buggy_model_api.py` file contains **8 intentional bugs** that test:

1. **Basic competence**: Import errors, syntax issues
2. **Production awareness**: File handling, error handling, logging
3. **ML expertise**: Training/serving skew (THE KEY BUG)
4. **Data quality**: Input validation, type handling
5. **Performance**: Batch processing efficiency
6. **Observability**: Health checks, monitoring readiness

### Expected Behavior
- **Strong candidates**: Find 6+ bugs, explain impact, prioritize systematically
- **Average candidates**: Find 3-5 bugs, fix obvious ones
- **Weak candidates**: Find 1-2 bugs, focus only on syntax errors

---

## 💡 Interview Tips

### Do's ✅
- Create psychological safety - tell them it's okay to say "I don't know"
- Let them struggle a bit to see problem-solving process
- Ask "why" to test depth of knowledge
- Watch for soft skills (transparency, assertiveness)
- Take detailed notes on scorecard

### Don'ts ❌
- Don't give hints too early in debugging
- Don't accept surface-level answers
- Don't skip the soft skills assessment
- Don't rush - let them think through problems

### Red Flags 🚩
- Makes excuses or blames tools/others
- Doesn't ask any clarifying questions
- Overconfident without substance
- Gives up after finding one bug
- Can't explain trade-offs or alternatives

### Green Flags ✅
- Asks clarifying questions proactively
- Admits uncertainty honestly
- Systematic, methodical approach
- Thinks about production implications
- Explains reasoning clearly
- Prioritizes by business impact

---

## 🎓 Customization Tips

Want to adjust the assessment? Here's how:

### Make it Harder
- Add more subtle bugs (e.g., race conditions, memory leaks)
- Increase time pressure
- Add system design coding exercise
- Include Kubernetes/Docker questions

### Make it Easier
- Remove some bugs from the debugging exercise
- Provide more context about the production environment
- Focus on specific areas (just MLOps, just ML theory)
- Allow reference materials

### Focus on Specific Skills
- **More MLOps**: Add questions about CI/CD, Kubernetes, monitoring tools
- **More ML**: Add model architecture or algorithm questions
- **More System Design**: Add whiteboarding exercises
- **More Coding**: Add live coding problems (e.g., implement caching)

---

## 📖 Assessment Philosophy

This assessment is designed around the principle that **great AI developers are not just technical experts, but also transparent communicators who take end-to-end ownership.**

The debugging exercise intentionally includes:
- **Ambiguity**: No perfect answer - tests how they handle uncertainty
- **Multiple issues**: Tests thoroughness and prioritization
- **Production concerns**: Tests real-world experience
- **Soft skill triggers**: Forces them to ask questions and admit gaps

The interview questions are designed to:
- **Simulate real scenarios**: Not theoretical puzzles
- **Test decision-making**: Focus on trade-offs and constraints
- **Reveal values**: Do they care about quality, users, collaboration?
- **Assess assertiveness**: Will they push back on bad requirements?

---

## 🤝 After the Interview

### Debrief Checklist
- [ ] Complete `INTERVIEW_SCORECARD.md`
- [ ] Calculate total score
- [ ] List 3 strengths and 3 concerns
- [ ] Make hire recommendation
- [ ] Share feedback with hiring team

### Questions to Reflect On
1. Would I want this person on my team?
2. Can they work independently on complex projects?
3. Will they raise concerns proactively?
4. Do they have the judgment for production systems?
5. Can they learn quickly when facing new challenges?

---

## 📞 Questions or Feedback?

This assessment package is designed to be comprehensive yet flexible. Adapt it to your team's specific needs and culture.

**Good luck with your interviews!**

---

## 📄 License

This assessment package is for internal hiring use. Please adapt and modify as needed for your organization.

