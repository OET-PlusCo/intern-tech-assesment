variable "project_id" {
  description = "GCP project ID"
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
