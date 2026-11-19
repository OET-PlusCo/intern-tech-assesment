# Assessment: AI Product Quality Engineer

**Time**: 20 minutes  
**Format**: Exploration → Documentation → Automation

---

## 🌍 Context

You're joining the product team at a data intelligence company.

The team has just shipped **v1.2.0** of the **Competitor Intelligence API** — an AI-powered service used daily by **10+ strategic analysts** to track competitors in the fertilizer and agriculture sector. Analysts rely on this API to generate quarterly competitor newsletters, pricing analyses, and market positioning reports.

> **Data accuracy matters.** An analyst who reads a summary about *AgriGlobal* when they asked about *PhosphoTech* may make the wrong strategic call.

Before the next sprint begins, your tech lead has asked you to:

1. Write a **test plan** for this release
2. **Test** the API and find any issues
3. **Document** your findings as proper bug reports
4. *(Bonus)* Write **automated regression tests** for the issues you found

---

## 🎯 Your Tasks

### Task 1 — Write a Test Plan (5 min)
**Before running the API**, review:
- The endpoint list below
- The request examples in `sample_requests.json`
- The interactive docs once the API is running: `http://localhost:8001/docs`

Write a brief test plan that covers:
- What you will test and **why** (what matters to users?)
- At least 3 test categories (happy path, edge cases, error handling)
- Any **AI-specific concerns** you'd want to validate (e.g. consistency, accuracy)

You can write this as a `.md` file, a comment block in the test file, or just describe it out loud to the interviewer.

> 💡 **Tip**: If anything is unclear or ambiguous, ask — don't assume.

---

### Task 2 — Explore & Find Issues (8–10 min)
Start the API, then run the exploration script to systematically test key behaviours:

```bash
python test_competitor_api.py
```

Or test manually with curl/Postman using the examples in `sample_requests.json`.

Each scenario (`S-01` through `S-08`) is designed to reveal something. Pay attention to:
- What comes back versus what you'd expect
- Behaviour that changes across repeated calls
- Error cases — are they handled clearly or silently?

---

### Task 3 — Document Your Findings (5 min)
For **each issue** you find, write a brief bug report with:

| Field | What to include |
|---|---|
| **Title** | One-line summary of the issue |
| **Steps to Reproduce** | Exact steps (endpoint, payload, how many times to run) |
| **Expected Behaviour** | What should happen? |
| **Actual Behaviour** | What actually happens? |
| **Business Impact** | Why does this matter to analysts using the system? |
| **Severity** | Critical / High / Medium / Low — and why |

---

### Task 4 — Automation (Bonus)
Write automated pytest tests for the issues you found.  
Use the starter classes in `test_competitor_api.py` as your scaffolding:

```bash
pytest test_competitor_api.py -v
```

---

## 🚀 Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Start the API (runs on port 8001)
python competitor_intelligence_api.py
```

**Interactive API docs**: `http://localhost:8001/docs`

---

## 📋 Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| GET | `/competitors` | List all competitors in the knowledge base |
| POST | `/analyze` | Analyze a single competitor |
| POST | `/analyze/batch` | Analyze multiple competitors at once |

### `/analyze` Request Schema

```json
{
  "query":       "natural language question  (e.g. 'What are their recent moves?')",
  "competitor":  "competitor name  — get valid names from GET /competitors",
  "format":      "'detailed' or 'brief'  (default: 'detailed')",
  "analyst_id":  "optional tracking identifier"
}
```

---

## ✅ What We're Looking For

| Dimension | What "good" looks like |
|---|---|
| **Product thinking** | You test what matters to *users*, not just technical correctness |
| **Thoroughness** | You systematically explore edge cases, not just happy paths |
| **Bug documentation** | Reports are clear, reproducible, and include business impact |
| **Business awareness** | You connect technical issues to real analyst consequences |
| **Automation mindset** | You identify what must be regression-tested before each release |
| **Communication** | You ask questions instead of assuming missing information |

---

Good luck! 🚀
