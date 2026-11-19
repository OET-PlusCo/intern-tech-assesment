# Progressive AI Developer Assessments

A series of assessments designed to evaluate AI developer candidates and AI product quality engineers during live interviews.

## 📋 Overview

| Assessment | Difficulty | Time | Role | Focus Areas |
|-----------|------------|------|------|-------------|
| **#1: Titanic Classification** | Beginner | 10 min | AI Developer | Debugging, data science basics |
| **#2: Production ML API** | Intermediate | 10 min | AI Developer | FastAPI, memory, efficiency, validation |
| **#3: Containerized ML API** | Advanced | 10 min | AI Developer | Docker security, containers, DevOps |
| **Salma: AI Product Quality** | Intermediate | 20 min | AI Quality Engineer | Test plans, bug documentation, product thinking |

---

## 🎯 Assessment #1: Titanic Classification (Beginner)

**Location**: `assessment_01_beginner/`

### What It Tests
- Debugging skills
- Python/pandas proficiency
- Understanding of ML best practices (data leakage, stratification)
- Attention to detail

### Bugs Included
- 2 **critical** bugs (prevent execution)
- 2 **subtle** bugs (best practices)

### Files
- `titanic_classification.ipynb` - Buggy notebook
- `README.md` - Detailed instructions
- `requirements.txt` - Dependencies

### How to Use
1. Share `titanic_classification.ipynb` with candidate
2. Give them 10 minutes to find and fix bugs
3. Observe their debugging process
4. Check if they identify subtle bugs

---

## 🎯 Assessment #2: Production ML API (Intermediate)

**Location**: `assessment_02_intermediate/`

### What It Tests
- Production ML knowledge
- Memory management and efficiency
- Logic errors and correctness
- Input validation and edge cases
- FastAPI and code organization

### Bugs Included
- **Bug #1 (CRITICAL)**: Memory leak - model loaded on every request
- **Bug #2 (CRITICAL)**: Inverted risk logic - wrong predictions
- **Bug #3 (SUBTLE)**: Inefficient batch processing
- **Bug #4 (SUBTLE)**: Missing input validation

### Files
- `model_api.py` - FastAPI app with bugs
- `test_api.py` - Test script to verify fixes
- `sample_requests.json` - Example requests
- `SOLUTION_GUIDE.md` - Full solutions (interviewer only)
- `requirements.txt` - Dependencies

### How to Use
1. Share `model_api.py`, `test_api.py`, `requirements.txt`, and `README.md`
2. Candidate installs dependencies and runs API
3. Candidate uses test script to identify bugs
4. Give them 10 minutes to find and fix all issues
5. Check SOLUTION_GUIDE.md for scoring

---

## 🎯 Assessment #3: Containerized ML API (Advanced)

**Location**: `assessment_03_advanced/`

### What It Tests
- Docker security best practices
- Container optimization and efficiency
- Production deployment knowledge
- Multiple solution approaches
- DevOps/MLOps skills

### Bugs Included
- **Bug #1 (CRITICAL)**: Exposed secrets in Dockerfile (hardcoded ENV)
- **Bug #2 (CRITICAL)**: Running as root user (security risk)
- **Bug #3 (SUBTLE)**: Inefficient layer caching (slow builds)
- **Bug #4 (SUBTLE)**: Missing health checks (no monitoring)

### Key Feature: Multiple Valid Solutions!
Each bug can be fixed in 2-4 different ways - tests candidate's depth of knowledge and ability to explain trade-offs.

### Files
- `Dockerfile` - Container definition with bugs
- `docker-compose.yml` - Orchestration with bugs
- `model_api.py` - Working FastAPI app (no bugs)
- `test_container.sh` - Automated test script
- `env_example.txt` - Environment template
- `SOLUTION_GUIDE.md` - All solutions & approaches (interviewer only)
- `INTERVIEWER_CHECKLIST.md` - Quick reference (interviewer only)
- `requirements.txt` - Dependencies

### How to Use
1. Share Dockerfile, docker-compose.yml, model_api.py, test_container.sh, README.md
2. Candidate runs `./test_container.sh` to identify bugs
3. Give them 10 minutes to fix all issues
4. Ask them to explain WHY they chose their solution approach
5. Check SOLUTION_GUIDE.md for valid solutions and scoring

---

---

## 🎯 Assessment: AI Product Quality Engineer (Salma profile)

**Location**: `assessment_salma_quality/`

### What It Tests
- Product & business thinking (not just code correctness)
- Writing structured test plans for AI systems
- Bug discovery through systematic exploration
- Bug documentation quality (reproduction steps, business impact, severity)
- Automation mindset (regression test design)
- Communication — does the candidate ask questions vs. assume?

### Issues Included
- **Issue #1 (CRITICAL)**: Data corruption — wrong competitor name shown in brief format
- **Issue #2 (CRITICAL)**: Silent failure — unknown competitor returns HTTP 200 with empty data
- **Issue #3 (HIGH)**: Non-reproducible confidence scores — same query, different values every time
- **Issue #4 (MEDIUM)**: No format validation — invalid format values accepted silently

### Key Differentiator vs. Developer Assessments
Candidates are **not asked to fix the code**. They are asked to:
1. Write a test plan before touching anything
2. Discover issues through systematic testing
3. Document findings as professional bug reports with **business impact**
4. Write regression tests to catch these issues in future releases

### Files
- `competitor_intelligence_api.py` — FastAPI app with 4 issues (share with candidate)
- `test_competitor_api.py` — Exploration + pytest stubs (share with candidate)
- `sample_requests.json` — Guided test scenarios (share with candidate)
- `requirements.txt` — Dependencies (share with candidate)
- `README.md` — Candidate instructions (share with candidate)
- `SOLUTION_GUIDE.md` — Full expected answers & fix code (interviewer only)
- `INTERVIEWER_CHECKLIST.md` — Scoring guide & discussion questions (interviewer only)

### How to Use
1. Share all non-interviewer files with the candidate
2. Ask them to write a test plan BEFORE running anything (~5 min)
3. Let them run the exploration script and find issues (~8–10 min)
4. Ask them to document findings as bug reports (~5 min)
5. If time permits: ask them to fill in the pytest stubs
6. Use `INTERVIEWER_CHECKLIST.md` to score each dimension

---

## 📊 Assessment Summary

| Assessment | Time | Role Target | Focus | Issues |
|-----------|------|-------------|-------|--------|
| #1: Titanic | 10 min | AI Developer | ML debugging | 4 (fix code) |
| #2: FastAPI | 10 min | AI Developer | Production ML | 4 (fix code) |
| #3: Docker | 10 min | AI Developer | Security/DevOps | 4 (fix code) |
| Salma: Quality | 20 min | AI Quality Engineer | Test & document | 4 (find & document) |
