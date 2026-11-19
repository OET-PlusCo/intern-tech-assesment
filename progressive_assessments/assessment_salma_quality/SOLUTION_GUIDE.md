# Solution Guide — AI Product Quality Engineer Assessment

> **Interviewer only — do not share with the candidate.**

---

## Overview

This assessment contains **4 intentional bugs** in the Competitor Intelligence API.  
Unlike the code-debugging assessments, the candidate is **not expected to fix the code** —  
they are expected to **find, reproduce, and document** the issues with business context.

| # | Severity | Type | Observable How |
|---|---|---|---|
| 1 | 🔴 Critical | Data corruption | Run brief-format query multiple times |
| 2 | 🔴 Critical | Silent failure | Query an unknown competitor |
| 3 | 🟠 High | Non-reproducibility | Run identical query twice, compare confidence |
| 4 | 🟡 Medium | Missing validation | Send invalid format value |

---

## Bug #1 — Data Corruption in Brief Format

### Location in Code
```python
# competitor_intelligence_api.py — generate_analysis(), lines ~90-96
if response_format == "brief":
    others = [c for c in COMPETITOR_DATABASE if c != competitor]
    wrong_name = random.choice(others)              # BUG: should be `competitor`
    summary = f"{wrong_name} holds {data['market_share']}% ..."
```

### What the Candidate Should Discover
Running `POST /analyze` with `format="brief"` and `competitor="PhosphoTech"` multiple times returns summaries that name `AgriGlobal` or `NutriCorp` instead of `PhosphoTech`.  
The underlying **data** (market share, insights) is correct for PhosphoTech — only the display name is wrong.

### Model Bug Report
```
Title: Summary in 'brief' format displays the wrong competitor name (intermittent)

Steps to Reproduce:
  1. POST /analyze with {"query": "...", "competitor": "PhosphoTech", "format": "brief"}
  2. Repeat 4-5 times
  3. Observe the "summary" field in each response

Expected: summary always starts with "PhosphoTech holds X% market share..."
Actual:   summary randomly starts with "AgriGlobal" or "NutriCorp" ~66% of the time

Business Impact:
  Analysts using the brief format for quick competitive overviews will read
  market-share figures attributed to the wrong company. Pricing and positioning
  decisions based on this data may be entirely incorrect.
  Brief format is typically used in executive dashboards and newsletters —
  the highest-visibility surfaces.

Severity: Critical
  Data accuracy failure in core functionality. Intermittent nature makes it
  harder to catch — analysts may not notice for weeks.
```

### Fix
```python
# Change: wrong_name = random.choice(others)
# To:     display_name = competitor
summary = f"{competitor} holds {data['market_share']}% ..."
```

---

## Bug #2 — Silent Failure on Unknown Competitor

### Location in Code
```python
# competitor_intelligence_api.py — generate_analysis(), lines ~65-72
if competitor not in COMPETITOR_DATABASE:
    return {
        "summary": "",
        "insights": [],
        "confidence": 0.0,
        "data_source": "knowledge_base",
    }
```
The endpoint then wraps this in an HTTP 200 response — no error is ever raised.

### What the Candidate Should Discover
`POST /analyze` with `competitor="UnknownCorp"` returns HTTP 200 with empty `summary`, empty `insights`, and `confidence=0.0`.  
There is no way for the caller to distinguish this from a valid but empty result.

### Model Bug Report
```
Title: Querying an unknown competitor returns HTTP 200 with empty data instead of an error

Steps to Reproduce:
  1. GET /competitors  → note valid names (PhosphoTech, AgriGlobal, NutriCorp)
  2. POST /analyze with {"query": "...", "competitor": "UnknownCorp"}
  3. Observe: HTTP 200, summary="", insights=[], confidence=0.0

Expected: HTTP 404 or HTTP 400 with a message like
  "Competitor 'UnknownCorp' not found. Valid options: PhosphoTech, AgriGlobal, NutriCorp"

Actual: HTTP 200 with empty payload. No error signal.

Business Impact:
  An analyst who misspells a competitor name or uses a deprecated name receives
  a blank response with no explanation. They may:
    - File a support ticket thinking the AI is broken
    - Assume the competitor has no data and skip the analysis entirely
    - Trust a blank result and report "no intelligence available"
  Silent failures are harder to debug and erode trust in the platform.

Severity: Critical
  Empty 200s are silent data failures. Explicit errors are always
  preferable to ambiguous empty responses in a data-accuracy context.
```

### Fix
```python
if competitor not in COMPETITOR_DATABASE:
    raise HTTPException(
        status_code=404,
        detail=(
            f"Competitor '{competitor}' not found in knowledge base. "
            f"Valid options: {', '.join(COMPETITOR_DATABASE.keys())}"
        ),
    )
```

---

## Bug #3 — Non-Reproducible Confidence Score

### Location in Code
```python
# competitor_intelligence_api.py — generate_analysis(), line ~108
confidence = round(random.uniform(0.60, 0.98), 2)
```
Called on every request with no seeding or caching.

### What the Candidate Should Discover
Running the identical request twice returns different `confidence` values each time  
(e.g. `0.73` → `0.85` → `0.61`). There is no way to reproduce a specific result.

### Model Bug Report
```
Title: Confidence score is non-deterministic — identical queries return different values

Steps to Reproduce:
  1. POST /analyze with {"query": "What is their market share?", "competitor": "AgriGlobal"}
  2. Record the "confidence" field
  3. POST the identical request again
  4. Compare confidence values

Expected: Same inputs → same confidence score (or at minimum a stable score per session)
Actual:   confidence changes on every call

Business Impact:
  1. Cannot reproduce analyst-reported issues:
     "It showed 0.42 confidence yesterday" — but we can't reproduce that state.
  2. Cannot track AI quality over time:
     Trending confidence down over releases is impossible to detect.
  3. Cannot write reliable regression tests:
     Any test asserting a specific confidence value will be flaky.
  4. Erodes analyst trust:
     Confidence is used by analysts to decide how much to verify manually.
     A value that changes without explanation is meaningless.

Severity: High
  Does not corrupt data but blocks quality tracking and issue reproduction.
```

### Fix Options

**Option A — Deterministic seed per query (recommended)**
```python
import hashlib
seed_str = f"{competitor}:{query}:{response_format}"
seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16) % (2**32)
rng = random.Random(seed)
confidence = round(rng.uniform(0.60, 0.98), 2)
```

**Option B — Store confidence in the knowledge base**
```python
# COMPETITOR_DATABASE entry gains a "confidence" key
"PhosphoTech": { ..., "base_confidence": 0.87 }
confidence = data["base_confidence"]
```

**Option C — Remove confidence entirely until it's real**
If this is mock data, exposing a fake confidence score may be worse than not having one.

---

## Bug #4 — No Format Validation

### Location in Code
```python
# competitor_intelligence_api.py — AnalysisRequest model, line ~116
class AnalysisRequest(BaseModel):
    ...
    format: str = "detailed"    # accepts any string — no validation
```

The `generate_analysis` function's `if response_format == "brief":` block means any value other than `"brief"` silently behaves as `"detailed"`.

### What the Candidate Should Discover
Sending `format="executive"`, `format="quick"`, or any arbitrary value returns HTTP 200 with no warning.  
The response echoes back the invalid format string as if it were valid.

### Model Bug Report
```
Title: Invalid 'format' values accepted silently — no validation error returned

Steps to Reproduce:
  1. POST /analyze with {"query": "...", "competitor": "NutriCorp", "format": "executive"}
  2. Observe: HTTP 200, format="executive" echoed back in response

Expected: HTTP 422 with a message like
  "Invalid format 'executive'. Valid values: 'detailed', 'brief'"

Actual: HTTP 200 — API silently falls back to 'detailed' behaviour with no notification

Business Impact:
  Downstream systems or dashboard widgets that pass a custom format string
  will receive unexpected output layout without any error signal.
  Engineers integrating the API cannot trust that their format preference
  is being respected — they need to compare output structure manually
  to discover the misconfiguration.
  Also: the API docs say "detailed or brief" but the contract is not enforced.

Severity: Medium
  Doesn't corrupt data or cause silent data failures, but breaks the
  contract between the API and its consumers.
```

### Fix
```python
from enum import Enum
from pydantic import BaseModel

class AnalysisFormat(str, Enum):
    DETAILED = "detailed"
    BRIEF    = "brief"

class AnalysisRequest(BaseModel):
    query:       str
    competitor:  str
    format:      AnalysisFormat = AnalysisFormat.DETAILED
    analyst_id:  Optional[str] = None
```
Pydantic + FastAPI will automatically return HTTP 422 with a clear message for invalid values.

---

## Ideal Test Plan (Reference)

A strong candidate's test plan would include:

### Categories
1. **Happy path** — valid inputs, all three competitors, both formats
2. **Data accuracy** — does the response reference the competitor I requested?
3. **Error handling** — unknown competitor, missing required fields, invalid format
4. **AI-specific concerns:**
   - *Consistency*: same query → same response?
   - *Reproducibility*: can I reproduce a reported result?
   - *Non-determinism*: is randomness acceptable here, and in what fields?
5. **Regression baseline** — what must always pass before every release?

### AI-Specific Risks to Flag Proactively
- Variable outputs between calls (confidence, phrasing)
- Output accuracy vs. requested input (name matching)
- Silent failures masquerading as empty results
- Format contract not enforced

---

## Ideal Automated Regression Tests (Reference)

```python
# test_competitor_api.py — filled-in versions of the TODO stubs

import requests
import pytest

API_URL = "http://localhost:8001"

class TestCompetitorAccuracy:

    def test_detailed_format_names_correct_competitor(self):
        r = requests.post(f"{API_URL}/analyze", json={
            "query": "What is their market position?",
            "competitor": "PhosphoTech",
            "format": "detailed"
        })
        assert r.status_code == 200
        assert "PhosphoTech" in r.json()["summary"]

    def test_brief_format_names_correct_competitor(self):
        # Run multiple times to catch the intermittent bug
        for _ in range(5):
            r = requests.post(f"{API_URL}/analyze", json={
                "query": "What is their market position?",
                "competitor": "PhosphoTech",
                "format": "brief"
            })
            assert r.status_code == 200
            assert "PhosphoTech" in r.json()["summary"], (
                f"Expected 'PhosphoTech' in summary but got: {r.json()['summary']}"
            )

    def test_batch_brief_format_names_correct_competitors(self):
        r = requests.post(f"{API_URL}/analyze/batch", json={"queries": [
            {"query": "Market position?", "competitor": "PhosphoTech", "format": "brief"},
            {"query": "Market position?", "competitor": "AgriGlobal",  "format": "brief"},
            {"query": "Market position?", "competitor": "NutriCorp",   "format": "brief"},
        ]})
        assert r.status_code == 200
        for analysis in r.json()["analyses"]:
            assert analysis["competitor"] in analysis["summary"], (
                f"Summary for {analysis['competitor']} does not mention that competitor: "
                f"{analysis['summary']}"
            )


class TestErrorHandling:

    def test_unknown_competitor_returns_http_error(self):
        r = requests.post(f"{API_URL}/analyze", json={
            "query": "What are their recent moves?",
            "competitor": "NonExistentCorp"
        })
        assert r.status_code != 200, (
            f"Expected an HTTP error for unknown competitor, got {r.status_code} "
            f"with body: {r.json()}"
        )
        assert r.status_code in (400, 404, 422)

    def test_invalid_format_returns_validation_error(self):
        r = requests.post(f"{API_URL}/analyze", json={
            "query": "What is their market position?",
            "competitor": "NutriCorp",
            "format": "executive"
        })
        assert r.status_code in (400, 422), (
            f"Expected validation error for invalid format, got {r.status_code}"
        )


class TestReproducibility:

    def test_same_query_same_confidence_score(self):
        payload = {
            "query": "What is their market share?",
            "competitor": "AgriGlobal",
            "format": "detailed"
        }
        r1 = requests.post(f"{API_URL}/analyze", json=payload)
        r2 = requests.post(f"{API_URL}/analyze", json=payload)
        assert r1.status_code == 200 and r2.status_code == 200
        assert r1.json()["confidence"] == r2.json()["confidence"], (
            f"Same query returned different confidence scores: "
            f"{r1.json()['confidence']} vs {r2.json()['confidence']}"
        )
```

---

## Scoring Quick Reference

| Total Score | Recommendation |
|---|---|
| **85–100** | Strong Hire |
| **70–84** | Hire |
| **55–69** | Maybe — discuss with team |
| **< 55** | No Hire |
