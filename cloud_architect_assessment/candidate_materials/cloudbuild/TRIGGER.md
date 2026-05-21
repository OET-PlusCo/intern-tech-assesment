# Cloud Build trigger — candidate guide

After `cloudbuild.yaml` works with `gcloud builds submit`, create a **Cloud Build trigger** so deploys run from the repo (push or manual) with the correct **substitutions** per client.

## Prerequisites

- `cloudbuild.googleapis.com` enabled
- Terraform applied; note outputs: `service_name`, `runtime_service_account`, `artifact_registry_repo`
- Source in **Cloud Source Repositories**, **GitHub** (connected to GCP), or **GitLab** — your interviewer will say which to use
- Deployer SA can run builds (see `terraform/deploy/iam_cloudbuild.tf.example` — uncomment or add equivalent IAM)

## Substitution map (required on every trigger)

| Substitution | Source |
|--------------|--------|
| `_PROJECT_ID` | GCP project ID |
| `_REGION` | e.g. `us-central1` |
| `_REPOSITORY` | Artifact Registry repo id (e.g. `acme-webapp`) |
| `_SERVICE_NAME` | Terraform output `service_name` |
| `_APP_GREETING` | Per-client greeting string |
| `_CLIENT_ID` | e.g. `client-acme` |
| `_RUNTIME_SA` | Terraform output `runtime_service_account` (full email) |

Build context: repo root must contain `cloudbuild/` and `frontend/` (submit directory = repository root).

---

## Option A — Manual trigger (good for live assessment)

No Git push required; run from Console or RPC.

```sh
cd ..   # candidate_materials/

gcloud builds triggers create manual acme-webapp-deploy \
  --region=us-central1 \
  --project=YOUR_PROJECT_ID \
  --build-config=cloudbuild/cloudbuild.yaml \
  --substitutions=_PROJECT_ID=YOUR_PROJECT_ID,_REGION=us-central1,_REPOSITORY=acme-webapp,_SERVICE_NAME=acme-webapp,_APP_GREETING=Hello%20from%20Trigger,_CLIENT_ID=client-acme,_RUNTIME_SA=acme-webapp-runtime@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

Then in Console: **Cloud Build → Triggers → Run** on `acme-webapp-deploy`.

**Strong answer:** Same trigger defined in Terraform (`terraform/deploy/cloudbuild_trigger.tf.example`) or committed `gcloud` script.

---

## Option B — Push trigger (Cloud Source Repositories)

1. Create / mirror repo (interviewer may provide):

```sh
gcloud source repos create intern-tech-assessment --project=YOUR_PROJECT_ID
gcloud source repos clone intern-tech-assessment --project=YOUR_PROJECT_ID
# copy candidate_materials contents, commit, push
```

2. Create trigger:

```sh
gcloud builds triggers create cloud-source-repositories acme-webapp-on-push \
  --region=us-central1 \
  --project=YOUR_PROJECT_ID \
  --repo=intern-tech-assessment \
  --branch-pattern="^main$" \
  --build-config=cloudbuild/cloudbuild.yaml \
  --substitutions=_PROJECT_ID=YOUR_PROJECT_ID,_REGION=us-central1,_REPOSITORY=acme-webapp,_SERVICE_NAME=acme-webapp,_APP_GREETING=Hello%20from%20Trigger,_CLIENT_ID=client-acme,_RUNTIME_SA=acme-webapp-runtime@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

3. Push a commit; confirm build starts automatically.

---

## Option C — Push trigger (GitHub / GitLab, 2nd gen)

Requires an existing **Cloud Build connection** in the project (interviewer sets up, or you create via Console / `gcloud builds connections create`).

Use Console **Cloud Build → Triggers → Create**, or Terraform `google_cloudbuild_trigger` with `repository_event_config` (see `terraform/deploy/cloudbuild_trigger.tf.example`).

Wire the same substitutions as in Option A.

---

## Option D — Terraform trigger (preferred for “good” score)

Copy `terraform/deploy/cloudbuild_trigger.tf.example` → `terraform/deploy/cloudbuild_trigger.tf`, set `create_cloudbuild_trigger = true` in `terraform.tfvars`, adjust `source_repo_name` / connection variables, `terraform apply`.

---

## Per-client triggers

For `client-beta`, create a **second trigger** (or one trigger per repo branch) with different:

- `_SERVICE_NAME` → `beta-webapp`
- `_CLIENT_ID` → `client-beta`
- `_REPOSITORY` / `_RUNTIME_SA` matching that client's Terraform outputs

Do **not** reuse one trigger's substitutions for all tenants unless you use separate trigger files per client.

---

## Verify

- [ ] Trigger appears in `gcloud builds triggers list --region=us-central1`
- [ ] Run produces a build using `cloudbuild/cloudbuild.yaml`
- [ ] Build logs show expected substitution values (especially `_SERVICE_NAME`, `_RUNTIME_SA`)
- [ ] Cloud Run revision updates after trigger run

---

## Common failures

| Error | Likely fix |
|-------|------------|
| Permission denied starting build | Grant deployer SA `roles/cloudbuild.builds.editor` + trigger uses that SA |
| Deploy step cannot set Cloud Run SA | `roles/iam.serviceAccountUser` on runtime SA for deployer (or Cloud Build SA) |
| Wrong config path | `build-config` path is relative to **repo root**, not `cloudbuild/` folder only |
| Substitutions empty in build | Set on trigger, not only in `cloudbuild.yaml` defaults |
