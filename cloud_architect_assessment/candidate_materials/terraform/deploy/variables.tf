variable "project_id" {
  description = "GCP project ID for the assessment sandbox"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "client_id" {
  description = "Logical client identifier (e.g. client-acme)"
  type        = string
  default     = "client-acme"
}

variable "client_slug" {
  description = "Short slug used in resource names (e.g. acme)"
  type        = string
  default     = "acme"
}

variable "create_cloudbuild_trigger" {
  description = "Create Cloud Build trigger (requires Cloud Source repo — see cloudbuild/TRIGGER.md)"
  type        = bool
  default     = false
}

variable "source_repo_name" {
  description = "Cloud Source Repositories name for push trigger"
  type        = string
  default     = "intern-tech-assessment"
}
