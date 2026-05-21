# Terraform — Deploy track (base infra)

Deploys **one client stack**: Artifact Registry, private GCS bucket, Cloud Run (placeholder image), service accounts. Does **not** enable GCP APIs automatically — if `apply` fails, enable the required APIs and retry.

## Apply

```sh
cd candidate_materials/terraform/deploy
cp terraform.tfvars.example terraform.tfvars
# Edit project_id

terraform init
terraform plan
terraform apply
```

Note outputs: `service_name`, `artifact_registry_repo`, `assets_bucket`, `runtime_service_account`.

## After apply

1. Enable any APIs Terraform reports as disabled (`run`, `artifactregistry`, `storage`, `cloudbuild`, etc.).
2. From `candidate_materials/`, run Cloud Build (see `../../cloudbuild/cloudbuild.yaml`).
3. **Create a Cloud Build trigger** with the same substitutions — see `../../cloudbuild/TRIGGER.md`.
4. Optionally copy `iam_cloudbuild.tf.example` and `cloudbuild_trigger.tf.example` into `.tf` files and apply.
5. Work through bugs in `../../CANDIDATE_INSTRUCTIONS_DEPLOY.md`.

## Cloud Build substitutions

Match Terraform outputs:

| Substitution | Example |
|--------------|---------|
| `_PROJECT_ID` | your project |
| `_REGION` | `us-central1` |
| `_REPOSITORY` | `acme-webapp` (from `client_slug`) |
| `_SERVICE_NAME` | `acme-webapp` (from output `service_name`) |
| `_APP_GREETING` | per-client greeting |
| `_CLIENT_ID` | `client-acme` |
| `_RUNTIME_SA` | output `runtime_service_account` |

Example (run from `candidate_materials/`):

```sh
gcloud builds submit --config=cloudbuild/cloudbuild.yaml . \
  --substitutions=_PROJECT_ID=YOUR_PROJECT,_SERVICE_NAME=acme-webapp,_RUNTIME_SA=acme-webapp-runtime@YOUR_PROJECT.iam.gserviceaccount.com
```
