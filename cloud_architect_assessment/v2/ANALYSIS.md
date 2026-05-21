# v2 design analysis

**KEEP PRIVATE** (interviewer calibration) — summary of how v2 maps to the team's requirements.

## Problem statement (v1 gap)

v1 tests whether candidates can **refactor Terraform** and reason about multi-tenant state. It deliberately avoids "find the typo" puzzles because AI solves syntax quickly.

v2 fills the gap for hires who must **own CI/CD and production incidents**: Cloud Build substitutions, Docker build-args, `gcloud run deploy` env semantics, Cloud Run auth, and GCS IAM — failures the team sees after `terraform apply`.

## Intentional bug → learning objective

| ID | Seeded issue | Skill tested | Strong fix | Low / reject |
|----|--------------|--------------|------------|--------------|
| — | APIs not in Terraform | Bootstrap discipline | `google_project_service` or `gcloud services enable` in repo | Console-only |
| 1 | Substitutions not passed to Docker | Build-time vs runtime config | `--build-arg` chain | Cloud Run env only; hardcode UI |
| 2 | `--set-env-vars` on deploy | Deploy flag semantics | `--update-env-vars` or drop flag | Re-apply Terraform each deploy |
| 3 | No `allUsers` invoker + no `--allow-unauthenticated` | Public service wiring | Terraform IAM + aligned deploy | UI-only toggle |
| 4 | GCS IAM commented out | Runtime SA ↔ bucket binding | `objectCreator` / `objectAdmin` on bucket for runtime SA | `storage.admin`, public bucket |
| 5 | `public_access_prevention` + direct GCS URL | Private object access | Signed URL (v4) | Public bucket / `allUsers` reader |
| Task | `_SERVICE_NAME` substitution | Multi-client deploy | Per-trigger substitutions | Copy entire `cloudbuild.yaml` |
| Task | No Cloud Build trigger | CI/CD automation | `google_cloudbuild_trigger` or `gcloud builds triggers create` with full subs | Console-only, wrong config path |

## Level mapping

| Level | Bugs | Time | Hire signal |
|-------|------|------|-------------|
| Beginning | 1 + manual trigger + explain pipeline | ~45m | Understands frontend env at **build** |
| Intermediate | 1–3 + trigger + naming | ~60m | Knows deploy env replacement; trigger substitutions |
| Advanced | All + IAM + signed URL | ~75–90m | Least privilege + IaC fixes |

## Discussion alignment

| Question | Acceptable answers |
|----------|-------------------|
| Cloud Build parts | steps, builders, substitutions, images |
| Dockerfile parts | multi-stage, ARG/ENV, layer order |
| Slow rebuilds | layer cache, Kaniko/cache-from, registry cache |
| Second client name | `_SERVICE_NAME`, `_CLIENT_ID` substitutions |

## v1 + v2 combined loop (optional full loop)

1. **v2** — fix deploy path and ship Hello World (operational).
2. **v1** — refactor the same Terraform for 10 clients (strategic).

Or reverse: v1 design session, homework v2 in sandbox.

## Anti-patterns scored down

- Granting **admin** roles to runtime SA for upload fixes.
- **Public bucket** as the only way to show images.
- **UI-only** fixes with no Terraform / Cloud Build commit.
- Enabling APIs only in console with no automation story for N clients.

## What v2 explicitly does not test

- Terraform module decomposition (v1).
- Cloud SQL, Secret Manager, full production stack (trimmed intentionally).
- Kubernetes / GKE.

---

See `interviewer_materials/BUGS_AND_SOLUTIONS.md` for verbatim acceptable answers during scoring.
