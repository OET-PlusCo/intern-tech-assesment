# Progressive AI Developer Assessments

A series of 3 progressively challenging assessments (10 minutes each) designed to evaluate AI developer candidates during live interviews.

## 📋 Overview

| Assessment | Difficulty | Time | Focus Areas |
|-----------|------------|------|-------------|
| **#1: Titanic Classification** | Beginner | 10 min | Debugging, data science basics |
| **#2: TBD** | Intermediate | 10 min | TBD |
| **#3: TBD** | Advanced | 10 min | TBD |

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

## 📊 Progression Summary

| Assessment | Difficulty | Time | Focus | Critical Bugs | Subtle Bugs |
|-----------|------------|------|-------|---------------|-------------|
| #1: Titanic | Beginner | 10 min | ML basics, debugging | 2 | 2 |
| #2: FastAPI | Intermediate | 10 min | Production ML, APIs | 2 | 2 |
| #3: Docker | Advanced | 10 min | Security, containers | 2 | 2 |

**Total assessment time**: 30 minutes (can use all 3 or pick individually)

---

##Human: continue please create the second assesment the intermediate one
