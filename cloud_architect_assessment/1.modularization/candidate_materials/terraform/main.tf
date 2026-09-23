###############################################################################
# Webapp Stack — Monolithic Terraform
#
# This deploys our customer-facing webapp for a single client (client-acme).
# Stack components:
#   - Cloud Run service (the app itself)
#   - Cloud SQL Postgres instance (app database)
#   - GCS bucket (user uploads / static assets)
#   - Artifact Registry repo (container images)
#   - Secret Manager (DB password, API keys)
#   - Service accounts and IAM bindings
#   - Cloud Run service IAM (who can invoke the app)
#
# This file currently works. It deploys client-acme's stack successfully.
# Your job is to evolve it so we can deploy 10+ clients without copying this
# file 10 times.
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
  project = "acme-webapp-prod"
  region  = "us-central1"
}

###############################################################################
# Random suffix for globally-unique resource names (buckets, etc.)
###############################################################################

resource "random_id" "suffix" {
  byte_length = 4
}

###############################################################################
# Enable required APIs
###############################################################################

resource "google_project_service" "run" {
  project = "acme-webapp-prod"
  service = "run.googleapis.com"

  disable_on_destroy = false
}

resource "google_project_service" "sqladmin" {
  project = "acme-webapp-prod"
  service = "sqladmin.googleapis.com"

  disable_on_destroy = false
}

resource "google_project_service" "secretmanager" {
  project = "acme-webapp-prod"
  service = "secretmanager.googleapis.com"

  disable_on_destroy = false
}

resource "google_project_service" "artifactregistry" {
  project = "acme-webapp-prod"
  service = "artifactregistry.googleapis.com"

  disable_on_destroy = false
}

###############################################################################
# Service Accounts
###############################################################################

# Runtime SA for the Cloud Run service
resource "google_service_account" "app_runtime" {
  account_id   = "acme-webapp-runtime"
  display_name = "client-acme webapp runtime"
  project      = "acme-webapp-prod"
}

# Deployer SA used by CI to push images and deploy revisions
resource "google_service_account" "deployer" {
  account_id   = "acme-webapp-deployer"
  display_name = "client-acme webapp deployer"
  project      = "acme-webapp-prod"
}

###############################################################################
# Artifact Registry — container images for this client
###############################################################################

resource "google_artifact_registry_repository" "images" {
  location      = "us-central1"
  repository_id = "acme-webapp"
  description   = "client-acme webapp container images"
  format        = "DOCKER"
  project       = "acme-webapp-prod"

  depends_on = [google_project_service.artifactregistry]
}

resource "google_artifact_registry_repository_iam_member" "deployer_writer" {
  project    = "acme-webapp-prod"
  location   = google_artifact_registry_repository.images.location
  repository = google_artifact_registry_repository.images.name
  role       = "roles/artifactregistry.writer"
  member     = "serviceAccount:${google_service_account.deployer.email}"
}

resource "google_artifact_registry_repository_iam_member" "runtime_reader" {
  project    = "acme-webapp-prod"
  location   = google_artifact_registry_repository.images.location
  repository = google_artifact_registry_repository.images.name
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:${google_service_account.app_runtime.email}"
}

###############################################################################
# GCS Bucket — user uploads / static assets
###############################################################################

resource "google_storage_bucket" "assets" {
  name          = "acme-webapp-assets-${random_id.suffix.hex}"
  location      = "US"
  project       = "acme-webapp-prod"
  force_destroy = false

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type = "Delete"
    }
  }
}

resource "google_storage_bucket_iam_member" "runtime_object_admin" {
  bucket = google_storage_bucket.assets.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.app_runtime.email}"
}

###############################################################################
# Secret Manager — DB password and external API keys
###############################################################################

resource "random_password" "db_password" {
  length  = 32
  special = true
}

resource "google_secret_manager_secret" "db_password" {
  secret_id = "acme-webapp-db-password"
  project   = "acme-webapp-prod"

  replication {
    auto {}
  }

  depends_on = [google_project_service.secretmanager]
}

resource "google_secret_manager_secret_version" "db_password" {
  secret      = google_secret_manager_secret.db_password.id
  secret_data = random_password.db_password.result
}

resource "google_secret_manager_secret_iam_member" "runtime_db_password_reader" {
  project   = "acme-webapp-prod"
  secret_id = google_secret_manager_secret.db_password.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.app_runtime.email}"
}

resource "google_secret_manager_secret" "api_key_stripe" {
  secret_id = "acme-webapp-stripe-api-key"
  project   = "acme-webapp-prod"

  replication {
    auto {}
  }

  depends_on = [google_project_service.secretmanager]
}

resource "google_secret_manager_secret_iam_member" "runtime_stripe_reader" {
  project   = "acme-webapp-prod"
  secret_id = google_secret_manager_secret.api_key_stripe.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.app_runtime.email}"
}

###############################################################################
# Cloud SQL Postgres — app database
###############################################################################

resource "google_sql_database_instance" "main" {
  name             = "acme-webapp-db-${random_id.suffix.hex}"
  database_version = "POSTGRES_15"
  region           = "us-central1"
  project          = "acme-webapp-prod"

  settings {
    tier              = "db-custom-1-3840"
    availability_type = "ZONAL" # single-zone for acme
    disk_size         = 20
    disk_type         = "PD_SSD"

    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
      start_time                     = "03:00"
    }

    ip_configuration {
      ipv4_enabled = true
      # Locked down to specific networks in production.
      authorized_networks {
        name  = "all"
        value = "0.0.0.0/0"
      }
    }
  }

  deletion_protection = false

  depends_on = [google_project_service.sqladmin]
}

resource "google_sql_database" "app" {
  name     = "appdb"
  instance = google_sql_database_instance.main.name
  project  = "acme-webapp-prod"
}

resource "google_sql_user" "app" {
  name     = "appuser"
  instance = google_sql_database_instance.main.name
  password = random_password.db_password.result
  project  = "acme-webapp-prod"
}

###############################################################################
# Cloud Run — the webapp
###############################################################################

resource "google_cloud_run_v2_service" "app" {
  name     = "acme-webapp"
  location = "us-central1"
  project  = "acme-webapp-prod"

  template {
    service_account = google_service_account.app_runtime.email

    scaling {
      min_instance_count = 1
      max_instance_count = 10
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
        value = "client-acme"
      }

      env {
        name  = "DB_HOST"
        value = google_sql_database_instance.main.public_ip_address
      }

      env {
        name  = "DB_NAME"
        value = google_sql_database.app.name
      }

      env {
        name  = "DB_USER"
        value = google_sql_user.app.name
      }

      env {
        name = "DB_PASSWORD"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.db_password.secret_id
            version = "latest"
          }
        }
      }

      env {
        name = "STRIPE_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.api_key_stripe.secret_id
            version = "latest"
          }
        }
      }

      env {
        name  = "ASSETS_BUCKET"
        value = google_storage_bucket.assets.name
      }
    }
  }

  depends_on = [
    google_project_service.run,
    google_secret_manager_secret_version.db_password,
  ]
}

# Make the service publicly invokable (this client is a public-facing webapp)
resource "google_cloud_run_v2_service_iam_member" "public" {
  project  = google_cloud_run_v2_service.app.project
  location = google_cloud_run_v2_service.app.location
  name     = google_cloud_run_v2_service.app.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Deployer can deploy new revisions
resource "google_cloud_run_v2_service_iam_member" "deployer_admin" {
  project  = google_cloud_run_v2_service.app.project
  location = google_cloud_run_v2_service.app.location
  name     = google_cloud_run_v2_service.app.name
  role     = "roles/run.admin"
  member   = "serviceAccount:${google_service_account.deployer.email}"
}
