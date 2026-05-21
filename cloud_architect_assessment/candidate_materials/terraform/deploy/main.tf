###############################################################################
# Webapp Stack — deploy track base infrastructure (post-apply: use Cloud Build)
#
# Intentional assessment gaps (candidates fix during session):
#   - APIs are NOT auto-enabled (enable via Terraform or gcloud)
#   - Cloud Run is NOT publicly invokable (Bug 3)
#   - Runtime SA may lack GCS permissions for uploads (Bug 4)
#   - Assets bucket is private (Bug 5 — need signed URLs in app/Terraform)
###############################################################################

terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "random_id" "suffix" {
  byte_length = 4
}

###############################################################################
# NOTE: google_project_service resources are deliberately OMITTED.
# If apply fails with "API not enabled", candidates should enable APIs via
# Terraform or gcloud — UI-only fix scores lowest.
###############################################################################

resource "google_service_account" "app_runtime" {
  account_id   = "${var.client_slug}-webapp-runtime"
  display_name = "${var.client_id} webapp runtime"
  project      = var.project_id
}

resource "google_service_account" "deployer" {
  account_id   = "${var.client_slug}-webapp-deployer"
  display_name = "${var.client_id} webapp deployer"
  project      = var.project_id
}

resource "google_artifact_registry_repository" "images" {
  location      = var.region
  repository_id = "${var.client_slug}-webapp"
  description   = "${var.client_id} container images"
  format        = "DOCKER"
  project       = var.project_id
}

resource "google_artifact_registry_repository_iam_member" "deployer_writer" {
  project    = var.project_id
  location   = google_artifact_registry_repository.images.location
  repository = google_artifact_registry_repository.images.name
  role       = "roles/artifactregistry.writer"
  member     = "serviceAccount:${google_service_account.deployer.email}"
}

resource "google_artifact_registry_repository_iam_member" "runtime_reader" {
  project    = var.project_id
  location   = google_artifact_registry_repository.images.location
  repository = google_artifact_registry_repository.images.name
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:${google_service_account.app_runtime.email}"
}

resource "google_storage_bucket" "assets" {
  name          = "${var.client_slug}-webapp-assets-${random_id.suffix.hex}"
  location      = "US"
  project       = var.project_id
  force_destroy = true

  uniform_bucket_level_access = true

  # Private bucket — objects are not public (Bug 5)
  public_access_prevention = "enforced"
}

# BUG 4 (intentional): objectAdmin binding commented out — uploads fail until fixed
# resource "google_storage_bucket_iam_member" "runtime_object_admin" {
#   bucket = google_storage_bucket.assets.name
#   role   = "roles/storage.objectAdmin"
#   member = "serviceAccount:${google_service_account.app_runtime.email}"
# }

resource "google_cloud_run_v2_service" "app" {
  name     = "${var.client_slug}-webapp"
  location = var.region
  project  = var.project_id

  # Public access disabled at service level (Bug 3 — pair with IAM + deploy flags)
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.app_runtime.email

    scaling {
      min_instance_count = 0
      max_instance_count = 5
    }

    containers {
      image = "gcr.io/cloudrun/hello"

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }

      env {
        name  = "CLIENT_ID"
        value = var.client_id
      }

      env {
        name  = "ASSETS_BUCKET"
        value = google_storage_bucket.assets.name
      }

      env {
        name  = "APP_GREETING"
        value = "Hello from Terraform (runtime)"
      }
    }
  }
}

# BUG 3 (intentional): public invoker NOT granted — candidate enables in Terraform and/or Cloud Build
# resource "google_cloud_run_v2_service_iam_member" "public" {
#   project  = google_cloud_run_v2_service.app.project
#   location = google_cloud_run_v2_service.app.location
#   name     = google_cloud_run_v2_service.app.name
#   role     = "roles/run.invoker"
#   member   = "allUsers"
# }

resource "google_cloud_run_v2_service_iam_member" "deployer_admin" {
  project  = google_cloud_run_v2_service.app.project
  location = google_cloud_run_v2_service.app.location
  name     = google_cloud_run_v2_service.app.name
  role     = "roles/run.admin"
  member   = "serviceAccount:${google_service_account.deployer.email}"
}
