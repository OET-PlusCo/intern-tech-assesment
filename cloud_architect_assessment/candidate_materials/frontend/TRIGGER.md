# Cloud Build trigger

Pass per-client values on a **Cloud Build trigger** (or `gcloud builds submit --substitutions`). The pipeline uses custom substitution variables in `cloudbuild.yaml`; there is no `substitutions:` defaults block in that file.

## Prerequisites

- `cloudbuild.googleapis.com` enabled
- Terraform applied in `terraform/deploy/`; note outputs: `service_name`, `runtime_service_account`, `artifact_registry_repo`
- Source repository (Cloud Source Repositories, GitHub, or GitLab) — your interviewer will specify
- Deployer service account IAM for running builds (`terraform/deploy/iam_cloudbuild.tf.example`)

Build context is `frontend/` (contains `cloudbuild.yaml`, `Dockerfile`, and the Next.js app).

Run from Console: **Cloud Build → Triggers → Run**.
