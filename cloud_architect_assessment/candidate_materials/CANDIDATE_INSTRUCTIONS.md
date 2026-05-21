# Cloud Architect Assessment — Modularization Track

Welcome, and thanks for taking the time. This is a **60-minute live exercise** done over screen-share.

> **Other track:** For the hands-on **deploy & debug** exercise (Cloud Build, Cloud Run, seeded bugs), see [`CANDIDATE_INSTRUCTIONS_DEPLOY.md`](CANDIDATE_INSTRUCTIONS_DEPLOY.md).

## The Setup

We run a webapp that we deploy to **multiple client tenants**. Each client gets their own isolated stack on GCP — their own database, their own Cloud Run service, their own storage bucket, their own secrets. Today, we have one client (`client-acme`) deployed via a single monolithic Terraform file.

We're about to onboard several more clients (`client-beta`, `client-gamma`, and more after that). Before we do, we need someone to set the foundation properly.

**That someone is you, for the next 60 minutes.**

## What You Have

In `terraform/` you'll find:

- **`main.tf`** — the monolithic Terraform that deploys our webapp stack for `client-acme`. It works. It's just not built to scale to many clients.
- **`variables.tf`** — input variables (currently flat)
- **`outputs.tf`** — outputs from the stack
- **`terraform.tfvars.example`** — example values
- **`README.md`** — a brief description of the stack

Your interviewer will give you:
- GCP project access (or a sandbox)
- Service account credentials, if needed
- A scratch GCS bucket for Terraform state, if you want one

## Your Tasks

### Task 1 — Refactor the monolith into modules (~20 min)

Take `main.tf` and break it into a sensible module structure. Use your judgment on:

- Which resources belong together in a module
- Which resources are better left at the root
- Module inputs, outputs, locals
- How to keep the result **readable** for the next engineer

You don't need to actually run `terraform apply` end-to-end. `terraform init` and `terraform validate` on your refactor is enough to show it's structurally sound. If you `plan` against the sandbox project, even better.

### Task 2 — Design for multiple clients (~15 min)

Now show us how a **second client (`client-beta`) is onboarded** with minimal effort. Some things to consider:

- How is per-client config separated from shared logic?
- How is Terraform state organized when there are 10 clients? 50?
- What happens if one client needs a slightly different topology than the others (e.g., they want a Cloud SQL HA replica, others don't)?
- How do you prevent a bad change from hitting all clients at once?

You can choose your approach — workspaces, separate root modules per client, `for_each` over a clients map, separate state files, or something else. We care about the **reasoning**, not the specific tool choice.

### Task 3 — Discussion (~15 min)

Your interviewer will work through the questions in `ARCHITECTURE_QUESTIONS.md` with you. These are deliberately open-ended. There are no single right answers.

## Ground Rules

- ✅ **Think out loud.** We're scoring how you reason, not just what you produce.
- ✅ **AI tools are allowed** (Cursor, Copilot, Claude, ChatGPT). Use them like you would on the job.
- ✅ **Ask clarifying questions** any time. Vague requirements are deliberate — we want to see what you ask.
- ✅ **It's fine to say "I don't know"** or "I'd look that up." We value transparency.
- ✅ **Trade-offs over absolutes.** "It depends, and here's why" is a better answer than "always do X."

## Timing Targets

A skilled candidate typically finishes Tasks 1 & 2 in ~30 min and uses the rest for discussion. If you're slower, that's fine — we'd rather you do a thoughtful job than a rushed one. Your interviewer will manage the clock.

## What We're Looking For

- A clean, defensible module boundary
- A multi-client design you can explain in plain English
- Awareness of what could go wrong at scale
- Honest reasoning about trade-offs (you should be able to argue *against* your own design too)

What we're **not** looking for:
- Memorized resource names — Google it, use docs
- Perfect Terraform syntax — `terraform validate` is enough
- A complete, working apply — design clarity matters more

Good luck. 🏗️
