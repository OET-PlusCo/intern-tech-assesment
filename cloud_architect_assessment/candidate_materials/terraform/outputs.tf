###############################################################################
# Outputs
###############################################################################

output "service_url" {
  description = "Public URL of the Cloud Run service"
  value       = google_cloud_run_v2_service.app.uri
}

output "db_connection_name" {
  description = "Cloud SQL instance connection name"
  value       = google_sql_database_instance.main.connection_name
}

output "assets_bucket" {
  description = "GCS bucket for user uploads / static assets"
  value       = google_storage_bucket.assets.name
}

output "artifact_registry_repo" {
  description = "Artifact Registry repo for container images"
  value       = "${google_artifact_registry_repository.images.location}-docker.pkg.dev/acme-webapp-prod/${google_artifact_registry_repository.images.repository_id}"
}

output "runtime_service_account" {
  description = "Runtime SA email used by the Cloud Run service"
  value       = google_service_account.app_runtime.email
}

output "deployer_service_account" {
  description = "Deployer SA email used by CI"
  value       = google_service_account.deployer.email
}
