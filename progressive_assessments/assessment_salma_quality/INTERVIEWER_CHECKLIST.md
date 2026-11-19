# Interviewer Quick Reference — AI Product Quality Engineer

> **Do NOT share this file with the candidate.**

---

## Setup (Before the Interview)

```bash
cd progressive_assessments/assessment_salma_quality
pip install -r requirements.txt
python competitor_intelligence_api.py        # verify it starts on port 8001
python test_competitor_api.py                # verify all 6 exploration functions run
```

**Share with candidate:**
- `competitor_intelligence_api.py`
- `test_competitor_api.py`
- `sample_requests.json`
- `requirements.txt`
- `README.md`

**Keep to yourself:**
- `INTERVIEWER_CHECKLIST.md` (this file)
- `SOLUTION_GUIDE.md`

---

## Interview Flow (20 Minutes)

### Opening (1 min)
*"This is the Competitor Intelligence API — v1.2.0, just shipped. 10+ analysts use it daily. I'd like you to test it, find any issues, and document what you find. Before running anything, can you walk me through how you'd approach testing an AI API like this?"*

### Test Plan Phase — Task 1 (5 min)
Let them talk through their plan.

**Listen for:**
- [ ] Do they distinguish between *technical* correctness and *product/user* correctness?
- [ ] Do they mention AI-specific concerns (consistency, reproducibility, accuracy)?
- [ ] Do they think about **data accuracy** — not just "does it return 200"?
- [ ] Do they ask clarifying questions instead of assuming? *(key signal for this role)*
- [ ] Do they mention edge cases proactively (empty inputs, unknown competitors)?

**Red flags:**
- Only plans happy-path testing
- No mention of what failure looks like from a user's perspective
- Assumes everything without asking

### Exploration Phase — Task 2 (8–10 min)
Let them run `python test_competitor_api.py` and explore freely.

**Watch for:**
- Do they read the exploration output carefully or skim it?
- Do they re-run tests when they see inconsistency?
- Do they think aloud about *why* something is wrong (business impact)?
- Do they go beyond the exploration script and test additional cases?

---

## Bug Tracking Sheet

### Bug #1 — Data Corruption in Brief Format  🔴 CRITICAL

**Root cause**: `generate_analysis()` randomly replaces the competitor's display name with a different competitor's name when `format="brief"`.

**Observable signs:**
- [ ] `explore_brief_format()` shows wrong competitor names in summaries
- [ ] Running scenario S-02 multiple times reveals different names in `summary`
- [ ] Batch scenario S-06 shows mismatched names across results

**What they should report:**
```
Title: Summary in 'brief' format displays the wrong competitor name
Steps: POST /analyze with format="brief" and competitor="PhosphoTech" × 4 times
Expected: Every summary mentions "PhosphoTech"
Actual: Summaries randomly mention "AgriGlobal" or "NutriCorp"
Business impact: Analysts reading a brief competitive overview will attribute
                 market share and strategy to the wrong competitor, leading to
                 wrong pricing and positioning decisions.
Severity: Critical — data accuracy failure in the primary use case
```

**Discussion questions:**
1. "How would you catch this in an automated test?"
2. "What if this bug only appeared 30% of the time — how would you test for it?"
3. "Who else on the team needs to know about this?"

**Red flags:**
- Finds the inconsistency but can't explain the business impact
- Doesn't note that it's random / intermittent

---

### Bug #2 — Silent Failure on Unknown Competitor  🔴 CRITICAL

**Root cause**: When a competitor is not in `COMPETITOR_DATABASE`, the function returns empty data instead of raising an error. The endpoint returns HTTP 200 with `summary: ""`.

**Observable signs:**
- [ ] `explore_unknown_competitor()` shows HTTP 200 with empty summary and insights
- [ ] Scenario S-03 returns `{"summary": "", "insights": [], "confidence": 0.0, ...}`
- [ ] No error message, no indication that the input was wrong

**What they should report:**
```
Title: Unknown competitor returns HTTP 200 with empty data instead of an error
Steps: POST /analyze with competitor="UnknownCorp"
Expected: HTTP 404 or 400 with a clear error message
Actual: HTTP 200 with empty summary and insights, confidence=0.0
Business impact: Analysts see empty results and cannot tell if (a) the system
                 has no data, (b) their input was wrong, or (c) the AI
                 genuinely found nothing. They may report non-issues or miss
                 real data-entry mistakes.
Severity: Critical — silent failures are worse than explicit errors
```

**Discussion questions:**
1. "What HTTP status code would you return and why?"
2. "Should the error message tell the user what valid competitors are?"
3. "How would you distinguish 'AI found nothing' from 'invalid input'?"

**Red flags:**
- Says "it works, it just returns empty" — misses the implicit failure
- Can't explain why HTTP 200 with empty data is worse than a 404

---

### Bug #3 — Non-Reproducible Confidence Scores  🟠 HIGH

**Root cause**: `confidence = round(random.uniform(0.60, 0.98), 2)` is called on every request — same input, different output every time.

**Observable signs:**
- [ ] `explore_reproducibility()` shows three different confidence values for identical requests
- [ ] Scenario S-04 (run twice) shows different confidence scores

**What they should report:**
```
Title: Confidence score is non-deterministic — same query returns different values
Steps: POST /analyze with same payload twice, compare "confidence"
Expected: Identical inputs → identical confidence scores
Actual: confidence changes on every call (e.g. 0.72, 0.85, 0.63)
Business impact: (1) Cannot reproduce a specific analyst-reported issue.
                 (2) Cannot track AI quality degradation over time.
                 (3) Cannot create meaningful regression benchmarks.
                 (4) Erodes analyst trust — "why did it say 0.95 yesterday and 0.61 today?"
Severity: High — blocks quality tracking and issue reproduction
```

**Discussion questions:**
1. "What would you need to make results reproducible? (seeds, caching, versioning)"
2. "How would you write a regression test for this — what's the assertion?"
3. "What's the difference between AI non-determinism that's acceptable vs. problematic?"

**Red flags:**
- Accepts randomness as "normal for AI" without questioning it
- Doesn't connect it to inability to reproduce user issues

---

### Bug #4 — No Format Validation  🟡 MEDIUM

**Root cause**: The `format` field has no validation. Any string is accepted silently; invalid values fall through to "detailed" behaviour with no warning to the caller.

**Observable signs:**
- [ ] `explore_format_validation()` shows HTTP 200 for all invalid format values
- [ ] Scenario S-05 (`format="executive"`) succeeds silently
- [ ] Response field `format` echoes back the invalid value as if it's valid

**What they should report:**
```
Title: Invalid `format` values accepted silently — no validation error
Steps: POST /analyze with format="executive" (or "quick", "summary", etc.)
Expected: HTTP 422 Unprocessable Entity listing valid options
Actual: HTTP 200 — API silently behaves as "detailed" without notifying the caller
Business impact: Downstream systems or dashboards that pass custom format values
                 will receive unexpected output with no indication of misconfiguration.
                 Developers integrating the API cannot trust their format preference
                 is being respected.
Severity: Medium — doesn't corrupt data but breaks contract between API and consumer
```

**Discussion questions:**
1. "Where should this validation live — Pydantic model or inside the function?"
2. "Should the API reject it or default gracefully? What are the trade-offs?"
3. "What would the OpenAPI spec say about this field if it were correct?"

**Red flags:**
- Marks severity as Critical (over-reaction relative to the other bugs)
- Can't distinguish between validation at the model layer vs. business logic layer

---

## Overall Scoring Rubric

### Dimension 1: Product & Business Thinking (30%)

| Score | Description |
|---|---|
| 9–10 | Connects every bug to analyst impact without prompting. Thinks about what analysts would experience, not just what the code does. |
| 7–8 | Mentions business impact for most bugs, needs light prompting for one or two. |
| 5–6 | Identifies bugs technically but business impact is surface-level or only when asked. |
| 3–4 | Treats this like a code debugging exercise. No product lens. |
| 1–2 | Only technical observations with no user/business context. |

### Dimension 2: Test Plan Quality (20%)

| Score | Description |
|---|---|
| 9–10 | Identifies AI-specific risks (consistency, accuracy, reproducibility), proposes categories beyond happy path, asks clarifying questions before testing. |
| 7–8 | Solid plan with multiple test categories, mentions some AI concerns. |
| 5–6 | Basic plan, mostly happy path and negative cases, limited AI awareness. |
| 3–4 | Vague plan or jumps straight to running without planning. |
| 1–2 | No plan at all. |

### Dimension 3: Bug Documentation Quality (25%)

| Score | Description |
|---|---|
| 9–10 | All 4 bugs documented with clear reproduction steps, expected vs. actual, severity with justification, and concrete business impact. |
| 7–8 | 3–4 bugs documented, most fields present, impact stated. |
| 5–6 | 2–3 bugs documented, some fields missing, impact vague. |
| 3–4 | 1–2 bugs documented, reproduction steps unclear. |
| 1–2 | Verbal notes only, no written documentation. |

### Dimension 4: Thoroughness & Exploration (15%)

| Score | Description |
|---|---|
| 9–10 | Found all 4 bugs. Went beyond the exploration script. Tested edge cases proactively. |
| 7–8 | Found 3–4 bugs. Used the exploration script well plus some manual testing. |
| 5–6 | Found 2–3 bugs. Mostly followed the script. |
| 3–4 | Found 1–2 bugs. Missed non-obvious ones. |
| 1–2 | Found 0–1 bugs. |

### Dimension 5: Automation Mindset (10%)

| Score | Description |
|---|---|
| 9–10 | Wrote working regression tests for all 4 bugs with clear assertions. |
| 7–8 | Wrote 2–3 working tests or stubbed all 4 meaningfully. |
| 5–6 | Wrote 1 working test or described what automation would look like. |
| 3–4 | Filled in one test partially. |
| 1–2 | No automation produced. |

---

## Decision Matrix

| Dimension | Weight | Score (1–10) | Weighted |
|---|---|---|---|
| Product & Business Thinking | 30% | ___ | ___ |
| Test Plan Quality | 20% | ___ | ___ |
| Bug Documentation | 25% | ___ | ___ |
| Thoroughness | 15% | ___ | ___ |
| Automation Mindset | 10% | ___ | ___ |
| **Total** | **100%** | | **___** |

### Score Guide
- **85–100**: Strong Hire — sharp product lens, thorough, excellent documentation
- **70–84**: Hire — good product thinking, solid documentation, found main bugs
- **55–69**: Maybe — technically competent but limited product/business framing
- **< 55**: No Hire — treats this as a pure code task, missed critical issues

---

## Watch List: Does She Ask Questions?

A key signal for this role is whether the candidate **asks clarifying questions** rather than assuming. Mark each occurrence:

- [ ] Asked about the intended behaviour of an endpoint before testing
- [ ] Flagged an ambiguity in the spec (e.g. "what should happen for unknown competitors?")
- [ ] Asked about the analyst workflow to understand impact
- [ ] Requested confirmation before logging a bug (e.g. "is this by design?")
- [ ] Named an assumption explicitly instead of treating it as fact

> Candidates who ask good questions before diving in demonstrate the mindset described in the role: *"do not assume missing information — ask and validate."*

---

## Notes Section

### Strengths Observed:
1.
2.
3.

### Concerns Observed:
1.
2.
3.

### Questions Asked by Candidate (Good Signal):
1.
2.
3.

### Overall Recommendation:
- [ ] Strong Hire
- [ ] Hire
- [ ] Maybe — more interview
- [ ] No Hire

**Reasoning:**
