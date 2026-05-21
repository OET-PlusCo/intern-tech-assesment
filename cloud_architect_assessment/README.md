# Cloud Architect Assessment

Live, shared-screen GCP assessments for Cloud Architect candidates. Two complementary tracks in one repo — pick one per session (or run both on separate days).

| Track | Candidate doc | Focus | Duration |
|-------|---------------|--------|----------|
| **Modularization** | `candidate_materials/CANDIDATE_INSTRUCTIONS.md` | Terraform modules & multi-tenant **design** | ~60 min |
| **Deploy & debug** | `candidate_materials/CANDIDATE_INSTRUCTIONS_DEPLOY.md` | Cloud Build, Cloud Run, IAM | ~45–90 min |

Use **modularization** for architecture and module boundaries. Use **deploy & debug** for pipeline fluency, build-time env vars, deploy flags, and least-privilege IAM.

---

## Folder structure (what is in git)

```
cloud_architect_assessment/
│
├── README.md
├── INTERVIEWER_SETUP.md          ← How to install local interviewer pack
│
└── candidate_materials/          ← Share with candidate only
    ├── CANDIDATE_INSTRUCTIONS.md
    ├── CANDIDATE_INSTRUCTIONS_DEPLOY.md
    ├── TESTING.md                      ← E2E verification (deploy track)
    ├── ARCHITECTURE_QUESTIONS.md
    ├── frontend/
    ├── cloudbuild/
    └── terraform/
        ├── main.tf               ← Monolith (modularization)
        └── deploy/               ← Deploy track infra
```

**Interviewer guides, scorecards, and answer keys** live in `interviewer_materials/` on your machine only — see [`INTERVIEWER_SETUP.md`](INTERVIEWER_SETUP.md). That folder is **gitignored** and must not be pushed.

---

## Track 1 — Modularization (~60 min)

- Refactor `terraform/main.tf` into modules
- Design onboarding for multiple clients
- Open-ended discussion (`ARCHITECTURE_QUESTIONS.md`)

| Phase | Time |
|-------|------|
| Intro & context | 5 min |
| Refactor into modules | 20 min |
| Multi-client design | 15 min |
| Design Q&A | 15 min |
| Wrap-up | 5 min |

---

## Track 2 — Deploy & debug (~45–90 min)

1. `terraform apply` in `candidate_materials/terraform/deploy/`
2. `gcloud builds submit` then create a Cloud Build trigger (`cloudbuild/TRIGGER.md`)
3. Candidate completes the flow in `candidate_materials/TESTING.md` (greeting, upload, image on page)

Scope and level are set by the interviewer using the local materials pack.

---

**Built for:** Cloud Architects owning multi-client webapp deployments on GCP and CI/CD (Terraform, Cloud Build, Cloud Run).
