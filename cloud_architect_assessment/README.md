# Cloud Architect Assessment

Live, shared-screen GCP assessments for Cloud Architect candidates. Two complementary tracks in one repo — pick one per session (or run both on separate days).

| Track | Candidate doc | Focus | Duration |
|-------|---------------|--------|----------|
| **Modularization** | `candidate_materials/CANDIDATE_INSTRUCTIONS.md` | Terraform modules & multi-tenant **design** | ~60 min |
| **Deploy & debug** | `candidate_materials/CANDIDATE_INSTRUCTIONS_DEPLOY.md` | Cloud Build, Cloud Run, IAM, intentional bugs | ~45–90 min (leveled) |

Use **modularization** for architecture and module boundaries. Use **deploy & debug** for pipeline fluency, build-time env vars, deploy flags, and least-privilege IAM.

---

## Folder structure

```
cloud_architect_assessment/
│
├── README.md
│
├── candidate_materials/              ← Share with candidate
│   ├── CANDIDATE_INSTRUCTIONS.md           ← Modularization track
│   ├── CANDIDATE_INSTRUCTIONS_DEPLOY.md    ← Deploy & debug track
│   ├── ARCHITECTURE_QUESTIONS.md
│   ├── LEVELS.md                           ← Deploy track difficulty tiers
│   ├── frontend/                           ← Hello World app (deploy track)
│   ├── cloudbuild/                         ← Pipeline + TRIGGER.md
│   └── terraform/
│       ├── main.tf                         ← Monolith to refactor (modularization)
│       ├── variables.tf, outputs.tf, ...
│       └── deploy/                         ← Base infra for deploy track
│
└── interviewer_materials/          ← KEEP PRIVATE
    ├── INTERVIEWER_GUIDE.md                ← Modularization run-of-show
    ├── INTERVIEWER_GUIDE_DEPLOY.md
    ├── SOLUTION_GUIDE.md
    ├── ANSWER_KEY_QUESTIONS.md
    ├── SCORECARD.md
    ├── SCORECARD_DEPLOY.md
    ├── BUGS_AND_SOLUTIONS.md
    ├── DISCUSSION_QUESTIONS_DEPLOY.md
    └── ANALYSIS_DEPLOY.md
```

---

## Track 1 — Modularization (~60 min)

Evaluates **architectural reasoning** (not syntax puzzles):

- Refactor `terraform/main.tf` into modules
- Design onboarding for multiple clients
- Open-ended discussion (`ARCHITECTURE_QUESTIONS.md`)

**Interviewer:** `interviewer_materials/INTERVIEWER_GUIDE.md`, `SCORECARD.md`, `SOLUTION_GUIDE.md`

| Phase | Time |
|-------|------|
| Intro & context | 5 min |
| Refactor into modules | 20 min |
| Multi-client design | 15 min |
| Design Q&A | 15 min |
| Wrap-up | 5 min |

---

## Track 2 — Deploy & debug (~45–90 min)

Hands-on **Terraform → Cloud Build → Cloud Run** with seeded production-like bugs.

| Level | Scope |
|-------|--------|
| Beginning | Build-time env bug, manual build + trigger, explain pipeline |
| Intermediate | + env deploy flags, public access, per-client substitutions |
| Advanced | + GCS IAM, signed URLs, API bootstrap |

**Interviewer:** `INTERVIEWER_GUIDE_DEPLOY.md`, `BUGS_AND_SOLUTIONS.md`, `SCORECARD_DEPLOY.md`

**Quick start:**

1. `terraform apply` in `candidate_materials/terraform/deploy/`
2. `gcloud builds submit` then create trigger (`cloudbuild/TRIGGER.md`)
3. Candidate fixes bugs; score with `BUGS_AND_SOLUTIONS.md`

---

## Scoring snapshot (modularization track)

| Band | Score | Signal |
|------|-------|--------|
| Strong Hire | 85–100 | Multiple valid designs, deep trade-off reasoning |
| Hire | 70–84 | One clean design, defends trade-offs when prompted |
| Maybe | 55–69 | Refactor done, weak multi-client design |
| No Hire | <55 | Cannot finish refactor or tool-name-only answers |

Deploy track: see `interviewer_materials/SCORECARD_DEPLOY.md`.

---

**Built for:** Cloud Architects owning multi-client webapp deployments on GCP and CI/CD (Terraform, Cloud Build, Cloud Run).
