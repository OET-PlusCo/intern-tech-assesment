###############################################################################
# Variables — currently flat. Most config is hardcoded directly in main.tf.
# Part of the assessment is deciding what should become variables, and
# at which level (root, module, locals).
###############################################################################

variable "image_tag" {
  description = "Container image tag to deploy"
  type        = string
  default     = "latest"
}
