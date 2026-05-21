# Cloud Architect Assessment — v2 (Deploy & Debug)

Hands-on assessment focused on **Terraform → Cloud Build → Cloud Run** on GCP. Candidates deploy infrastructure, build a frontend with CI/CD, and fix intentional bugs that mirror real production incidents.

## How v2 differs from v1

| Aspect | v1 (`cloud_architect_assessment/`) | v2 (this folder) |
|--------|-----------------------------------|------------------|
| **Focus** | Terraform modularization & multi-tenant design | Post-`apply` pipeline, Cloud Build, runtime/IAM issues |
| **Format** | Refactor monolith + architecture Q&A | Debug seeded bugs + explain pipeline |
| **AI resistance** | Trade-off reasoning | Env/build-time vs runtime, IAM least privilege, deploy flags |

v1 remains valid for **architecture and module design**. Use v2 when you want to test **operational GCP fluency** (Cloud Build, Docker, Cloud Run deploy, GCS IAM).

## Folder structure

```
v2/
├── README.md
├── candidate_materials/
│   ├── CANDIDATE_INSTRUCTIONS.md
│   ├── LEVELS.md
│   ├── frontend/              # Hello World + env-driven greeting
│   ├── cloudbuild/
│   │   ├── cloudbuild.yaml    # Intentional bugs — do not “fix” before interview
│   │   ├── Dockerfile
│   │   └── TRIGGER.md         # Create manual or push trigger + substitutions
│   └── terraform/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── README.md
└── interviewer_materials/     # PRIVATE
    ├── INTERVIEWER_GUIDE.md
    ├── BUGS_AND_SOLUTIONS.md
    ├── DISCUSSION_QUESTIONS.md
    └── SCORECARD.md
```

## Suggested levels

| Level | Time | Bugs / tasks |
|-------|------|----------------|
| **Beginning** | ~45 min | Bug 1, manual build + **manual trigger**, explain pipeline |
| **Intermediate** | ~60 min | + Bugs 2–3, trigger substitutions per client, push trigger (optional) |
| **Advanced** | ~75–90 min | + GCS IAM for uploads, signed URLs (private bucket), API enablement, least-privilege IAM |

See `candidate_materials/LEVELS.md` for the full breakdown.

## Quick start (interviewer)

1. Provision a GCP sandbox project; share project ID and credentials.
2. Candidate runs `terraform apply` in `candidate_materials/terraform/`.
3. Candidate runs `gcloud builds submit`, then **creates a Cloud Build trigger** (`cloudbuild/TRIGGER.md`).
4. Use `interviewer_materials/BUGS_AND_SOLUTIONS.md` to score fixes and probes.
5. Fill `interviewer_materials/SCORECARD.md` within 24 hours.

## Seeded bugs (summary)

| ID | Symptom | Strong fix |
|----|---------|------------|
| 1 | Frontend env var empty / wrong at runtime | Cloud Build substitutions → Docker `ARG` → build-time embed (or runtime config via backend) |
| 2 | Terraform env vars disappear after deploy | Use `--update-env-vars` or remove `--set-env-vars` from deploy step |
| 3 | Cannot open Cloud Run URL (403) | Enable public invoker in Terraform and/or deploy with `--allow-unauthenticated` |
| 4 | Upload button → backend permission error | Grant least-privilege GCS role to runtime SA in Terraform; attach SA to Cloud Run |
| 5 | Upload succeeds but image not visible | Signed URLs (preferred) or controlled read access — not `allUsers` on bucket |
| — | `terraform apply` fails on API not enabled | Enable APIs via Terraform / `gcloud` (not UI-only) |
| Task | Same service name for every client build | Parameterize via **trigger** substitutions |
| Task | No repeatable CI | Create trigger (Terraform / `gcloud`); wire `_RUNTIME_SA`, `_SERVICE_NAME` |

Full rubric and acceptable/low answers: `interviewer_materials/BUGS_AND_SOLUTIONS.md`.
