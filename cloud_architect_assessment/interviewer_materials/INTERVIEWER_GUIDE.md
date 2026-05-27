# Interviewer Guide — Cloud Architect Assessment

**KEEP PRIVATE — do not share with candidate.**

This is your run-of-show for the 60-minute live assessment. Pair it with:
- `SOLUTION_GUIDE.md` — what a good refactor looks like (multiple valid versions)
- `ANSWER_KEY_QUESTIONS.md` — what to listen for in the discussion
- `SCORECARD.md` — the rubric to fill out after

---

## Before the Interview (day-of, 15 min prep)

- [ ] Confirm GCP sandbox project is provisioned and candidate has IAM access
- [ ] Have a service account JSON key ready *or* be ready to grant their user identity
- [ ] Optional: pre-create a GCS bucket for state if they want one
- [ ] Pull up `SOLUTION_GUIDE.md` and `SCORECARD.md` in a separate window
- [ ] Read this file end-to-end
- [ ] Have the original `main.tf` open so you can reference line numbers if needed

### Heads-up on the Terraform file

- The hardcoded project ID in `main.tf` is `acme-webapp-prod`. Candidates will
  need to swap this to your actual assessment project ID before `terraform apply`.
  The candidate `terraform/README.md` mentions this. Confirm your project ID is
  ready to share at the start.
- The Cloud Run service uses the **public placeholder image** `gcr.io/cloudrun/hello`
  rather than a real app image, so `apply` works end-to-end in a fresh project
  without anything pre-pushed to Artifact Registry. If a candidate asks why the
  image isn't pulled from the Artifact Registry repo defined in the same file,
  the honest answer is: "It's a placeholder for the assessment — in production
  the CI pipeline would push the real image. Treat the Artifact Registry repo
  + IAM as part of the stack regardless." This is also a small signal — a
  sharp candidate may notice the apparent disconnect.

---

## Run of Show

### Minute 0–5: Intro & context

What to say:

> *"Hey, thanks for joining. This is a live, screen-share exercise. You'll be working in Terraform on GCP — I'll give you credentials in a sec. We have a real webapp stack here that's currently deployed for one client. We need to deploy it for many clients in the near future. Your job for the next hour is to set that up.*
>
> *Three things to know: First, you can use any AI tool you want — Cursor, Copilot, Claude, ChatGPT. Use them like you would on the job. Second, please think out loud. We score how you reason as much as what you produce. Third, I'm going to ask 'why' a lot. Have your reasoning ready.*
>
> *Take a minute to skim `CANDIDATE_INSTRUCTIONS.md` and `terraform/main.tf` and let me know when you're ready."*

Hand over creds. Confirm they can `terraform init`. Once they say they understand the task, start the clock.

### Minute 5–25: Task 1 (Refactor)

**Do not interrupt unless they're stuck for more than ~3 min.** Watch:

- Where they start (good signal: they read `main.tf` end-to-end first)
- How they group resources into modules (see `SOLUTION_GUIDE.md` for valid splits)
- Whether they use AI tools intelligently or paste blindly
- Whether they leave anything as a root-level resource (good — not everything should be a module)

If they ask **clarifying questions**, that's a strong signal. Examples of good ones to encourage:
- *"Are clients always in their own GCP project, or do they sometimes share one?"* → Answer: **own project**. (This matters for module design.)
- *"Is the stack identical for every client, or does it vary?"* → Answer: **mostly identical, but expect some clients to want different DB tiers or HA**. (This sets up the divergent-client question.)
- *"Where does state live today?"* → Answer: **local — and that's part of what you'd want to fix**.

If they don't ask any clarifying questions in the first 10 minutes, that's a flag. You can prompt: *"Anything you want to know about how we operate this in production?"*

**Mid-task probe** (around minute 15): pick one module they've created and ask:
> *"Why did you draw the boundary there? What goes inside this module, and what doesn't?"*

A strong candidate names a coherent principle (e.g. "this module owns everything that has its own lifecycle independent of the app" or "I grouped by failure domain"). A weak candidate says "felt right" or rephrases what's in the module.

### Minute 25–40: Task 2 (Multi-client design)

Transition:

> *"OK, let's say I now need to onboard `client-beta` next week. Walk me through what you'd add and what files you'd change. Show me, don't just tell me."*

Watch for which approach they pick. All four are defensible — see `SOLUTION_GUIDE.md` for the trade-offs. The signal is **whether they can defend their choice and acknowledge the downsides**.

Quick probe questions to use during this phase (don't ask all of them — pick 2-3):
- *"What if I told you we'll have 50 clients in 18 months?"*
- *"What if one client gets compromised — what's the blast radius?"*
- *"How is `terraform plan` for client-beta affected by uncommitted changes to client-acme?"*
- *"Where does the state live in your design?"*

### Minute 40–55: Discussion (`ARCHITECTURE_QUESTIONS.md`)

Use the candidate-facing question doc as your script. You don't need to ask all 8 — pick 4-5 that haven't been organically covered. **Always ask Q4 (divergent client)** and **Q5 (blast radius)** — these are the strongest differentiators.

For each question, use `ANSWER_KEY_QUESTIONS.md` to recognize a good answer vs. a tool-name-drop. A strong answer describes a *pattern* (idempotency, canary rollouts, version pinning, blue-green); a weak answer names a *tool* without unpacking what design property it provides.

### Minute 55–60: Wrap-up

> *"Last few minutes — anything you'd like to ask about the role, the team, or the stack? Or anything you wish I'd asked you about?"*

Their question matters. A strong candidate asks something specific about the team's operational maturity, on-call, or the multi-cloud strategy. A weak candidate asks about compensation or has no question.

---

## Red Flags (Stop the clock if you see these)

| Flag | Why it matters |
|------|---------------|
| Cannot read and explain the monolith after 5 min | Not actually Terraform-fluent |
| Pastes the whole file into ChatGPT and reads back the answer | Not using AI as a tool — being driven by it |
| Every answer is a product/tool name (Atlantis, Terragrunt, Spacelift) without explaining the pattern underneath | Tool-dependent, not a pattern-thinker — a common anti-signal in this role |
| Cannot name a single downside of their own design | No real production scars |
| Asks zero clarifying questions in the first 15 min | Will build the wrong thing on day one of the job |

## Green Flags

| Flag | Why it matters |
|------|---------------|
| Asks "are clients always in their own project?" before writing anything | Designs from constraints, not defaults |
| Leaves something as a root-level resource and can explain why | Knows that not everything benefits from abstraction |
| Names a downside of their chosen approach unprompted | Real production experience |
| When asked "how would this work in AWS", swaps providers in their head and identifies which parts break | Cloud-agnostic thinking |
| Explicitly says "I'd want to test this against state locking with 10 clients applying at once" | Operational awareness |

---

## Pacing Adjustments

**Candidate ahead of schedule (finishes Task 1 by minute 15)**
- Add: *"Now I want you to also add a per-client log sink that ships to a central audit project. How does it fit your module design?"*
- Or: *"What if we also need a CDN in front of Cloud Run — Cloud Load Balancer with Cloud CDN. Where does that live?"*

**Candidate behind schedule (Task 1 not done at minute 30)**
- Cut Task 2 to verbal only: *"You don't need to code this. Talk me through what you'd do for client-beta if you had another hour."*
- This still gives you signal — and it's a signal in itself that they couldn't finish.

**Candidate visibly stuck (>3 min on one thing)**
- Offer a small nudge: *"What if you started by just pulling out the database-related resources into one module?"*
- The fact that they needed a nudge goes in the scorecard. The quality of what they do with it tells you whether they're junior-but-coachable vs. mis-leveled.

---

## After the Interview

- [ ] Fill `SCORECARD.md` within 24 hours
- [ ] Note specific quotes — they're more useful than scores when comparing candidates later
- [ ] Forward your scorecard to the hiring panel

---

## Calibration Notes

The most reliable anti-signal in this role is what we call **tool-name dropping**: when every architectural answer reduces to a product or service name without unpacking the underlying design property. Examples:

- *"How would you handle multi-cloud?"* → "Use Terragrunt." (Doesn't explain what abstraction layer Terragrunt provides, or why.)
- *"How do you orchestrate cross-cloud?"* → "Step Functions." (Doesn't address the actual question, which is about idempotency and state.)
- *"How do you handle vendor lock-in?"* → "Just use Cloud Build for everything." (The opposite of an answer.)

A candidate who answers this way usually completes the refactor (Task 1) competently — they've done IaC before — but struggles on Q4 (divergent client) and Q5 (blast radius), because both require pattern-level reasoning that isn't reducible to a tool name. They also tend to answer Q6 (Cloud-agnostic) by listing AWS resource names instead of describing what survives a re-platform.

Use this as your calibration baseline. Anyone who clearly **leads with the pattern and only names a tool to illustrate the pattern** is what we're hiring for.
