# AI Developer Assessment - Hiring Manager Guide

## Overview
This assessment is designed for a **60-minute live interview** to evaluate AI Developer candidates on:
- End-to-end development skills
- Problem-solving and debugging abilities
- Transparency and communication
- Production-readiness mindset
- MLOps knowledge

## Interview Structure (60 minutes)

### Part 1: Live Debugging Exercise (15 minutes)
**Objective**: Assess problem-solving, debugging skills, and transparency

**Instructions for Candidate**:
1. Share screen
2. Open `buggy_model_api.py`
3. Tell them: *"This is a FastAPI service for a churn prediction model that's failing in production. Find and fix as many issues as you can in 15 minutes. Think aloud as you work."*

**What to Observe**:
- ✅ Do they ask clarifying questions?
- ✅ Do they admit when they're unsure?
- ✅ Do they think systematically or randomly?
- ✅ Do they explain their reasoning clearly?
- ✅ Do they find multiple issues or stop after the first one?
- ✅ Do they think about production implications?

**Expected Issues to Find** (see `SOLUTION_GUIDE.md` for details):
- 8 bugs ranging from critical to best-practice violations
- Tests their ML knowledge, Python skills, and production awareness

---

### Part 2: Technical Interview Questions (45 minutes)

Use the questions in `INTERVIEW_QUESTIONS.md`:
- **System Design** (15 min): End-to-end ML system architecture
- **MLOps & Deployment** (15 min): Production practices, CI/CD, monitoring
- **Problem-Solving Scenarios** (15 min): Real-world challenges, soft skills assessment

---

## Scoring Rubric

### Debugging Exercise (40 points)
| Criteria | Points | What to Look For |
|----------|--------|------------------|
| **Bugs Found** | 0-20 | Found 1-2 bugs (10pts), 3-5 bugs (15pts), 6+ bugs (20pts) |
| **Communication** | 0-10 | Clear explanation of thought process, asks good questions |
| **Transparency** | 0-5 | Admits uncertainty, raises concerns about ambiguity |
| **Approach** | 0-5 | Systematic debugging, tests assumptions, considers production |

### Interview Questions (60 points)
| Criteria | Points | What to Look For |
|----------|--------|------------------|
| **System Design** | 0-20 | Scalable architecture, considers edge cases, end-to-end thinking |
| **MLOps Knowledge** | 0-20 | CI/CD, monitoring, deployment strategies, automation |
| **Problem-Solving** | 0-15 | Analytical thinking, practical solutions, trade-off analysis |
| **Soft Skills** | 0-5 | Assertiveness, ownership, collaborative attitude |

### Overall Scoring
- **90-100**: Strong Hire - Exceptional candidate
- **75-89**: Hire - Solid candidate with minor gaps
- **60-74**: Maybe - Has potential but significant gaps
- **<60**: No Hire - Does not meet requirements

---

## Tips for Interviewing

1. **Create Psychological Safety**: Tell candidates it's okay to say "I don't know" and ask questions
2. **Don't Give Hints Too Early**: Let them struggle a bit to see their problem-solving process
3. **Probe Deeply**: Ask "why" and "how would you handle X" to test depth
4. **Listen for Red Flags**:
   - Making excuses or blaming tools
   - Not asking about requirements/constraints
   - Overconfident without substance
   - Can't explain trade-offs

## Files in This Assessment
- `buggy_model_api.py` - Broken code for debugging exercise
- `INTERVIEW_QUESTIONS.md` - Structured questions for the interview
- `SOLUTION_GUIDE.md` - Answer key and evaluation guidance
- `requirements.txt` - Dependencies (for context)

