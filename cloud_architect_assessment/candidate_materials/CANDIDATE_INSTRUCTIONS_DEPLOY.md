# Cloud Architect Assessment — Deploy & Debug Track

**Duration:** 45–90 minutes (level-dependent) · **Format:** Live screen-share · **Cloud:** GCP

## Scenario

We deploy a small **Hello World** Next.js app per client on **Cloud Run** (UI and API in one codebase). Each client gets infrastructure from Terraform, then **Cloud Build** builds and deploys the container.

Apply Terraform, run the pipeline, create a **Cloud Build trigger**, and get the app working end-to-end in the sandbox.

## What you have

| Path | Purpose |
|------|---------|
| `frontend/` | Next.js app, `/api/upload`, Cloud Build config, `terraform/deploy/` stack |
| `TESTING.md` | End-to-end verification checklist |

## Flow

1. `terraform apply` in `frontend/terraform/deploy/`
2. `gcloud builds submit` from `frontend/` (see `frontend/cloudbuild.yaml`)
3. Create a Cloud Build trigger with per-client substitutions (`frontend/TRIGGER.md`)
4. Run the trigger and complete the steps in [`TESTING.md`](TESTING.md)

## Testing scenario (summary)

1. Open the Cloud Run URL in a browser.
2. Confirm **Hello World** and the **greeting** text.
3. Click upload to send an image to **Google Cloud Storage**.
4. Confirm the **image appears on the page**, under the greeting.

Full checklist: [`TESTING.md`](TESTING.md).

You may use AI tools. Think out loud. Ask clarifying questions.

## Ground rules

- Prefer **Terraform / Cloud Build / gcloud** over console-only changes
- Use **least privilege** for IAM
- Per-client values belong on the **trigger** (or submit `--substitutions`)

Your interviewer will share the expected scope and time box for your session. Good luck.
