# Cloud Architect Assessment v2 — Candidate Instructions

**Duration:** 45–90 minutes (level-dependent) · **Format:** Live screen-share · **Cloud:** GCP

## Scenario

We deploy a small **Hello World frontend** per client on **Cloud Run**. Each client gets isolated infrastructure from Terraform, then **Cloud Build** builds the Docker image and deploys it.

Your sandbox already has (or will have) Terraform applied. The pipeline and app **mostly work** but several production-like issues are waiting for you.

## What you have

| Path | Purpose |
|------|---------|
| `terraform/` | Base stack (Cloud Run, GCS, Artifact Registry, service accounts) |
| `frontend/` | Node app: Hello World + greeting from env + GCS upload button |
| `cloudbuild/cloudbuild.yaml` | CI: build image → push → deploy Cloud Run |
| `cloudbuild/Dockerfile` | Multi-stage build for the frontend |
| `cloudbuild/TRIGGER.md` | How to create a Cloud Build trigger (manual or push) |
| `LEVELS.md` | Optional difficulty tiers |

## Flow

1. **Terraform** — `terraform apply` (fix API enablement if apply fails).
2. **Cloud Build (manual)** — `gcloud builds submit` to validate `cloudbuild.yaml`.
3. **Cloud Build trigger** — create a trigger (manual or on push) with per-client **substitutions** — see `cloudbuild/TRIGGER.md`.
4. **Verify** — run the trigger, open the Cloud Run URL, check the greeting, try the upload button.
5. **Fix** — resolve seeded bugs until the app behaves as expected for a public demo.

You may use AI tools. Think out loud. Ask clarifying questions.

## Expected end state

- Browser shows **Hello World** and a **greeting** that reflects your client config (not `(not set at build time)`).
- Cloud Run URL is **reachable without Google sign-in** (public webapp).
- **Upload** succeeds and you can **see** the uploaded image (private bucket — design matters).
- Deploying via Cloud Build does **not** wipe environment variables Terraform set.
- For a second client, the **Cloud Run service name** can differ via build config (not a single hardcoded name everywhere).
- A **Cloud Build trigger** exists (Terraform, `gcloud`, or Console + IaC follow-up) with correct substitutions including `_SERVICE_NAME` and `_RUNTIME_SA`.

## What we may ask you to explain

- Main sections of `cloudbuild.yaml` (build, push, deploy).
- Main stages of the `Dockerfile` (build vs runtime).
- Why frontend env vars often fail without Cloud Build → Docker → build wiring.
- How to **speed up** repeated builds (e.g. layer cache, Artifact Registry as cache).
- How a **trigger** differs from `gcloud builds submit` and which substitutions must live on the trigger.

## Ground rules

- Prefer **Terraform / Cloud Build / gcloud** fixes over console-only changes (console is acceptable for exploration, not as the final answer).
- **Least privilege** for IAM — avoid granting `roles/storage.admin` or project Owner to the runtime SA.
- Say **"I don't know"** when appropriate; we value reasoning over guessing.

See `LEVELS.md` if your interviewer assigns a tier. Good luck.
