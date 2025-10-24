# 🎯 AI Developer Assessment - Quick Reference

## ✅ Repository is Clean and Ready to Share!

---

## 📁 What You Have Now

```
ai_developer_assessment/
│
├── ✅ SAFE TO SHARE WITH CANDIDATES:
│   ├── README.md                    (Overview for candidates)
│   ├── CANDIDATE_INSTRUCTIONS.md    (Exercise details)
│   ├── buggy_model_api.py          (Buggy code to debug)
│   └── requirements.txt             (Dependencies)
│
└── ❌ KEEP PRIVATE (interviewer_materials/):
    ├── CHEAT_SHEET.md              ⭐ Print this for interviews!
    ├── SOLUTION_GUIDE.md            (All 8 bug answers)
    ├── INTERVIEW_QUESTIONS.md       (Questions to ask)
    ├── INTERVIEW_SCORECARD.md       (Scoring sheet)
    └── ... (10+ helpful guides)
```

---

## 🚀 How to Use This

### For Your Next Interview:

1. **Before interview** (5 min):
   - Open: `ai_developer_assessment/interviewer_materials/CHEAT_SHEET.md`
   - Print: `ai_developer_assessment/interviewer_materials/INTERVIEW_SCORECARD.md`

2. **Share with candidate**:
   - `CANDIDATE_INSTRUCTIONS.md`
   - `buggy_model_api.py`

3. **During interview**:
   - Reference `SOLUTION_GUIDE.md` for bug answers
   - Use `INTERVIEW_QUESTIONS.md` for Q&A portion
   - Score on `INTERVIEW_SCORECARD.md`

### First Time Using This?

Read: `ai_developer_assessment/interviewer_materials/README_INTERVIEWER.md`

---

## 🔒 Security

✅ **Protected by .gitignore** - Interviewer materials won't be committed  
✅ **Separate folders** - Clear separation of candidate vs interviewer files  
✅ **Safe to share** - You can share the entire `ai_developer_assessment/` folder (just not the `interviewer_materials/` subfolder)

---

## 📤 Sharing with Candidates

### Option 1: During Live Interview (Recommended)
Just share these two files during the interview:
- `CANDIDATE_INSTRUCTIONS.md`
- `buggy_model_api.py`

### Option 2: Share the Entire Folder
You can share the whole `ai_developer_assessment/` folder because:
- Interviewer materials are in a separate subfolder
- Just tell candidates to only look at the root level files

### Option 3: GitHub/Version Control
The `.gitignore` protects interviewer materials, so you can safely:
```bash
git add ai_developer_assessment/
git commit -m "Add AI developer assessment"
git push
```

---

## 🐛 The 8 Bugs (Quick Reference)

1. **Import typo** - `pydette` → `pydantic`
2. **File handling** - No error handling for model loading
3. **Feature mismatch** ⭐ - Training/serving skew (MOST IMPORTANT!)
4. **Data validation** - No validation on string→float conversion
5. **Batch inefficiency** - Loops instead of batch processing
6. **Error handling** - Generic exception catching
7. **Logging config** - Logging not configured
8. **Health check** - Doesn't verify model loaded

**Strong candidates find 6+ bugs, especially Bug #3**

---

## 📊 Scoring Quick Guide

- **90-100**: Strong Hire 🌟
- **75-89**: Hire ✅
- **60-74**: Maybe 🤔
- **<60**: No Hire ❌

---

## 📍 File Locations

**Candidate materials:**
```
/Users/angie.ariza/Documents/intern-tech-assesment/ai_developer_assessment/
```

**Your interviewer guides:**
```
/Users/angie.ariza/Documents/intern-tech-assesment/ai_developer_assessment/interviewer_materials/
```

---

## 🎯 Next Steps

1. **Review** the interviewer materials in the `interviewer_materials/` folder
2. **Print** the cheat sheet and scorecard
3. **Share** only the candidate-facing files when interviewing
4. **Score** using the provided rubrics

---

## 💡 Pro Tips

- ✅ Tell candidates it's okay to say "I don't know"
- ✅ Let them struggle to see their problem-solving process
- ✅ Watch for soft skills: transparency, assertiveness, ownership
- ✅ Bug #3 (feature mismatch) is the key differentiator
- ❌ Don't give hints in the first 10 minutes

---

## 📞 Need Help?

Everything is documented in the `interviewer_materials/` folder:
- Start with `README_INTERVIEWER.md`
- Use `CHEAT_SHEET.md` during interviews
- Reference `SOLUTION_GUIDE.md` for detailed bug explanations

---

**You're all set! Good luck with your interviews! 🚀**

