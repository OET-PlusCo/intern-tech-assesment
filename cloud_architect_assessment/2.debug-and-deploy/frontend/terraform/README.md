# Terraform — deploy stack

Deploys one client stack: Artifact Registry, GCS bucket, Cloud Run, service accounts.

## Apply

```sh
cd candidate_materials/frontend/terraform/deploy
cp terraform.tfvars.example terraform.tfvars
# Edit project_id

terraform init
terraform plan
terraform apply
```

Outputs: `service_name`, `artifact_registry_repo`, `assets_bucket`, `runtime_service_account`.

## Cloud Build

From `candidate_materials/frontend/`:

```sh
gcloud builds submit --config=cloudbuild.yaml .
```

See `../../TRIGGER.md` for trigger setup.
