# 🏗️ Cloud Architect Assessment

Two complementary tracks:

| Track | Folder | Focus |
|-------|--------|--------|
| **v1** | `candidate_materials/` (this tree) | Terraform modularization & multi-tenant **design** (~60 min) |
| **v2** | [`v2/`](v2/) | Post-`apply` **Cloud Build / Cloud Run / IAM** debugging (~45–90 min, leveled) |

Use **v1** for architecture and module boundaries. Use **v2** for pipeline fluency, build-time env vars, deploy flags, and least-privilege IAM.

---

## v1 — Modularization assessment

A 1-hour live, shared-screen technical assessment designed to evaluate Cloud Architect candidates on **architectural reasoning** rather than rote knowledge or bug-fixing.

## 📋 Overview

| Aspect | Detail |
|--------|--------|
| **Role** | Cloud Architect |
| **Duration** | 60 min total (target: skilled candidate ~30 min, junior ~60 min) |
| **Format** | Live, shared screen, candidate may use AI tools |
| **Cloud** | GCP (access provided by interviewer) |
| **Focus** | Terraform modularization, multi-tenant deployment design, trade-off reasoning |

## 🎯 Why This Format

Because candidates can use AI tools, we deliberately avoid puzzles that ChatGPT solves in 10 seconds (syntax bugs, "find the typo", missing semicolons). Instead, we test things that AI will not do well unattended:

- **Choosing between equally valid designs** with justification
- **Knowing when not to abstract** (modules vs. resources, KISS vs. DRY)
- **Reasoning about blast radius, state, and operational pain** across many tenants
- **Articulating trade-offs in plain English**

These are the same gaps the team has seen in earlier Cloud Architect interviews: tool name-dropping instead of pattern-thinking, and difficulty answering "what would break and why".

## 📁 Folder Structure

```
cloud_architect_assessment/
│
├── README.md                          ← You are here
│
├── ✅ candidate_materials/            ← Safe to share with candidate
│   ├── CANDIDATE_INSTRUCTIONS.md      ← What they read first
│   ├── ARCHITECTURE_QUESTIONS.md      ← Design questions (open-ended)
│   └── terraform/
│       ├── main.tf                    ← The monolith they refactor
│       ├── variables.tf
│       ├── outputs.tf
│       ├── terraform.tfvars.example
│       └── README.md                  ← Context on the webapp stack
│
└── ❌ interviewer_materials/          ← KEEP PRIVATE
    ├── INTERVIEWER_GUIDE.md           ← Run-of-show and timing
    ├── SOLUTION_GUIDE.md              ← Multiple valid module designs
    ├── ANSWER_KEY_QUESTIONS.md        ← What to look for per question
    └── SCORECARD.md                   ← Scoring rubric
```

## ⏱️ Time Budget (Recommended)

| Phase | Time | What Happens |
|-------|------|--------------|
| **Intro & context** | 5 min | Walk through the stack, explain task, share GCP creds |
| **Task 1: Modularize** | 20 min | Candidate refactors `main.tf` into modules |
| **Task 2: Multi-client design** | 15 min | They show how to onboard a second client |
| **Design discussion (Q&A)** | 15 min | Open-ended architecture questions |
| **Wrap-up** | 5 min | Candidate questions, next steps |
| **Total** | **60 min** | |

A strong candidate finishes Tasks 1 & 2 in ~25-30 min, leaving room for deep discussion. A weaker candidate may need most of the hour to finish the refactor — that itself is a signal.

## 🧪 What This Tests

### Tested explicitly
- ✅ Terraform module design (inputs, outputs, locals, `for_each`)
- ✅ Multi-tenancy patterns (workspaces vs. tfvars vs. separate roots vs. `for_each`)
- ✅ State management at scale
- ✅ Blast-radius reasoning
- ✅ When to abstract vs. when to keep things flat

### Tested implicitly (through discussion)
- ✅ Cloud-agnostic thinking (would your design survive a GCP→AWS migration?)
- ✅ Operational awareness (rollout, rollback, drift)
- ✅ Cost & IAM scoping per tenant
- ✅ Communication and ability to justify decisions

### Deliberately **not** tested
- ❌ Memorized GCP resource names
- ❌ Terraform syntax trivia
- ❌ Bug hunts an AI tool would solve in seconds

## 🚦 Quick Start (Interviewer)

1. **Day before**: Provision GCP sandbox project, generate SA key or grant candidate IAM, send them the candidate folder.
2. **15 min before**: Re-read `interviewer_materials/INTERVIEWER_GUIDE.md` and `SCORECARD.md`.
3. **During**: Use `SOLUTION_GUIDE.md` to recognize valid approaches; use `ANSWER_KEY_QUESTIONS.md` to probe deeper.
4. **After**: Fill scorecard within 24 hours while it's fresh.

## 🎓 Scoring Snapshot

| Band | Score | Signal |
|------|-------|--------|
| 🌟 Strong Hire | 85-100 | Multiple valid designs, deep trade-off reasoning, anticipates ops pain |
| ✅ Hire | 70-84 | One clean design, can defend it, identifies most trade-offs when prompted |
| 🤔 Maybe | 55-69 | Gets the refactor done, struggles with multi-client design or trade-offs |
| ❌ No Hire | <55 | Cannot complete refactor in 45 min, or answers reduce to "I'd use tool X" |

See `interviewer_materials/SCORECARD.md` for the full rubric.

---

**Built for**: Hiring a Cloud Architect who will own multi-client webapp deployments on GCP and lead the CI/CD work described in the team's deployment proposal.
