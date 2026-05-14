# Answer Key — Discussion Questions

**KEEP PRIVATE — do not share with candidate.**

For each of the 8 questions in `candidate_materials/ARCHITECTURE_QUESTIONS.md`, this doc shows:
- 🟢 **Strong answer** — what to listen for
- 🟡 **Acceptable answer** — passable, ask follow-ups
- 🔴 **Weak answer** — the tool-namer anti-pattern (names a tool instead of describing a pattern)
- 🔬 **Probe questions** — to dig deeper if the answer is short

---

## Q1 — Monolith vs. Modules

> *"When would you deliberately leave something as a monolith and not modularize it?"*

🟢 **Strong:**
- "When there's no second consumer. A module's value is reuse + encapsulation; if there's exactly one caller, a module is just indirection."
- "When the stack is small enough that the module overhead (extra files, inputs/outputs, mental jumps) costs more than the duplication."
- "Early in a project before you understand the right boundary. Premature modularization locks in the wrong abstraction."
- "For one-off scripts, throwaway infra, and proofs-of-concept."

🟡 **Acceptable:** Names one of the above without naming the others. Push for more.

🔴 **Weak:**
- "Always modularize — modules are a best practice."
- "When I'm using a tool that doesn't support modules" (irrelevant tool reference).

🔬 **Probe:**
- *"Have you ever modularized something and regretted it? What happened?"*
- *"What's the cost of the wrong abstraction?"*

---

## Q2 — Resource vs. Module

> *"At what point does a resource block deserve to become its own module?"*

🟢 **Strong:**
- "When there are ≥2 callers, or when the resource is part of a coherent compound (e.g., a GCS bucket plus its IAM bindings plus its lifecycle config are one unit)."
- "When wrapping it in a module forces you to express *intent* rather than mechanics. `module.database` is more readable than five `google_sql_*` blocks."
- "When the resource has its own lifecycle or ownership."

🟡 **Acceptable:** "When it's used more than once." (True but shallow.)

🔴 **Weak:**
- "Everything should be a module."
- "When the docs say so."

🔬 **Probe:**
- *"Show me where in your refactor you left a resource at root. Why?"*

---

## Q3 — 50/100 Clients

> *"You have 10 clients today. Imagine 100 in two years. Does your design still work? What breaks first?"*

🟢 **Strong (depending on what they chose for Task 2):**
- **If they chose Pattern 2 (dir-per-client):** "The CI pipeline becomes the bottleneck. Running a plan across 100 directories on every PR is slow. I'd want PR-time plans only on the changed directories, plus a separate scheduled drift check that fans out."
- **If they chose Pattern 3 (`for_each`):** "It doesn't. State file becomes huge, `plan` runs forever, and one bad change blasts everyone. At 100 I'd have to migrate to per-client states. I'd start that migration around client 10-15."
- "State locking. With one shared bucket prefix and concurrent applies, you'll see lock contention."
- "IAM sprawl. Per-client deployer SAs across 100 projects becomes its own admin problem — I'd want a clear lifecycle for credential rotation and offboarding."

🟡 **Acceptable:** Names one of {state, plan time, IAM} without others.

🔴 **Weak:**
- "Just throw more CI runners at it."
- "I'd switch to <some product>" without explaining what scaling property of that product helps.

🔬 **Probe:**
- *"What's the first thing that breaks?"*
- *"At what client count would you migrate from one approach to another?"*

---

## Q4 — Divergent Client (the most important question)

> *"Client-gamma wants Cloud SQL HA and private VPC peering. Others don't. How do you handle this without forking your modules?"*

🟢 **Strong:**
- "Add optional inputs to the module with sensible defaults. `db_high_availability = false` by default; client-gamma sets it to true. Same for `private_networking`. The module's surface area grows; it doesn't fragment."
- "If the divergence is too large for inputs to express, that's the signal to introduce a new module (e.g., `client-stack-enterprise`) — not to fork. The two modules can share lower-level sub-modules."
- "Use feature flags at the module input level, not version forks at the source level. Forks rot."

🟡 **Acceptable:**
- "I'd just add a variable for it." (Right direction, no nuance about defaults or about when to split modules.)

🔴 **Weak:**
- "Make a copy of the module for client-gamma and modify it." (Forking — guarantees drift.)
- "Use Terragrunt to override values." (Names a tool, doesn't address the abstraction question.)
- "Put it in client-gamma's `main.tf` directly as raw resources." (Breaks encapsulation; what happens at the next divergent client?)

🔬 **Probe:**
- *"Where do you draw the line between an input and a new module?"*
- *"What happens when client-gamma also wants a different storage class, and three other clients want one of the two things but not both?"*

---

## Q5 — Blast Radius (also critical)

> *"You push a change to the Cloud Run module. Walk me through what happens between merge and that change reaching all 50 clients."*

🟢 **Strong:**
- "Without rollout staging, all 50 clients pick up the change on their next apply. So step one is: applies are not automatic on module changes; they're triggered per-client by a CI pipeline I control."
- "I'd want a canary client (or a real staging tenant) that runs the new module first. Only after it's validated do the rest of the clients get the version."
- "If the module is sourced via a version pin (`source = "git::...?ref=v1.4.2"`), then changes to main don't propagate until each client's `source` ref is bumped. That gives explicit promotion."
- "Drift detection scheduled separately so I don't only learn about a bad change at the next apply."

🟡 **Acceptable:**
- Talks about staging environments but doesn't address version pinning or canary clients.

🔴 **Weak:**
- "Cloud Build would catch it" / "Tests would catch it." (Vague — what tests, what catches what?)
- "Just don't push bad changes." (Not a serious answer.)
- "Use feature flags." (Where? What flag? What does the module check?)

🔬 **Probe:**
- *"Walk me through a specific rollback. Client-gamma's apply failed at 2am — what's the playbook?"*
- *"How does a developer test their module change before the first client gets it?"*

---

## Q6 — Cloud-Agnostic Design

> *"If we have to support AWS next year, which parts of your design survive, and which parts do you throw away?"*

🟢 **Strong:**
- "The shape of the module (what a 'client stack' is — compute + db + storage + secrets + identity + registry) survives. The resource types inside it don't. So I'd keep the multi-client pattern (per-client directory, per-client state, per-client variables) and rewrite only the leaves."
- "Per-client config (tier, instance count, secrets list) is mostly the same between clouds. Resource names are different. The pattern is portable; the implementation isn't."
- "I would not try to write a single Terraform module that targets both GCP and AWS — that's where people get into trouble. I'd write two parallel modules with the same input surface."

🟡 **Acceptable:**
- "The pattern survives, the resources don't." (Correct, but shallow if they can't unpack it.)

🔴 **Weak (tool-namer):**
- "Just use Terragrunt and it handles multi-cloud." (No — that's not what Terragrunt does.)
- "Switch the provider block and most things should work." (No — resource types are different.)
- "Use Pulumi instead." (Tool answer, doesn't address the design question.)

🔬 **Probe:**
- *"Have you ever actually done a cloud migration? What was the surprise?"*
- *"Is there anything in your current design that would actively prevent porting to AWS?"*

---

## Q7 — Per-Tenant Secrets & IAM

> *"How is client-acme's database password isolated from client-beta's?"*

🟢 **Strong:**
- "Each client is in its own GCP project. Secret Manager lives in that project. IAM is scoped per project, so a misconfigured Terraform run targeting acme's project literally cannot read beta's secrets — there's no IAM binding that would resolve."
- "The deployer SA for client-acme has IAM only in client-acme's project. The blast radius of compromised deployer credentials is one client, not all clients."
- "Each client's runtime SA only has bindings on resources inside its own project."
- "The Terraform state for each client is in a separate GCS bucket in that client's project, so even state-file exfiltration is scoped per tenant."

🟡 **Acceptable:** "Different projects, different IAM." (True, no depth.)

🔴 **Weak:**
- "We trust the team not to make mistakes."
- "Naming conventions" (relies on convention, not enforcement).

🔬 **Probe:**
- *"Where could this isolation break? What's the weakest link?"*

---

## Q8 — Onboarding Speed & Cost

> *"Salesperson signs a new client at 4pm Friday — working environment by Monday. Walk me through onboarding."*

🟢 **Strong:**
- "Step 1: provision the GCP project. With org-level Terraform that's automated — under 10 minutes."
- "Step 2: add the client to the clients-config (one PR, one approval). PR-time plan shows exactly what will be created."
- "Step 3: merge → automated apply runs in the per-client pipeline. End-to-end ~30 minutes if Cloud SQL is cold."
- "What's NOT in this flow: any human SSHing anywhere, any manual secret creation, any manual IAM grant. If any of those are needed, the design is broken."
- *On cost-cutting:* "Smallest version that preserves isolation: skip the dedicated Cloud SQL HA, use shared Artifact Registry across clients (saves project-level overhead), single-region. Each cut is a known trade-off, not a default."

🟡 **Acceptable:** Lists steps but doesn't include automation or PR-time review.

🔴 **Weak:**
- "We'd run the Terraform manually." (Will not survive 50 clients.)
- "It depends." (Without naming what it depends on.)

🔬 **Probe:**
- *"What's the longest single step? Can it be parallelized?"*
- *"What's manual today that you'd want automated by client #20?"*

---

## Summary signal

After 4-5 questions you should have a clear picture:

| Pattern | What it sounds like | Verdict |
|---------|---------------------|---------|
| **Pattern-thinker** | Names abstractions (blast radius, canary, idempotency, feature flags), can map them across clouds, names downsides of their own designs | Strong Hire territory |
| **Mechanic** | Knows the syntax, knows the resources, can execute — but gets stuck when asked "why" | Hire-but-junior, calibrate against role level |
| **Tool-namer** | Answers questions with product names — "use Terragrunt", "use Cloud Build", "use Step Functions" — without articulating what design property the tool provides | No Hire for an *Architect* role, possibly hire for a senior IC role |
| **Confused** | Cannot finish refactor, cannot defend choices, gives contradictory answers | No Hire |

Always note **specific quotes** in the scorecard. They make calibration with the panel ten times easier.
