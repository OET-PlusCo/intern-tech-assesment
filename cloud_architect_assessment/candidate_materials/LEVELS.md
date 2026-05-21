# Deploy track — assessment levels

Pick one track based on role seniority and time available. All levels share the same repo; higher levels include more bugs and discussion.

---

## Beginning (~45 min)

**Goal:** Understand the deploy pipeline and fix build-time configuration.

| Step | Activity |
|------|----------|
| 1 | `terraform apply` (enable APIs if needed) |
| 2 | Run `gcloud builds submit`; open Cloud Run URL |
| 3 | Create a **manual Cloud Build trigger** (`cloudbuild/TRIGGER.md`) |
| 4 | Fix **Bug 1** — greeting shows `(not set at build time)` |
| 5 | Explain **cloudbuild.yaml**, **Dockerfile**, and your **trigger** config |

**Discussion (5–10 min):**

- Why don’t frontend env vars work if you only set them on Cloud Run at runtime?
- What is `$SHORT_SHA` / substitutions used for?

**Not required at this level:** GCS upload, signed URLs, multi-client naming.

---

## Intermediate (~60 min)

Everything in **Beginning**, plus:

| Bug | Symptom |
|-----|---------|
| **Bug 2** | After Cloud Build deploy, `CLIENT_ID` / `ASSETS_BUCKET` from Terraform are gone |
| **Bug 3** | Cloud Run URL returns 403 / requires auth |
| **Task** | Parameterize **service name** per client via trigger/build substitutions |
| **Task** | Second trigger or trigger set for `client-beta` (different `_SERVICE_NAME`, `_CLIENT_ID`, `_RUNTIME_SA`) |

**Discussion:**

- Difference between `--set-env-vars` and `--update-env-vars`.
- Where public access should live: Terraform vs deploy flag vs both.

---

## Advanced (~75–90 min)

Everything in **Intermediate**, plus:

| Bug | Symptom |
|-----|---------|
| **Bug 4** | Upload button → permission error from backend |
| **Bug 5** | Upload succeeds but image does not display (private bucket) |
| **APIs** | First `terraform apply` may fail until APIs are enabled properly |

**Discussion:**

- Signed URL vs public bucket — trade-offs and least privilege.
- Wiring runtime service account in Cloud Build deploy (env var vs hardcoded email).
- Mitigating slow builds: Docker layer cache, Kaniko cache, registry cache.

**IAM bar:** `roles/storage.objectCreator` + `objectViewer` (or `objectAdmin` on prefix) — **not** `storage.admin` or project-wide admin on the runtime SA.

---

## Multi-client stretch (optional, any level)

Create a **second Cloud Build trigger** (or duplicate trigger with different substitutions) for `client-beta`:

- `_SERVICE_NAME=beta-webapp`
- `_CLIENT_ID=client-beta`
- `_RUNTIME_SA=beta-webapp-runtime@PROJECT.iam.gserviceaccount.com`

Terraform for `client-beta` is a second apply with different `client_slug` / `tfvars` — verbal design is enough if time is short.
