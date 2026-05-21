output "service_url" {
  description = "Cloud Run service URL (may return 403 until public access is fixed)"
  value       = google_cloud_run_v2_service.app.uri
}

output "service_name" {
  description = "Cloud Run service name"
  value       = google_cloud_run_v2_service.app.name
}

output "assets_bucket" {
  description = "Private GCS bucket for uploads"
  value       = google_storage_bucket.assets.name
}

output "artifact_registry_repo" {
  description = "Docker repository path for Cloud Build image tag"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.images.repository_id}"
}

output "runtime_service_account" {
  value = google_service_account.app_runtime.email
}

output "deployer_service_account" {
  value = google_service_account.deployer.email
}
