# Webapp Stack — Terraform

This is the current Terraform setup for our webapp. It's a single `main.tf`
that deploys the full stack for **one client** (`client-acme`).

## What gets deployed

| Resource | Purpose |
|----------|---------|
| Cloud Run service | The webapp itself (Python/Node container) |
| Cloud SQL Postgres | App database |
| GCS bucket | User uploads & static assets |
| Artifact Registry repo | Container images for this client |
| Secret Manager secrets | DB password, Stripe API key |
| 2× Service Accounts | One runtime SA (used by Cloud Run), one deployer SA (used by CI) |
| IAM bindings | Tying the SAs to the resources above |

## Files

- `main.tf` — all resources (the monolith)
- `variables.tf` — currently almost empty
- `outputs.tf` — outputs from the stack
- `terraform.tfvars.example` — example values

## How it runs today

```sh
terraform init
terraform plan
terraform apply
```

GCP project: `acme-webapp-prod` (in the assessment, use whatever project ID your interviewer gave you — adjust the hardcoded value in `main.tf`)
Region: `us-central1`

## A note on the container image

The Cloud Run service references the public placeholder image `gcr.io/cloudrun/hello`
rather than a real app image. This is so a fresh GCP assessment project can run
`terraform apply` end-to-end without needing an image pre-pushed to Artifact Registry.

In real life, this would be a private image built and pushed by CI into the
Artifact Registry repo defined in this file. **Your refactor should preserve
that future state** — keep the Artifact Registry repo + IAM as part of the
client's stack even though the placeholder image doesn't actually use it.

## What's wrong with this picture

Nothing — for one client. The problem starts at client #2.

If we want to deploy this same stack for `client-beta`, today we would
copy-paste this file, find-and-replace `acme` → `beta`, and change the project
ID. That doesn't scale to 10 clients, let alone 50.

**Your job is to make this scale.**

Refer to `../CANDIDATE_INSTRUCTIONS.md` for what we're asking you to do.
