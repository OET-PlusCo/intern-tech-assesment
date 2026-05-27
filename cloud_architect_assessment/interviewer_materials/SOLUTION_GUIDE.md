# Solution Guide — Cloud Architect Assessment

**KEEP PRIVATE — do not share with candidate.**

This document shows **multiple valid solutions** for both Task 1 (modularization) and Task 2 (multi-client design). It's a reference so you can recognize good work in real time — not a single "correct" answer to grade against.

A common anti-pattern in this role is candidates who name tools rather than describe designs; this assessment is calibrated so a candidate who actually understands the trade-offs scores higher than one who memorized which Terraform features exist.

---

## Task 1 — Modularization

There are **at least 4 valid module decompositions** for `main.tf`. None is universally correct; the candidate should be able to **defend their choice and name the downsides**.

### Approach A — "Group by Resource Family" (most common, safe choice)

```
modules/
├── database/        # cloud_sql_instance, database, user, db_password secret + IAM
├── storage/         # gcs bucket + IAM
├── service/         # cloud_run service + service IAM
├── registry/        # artifact_registry + IAM
└── identity/        # service accounts (runtime + deployer)
```

**Pros:** Easy to reason about, clear separation, each module maps to a service line.
**Cons:** A lot of cross-module wiring at the root — e.g., the `service` module needs outputs from `database`, `storage`, `identity`, and `registry`. Root file ends up being a giant "wire it together" block.

### Approach B — "Single Tenant Module" (KISS, often best for this use case)

```
modules/
└── client-stack/    # everything that comprises one client's stack
```

Root `main.tf`:
```hcl
module "acme" {
  source    = "./modules/client-stack"
  client_id = "acme"
  project   = "acme-webapp-prod"
  region    = "us-central1"
  db_tier   = "db-custom-1-3840"
  # ...
}
```

**Pros:** A new client is a single module block at the root. The internal grouping is irrelevant from the outside — encapsulation done right. State and blast radius align with the natural unit of work (one client).
**Cons:** Heavier module file, less granular reuse. If two different consumers need just the database without the rest, this is wrong.

**This is often the best answer for this exact use case** (multi-tenant identical stacks). Senior candidates frequently land here. Don't penalize Approach A — but if a candidate lands on B and can explain *why* over A, that's a strong signal.

### Approach C — "Stateful vs. Stateless Split"

```
modules/
├── persistent/      # Cloud SQL, GCS, Secrets — things you DO NOT want to destroy
└── ephemeral/       # Cloud Run, IAM bindings — safe to recreate
```

**Pros:** Aligns module boundaries with **risk of accidental destruction**. You can put `prevent_destroy` lifecycle on the persistent module and iterate freely on ephemeral. State separation between the two reduces blast radius on the dangerous stuff.
**Cons:** Less intuitive to a newcomer. The ephemeral module depends heavily on persistent outputs (DB connection string, bucket name) — tight coupling across the boundary.

This is a sophisticated answer. If a candidate volunteers it unprompted, it's a strong signal of production scars.

### Approach D — "Layered" (data, compute, edge)

```
modules/
├── data/            # Cloud SQL + GCS + Secrets
├── compute/         # Cloud Run + runtime SA
├── platform/        # Artifact Registry + deployer SA
└── access/          # public invoker IAM, cross-module bindings
```

**Pros:** Mirrors how teams often divide ownership (data team, platform team, app team).
**Cons:** Over-engineered for one webapp. Reasonable if you have a real org boundary to respect; over-kill otherwise.

---

## What should NOT become a module

A good candidate explicitly **leaves at least one thing at the root** and explains why. Examples:

| Resource | Why keep at root |
|----------|-----------------|
| `random_id.suffix` | One-off, used by multiple modules as input — naturally a root concern |
| `google_project_service.*` (API enablement) | Project-level concern, not stack-level. Often pre-provisioned outside Terraform anyway |
| Provider blocks | Cannot live inside child modules (per Terraform 1.5+ best practice for re-usable modules) |
| `terraform { backend ... }` blocks | Must be at root, by definition |

A candidate who wraps everything in modules and has zero root-level resources has probably over-engineered. Probe with: *"Is there anything you considered making a module but decided against?"*

---

## What good module signatures look like

For Approach B (`client-stack`), expect a `variables.tf` like:

```hcl
variable "client_id"  { type = string }
variable "project_id" { type = string }
variable "region"     { type = string }

variable "db_tier" {
  type    = string
  default = "db-custom-1-3840"
}

variable "db_high_availability" {
  type    = bool
  default = false
}

variable "min_instances" {
  type    = number
  default = 1
}

variable "max_instances" {
  type    = number
  default = 10
}

variable "extra_secrets" {
  type    = map(string)
  default = {}
  description = "Additional secret_id → description map for per-client API keys"
}
```

**Good signals in variables:**
- Sensible defaults for things most clients won't override
- `db_high_availability` as a knob (or similar) — they thought about the divergent-client problem
- `extra_secrets` as a map — they thought about extensibility

**Red flag:** A variable for *every* hardcoded value in the original `main.tf`. That's mechanical translation, not design.

---

## Locals — where they should appear

Strong candidates use `locals` to compute derived values, especially names:

```hcl
locals {
  resource_prefix = "${var.client_id}-webapp"
  labels = {
    client      = var.client_id
    managed_by  = "terraform"
    environment = "prod"
  }
}
```

Then `name = "${local.resource_prefix}-db"` everywhere. This is the right answer to "how do you avoid hardcoding `acme` in 17 places".

---

## Task 2 — Multi-Client Design

There are **4 well-known approaches**. Each has clear trade-offs. The signal is **which one they pick AND whether they can name the downsides**.

### Pattern 1 — Terraform Workspaces

```sh
terraform workspace new client-beta
terraform workspace select client-beta
terraform apply -var-file=clients/beta.tfvars
```

State separated by workspace. Same code, different variables per workspace.

**Pros:** Built-in. No directory restructuring.
**Cons:**
- All workspaces share the same backend config and *the same code revision* at any given time. If you're mid-rollout, half your clients are on old code, half on new — and the state files all live in the same bucket prefix.
- It's easy to `terraform apply` against the wrong workspace by accident. Production incidents have come from this exact mistake.
- HashiCorp's own docs say not to use workspaces for environment separation. The same caveat applies to tenant separation.

**Verdict from interviewers:** Acceptable for small N (≤5 clients). Not what you want for 50.

### Pattern 2 — Directory per Client (separate root modules)

```
deployments/
├── client-acme/
│   ├── main.tf       # one line: module "stack" { source = "../../modules/client-stack" ... }
│   ├── terraform.tfvars
│   └── backend.tf    # state lives in acme's GCS bucket
├── client-beta/
│   └── ...
└── client-gamma/
    └── ...
modules/
└── client-stack/     # the shared module
```

**Pros:**
- Hard isolation: each client has its own state, its own backend, its own apply pipeline.
- A bad apply for one client cannot touch another. **Smallest possible blast radius.**
- Per-client overrides are trivial: just edit that client's `main.tf`/`tfvars`.
- Maps cleanly to per-client CI pipelines, per-client approval gates.

**Cons:**
- Onboarding a new client = creating a new directory. With a generator script this is fine; manual is annoying.
- Hard to perform a fleet-wide change (you have to iterate or use a wrapper tool).
- Duplication across the per-client `main.tf` files (mitigated if it's just one `module` block).

**Verdict from interviewers:** This is the **canonical "right" answer** for many-tenants-with-strong-isolation. Strongly preferred for production multi-tenant SaaS.

### Pattern 3 — `for_each` Over a Clients Map (single state)

```hcl
locals {
  clients = {
    acme = {
      project_id = "acme-webapp-prod"
      db_tier    = "db-custom-1-3840"
    }
    beta = {
      project_id = "beta-webapp-prod"
      db_tier    = "db-custom-2-7680"
    }
  }
}

module "client_stack" {
  source   = "./modules/client-stack"
  for_each = local.clients

  client_id  = each.key
  project_id = each.value.project_id
  db_tier    = each.value.db_tier
}
```

**Pros:**
- Onboarding a new client is a 3-line addition to the locals map. Fastest onboarding of any pattern.
- One place to see all clients.

**Cons:**
- **Single state file holds all clients.** State corruption or accidental destroy hits everyone.
- A `terraform plan` shows changes for all clients at once. Diffs get huge. Approvers get desensitized.
- `terraform apply` is all-or-nothing — you can't easily roll out to just one client to test.
- The first time someone accidentally renames a map key, every resource for that client gets destroyed and recreated. Real outage waiting to happen.
- Doesn't scale operationally past ~10 clients in practice.

**Verdict from interviewers:** Tempting because it's elegant. Wrong choice for production. **Asking a candidate "what's wrong with this approach?" is a great probe** — strong candidates name the single-state-file risk immediately. Tool-namer candidates often think it's the right answer because it looks DRY.

### Pattern 4 — Terragrunt / Spacelift / Atlantis wrapper

Wrapper tool generates per-client root modules from a single source of truth.

**Pros:** Get the directory-per-client isolation of Pattern 2 with less repetition.
**Cons:** Adds tooling. Adds onboarding cost for new engineers. Adds another thing to break.

**Verdict from interviewers:** Reasonable for larger teams that already use Terragrunt. **If a candidate says "I'd use Terragrunt" without naming the underlying isolation pattern it provides, that's the tool-namer anti-pattern — they're naming the tool, not the design.** Push back: *"What if we didn't want to add Terragrunt? What design would still work?"*

---

## What "great" looks like across both tasks

A great candidate does roughly this:

1. **Reads `main.tf` end-to-end first** before touching anything.
2. **Asks ≥2 clarifying questions** about how clients map to projects, whether stacks vary, and where state lives.
3. **Picks Approach B (single client-stack module)** or has a coherent reason for picking A.
4. **Leaves provider, backend config, and one or two cross-cutting resources at root.**
5. **Uses `locals` for naming and labels** — not 17 string concatenations inline.
6. **Picks Pattern 2 (directory-per-client)** for multi-client, or Pattern 4 with explicit acknowledgment that it's just a wrapper around Pattern 2.
7. **Spontaneously names a downside** of whichever pattern they chose.
8. **Handles the divergent-client question** by adding optional inputs with defaults to the module, not by forking it.
9. **Identifies state locking, blast radius, and per-client backend buckets** as real concerns without prompting.
10. **Can answer "would this work on AWS?"** by talking about the abstraction layer, not the resource names.

---

## What "barely passing" looks like

- Approach A, mechanically extracted, no clear principle behind boundaries
- Variables for every hardcoded value, no defaults, no locals
- Picks Pattern 3 (single state, `for_each`) because it "looks clean"
- When asked about downsides: shrugs or rephrases the upside as the downside
- Cannot articulate why a `resource` would ever beat a `module`
- Answers Q6 (Cloud-agnostic) by listing AWS resource names

This is a "Maybe" or "No Hire" depending on other signals.

---

## Cheat sheet — the four hardest questions and what to listen for

| Question | Weak answer | Strong answer |
|----------|-------------|---------------|
| Monolith vs. modules | "Always modularize" | "For very simple stacks or one-off scripts, modules add overhead with no payoff. Modularize when there are ≥2 consumers, or when the module boundary maps to a real failure/ownership domain." |
| When use `resource` over `module` | "Always use modules" | "When the resource is used exactly once, has no compound logic, and wouldn't benefit from inputs. Wrapping a single resource in a single-line module is just indirection." |
| 50-client scale | "Workspaces" | "I'd want per-client state files, ideally per-client backends. Workspaces share a code revision across all tenants — that's a rollout-safety issue, not a scale issue. With 50 clients I'd want a per-client directory generated from a template, with a CI pipeline keyed by directory diff." |
| Divergent client | "Fork the module" | "Optional inputs with sensible defaults. The module's surface grows but doesn't fragment. If the divergence is large enough that defaults won't cover it, that's the signal to introduce a new module — not to fork the existing one." |

---

End of solution guide.
