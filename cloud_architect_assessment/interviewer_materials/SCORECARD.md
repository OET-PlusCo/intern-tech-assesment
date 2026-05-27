# Scorecard — Cloud Architect Assessment

**KEEP PRIVATE — do not share with candidate.**

Fill this out within 24 hours of the interview while it's fresh. Forward to the hiring panel.

---

## Candidate Info

```
Candidate: ___________________________
Date: ________________________________
Interviewer: _________________________
Duration used: _______ minutes (of 60)
AI tools used during session: ☐ Yes  ☐ No   (which: __________________)
```

---

## Scoring (out of 100)

### Section 1 — Task Execution (40 pts)

| Criterion | Points | Score |
|-----------|--------|-------|
| Refactor: produced a working module structure within ~25 min | 10 | ☐ |
| Refactor: module boundaries are coherent and defensible | 10 | ☐ |
| Refactor: appropriate use of variables, locals, outputs (not mechanical) | 5 | ☐ |
| Multi-client: produced a working second-client design | 10 | ☐ |
| Multi-client: state separation is correctly handled | 5 | ☐ |
| **Subtotal** | **/40** | |

### Section 2 — Design Reasoning (35 pts)

| Criterion | Points | Score |
|-----------|--------|-------|
| Can defend monolith-vs-module trade-offs with specifics | 5 | ☐ |
| Can defend resource-vs-module trade-offs with specifics | 5 | ☐ |
| Divergent-client question: avoids forking, uses inputs/defaults | 8 | ☐ |
| Blast-radius question: names canary/staging/version-pinning | 8 | ☐ |
| Cloud-agnostic question: distinguishes pattern from implementation | 5 | ☐ |
| Spontaneously names downsides of their own design | 4 | ☐ |
| **Subtotal** | **/35** | |

### Section 3 — Communication & Process (25 pts)

| Criterion | Points | Score |
|-----------|--------|-------|
| Asked ≥2 clarifying questions before/during the work | 5 | ☐ |
| Thought out loud throughout the session | 5 | ☐ |
| Used AI tools as a tool (not driven by them) | 5 | ☐ |
| Comfortable saying "I don't know" / "I'd look that up" | 5 | ☐ |
| Asked a substantive question of the interviewer at wrap-up | 5 | ☐ |
| **Subtotal** | **/25** | |

---

### Total: ____ / 100

---

## Score Bands

| Band | Score | Recommendation |
|------|-------|----------------|
| 🌟 Strong Hire | 85–100 | Senior+, can architect autonomously, lead the CI/CD work |
| ✅ Hire | 70–84 | Solid architect, may need pairing on first multi-tenant rollout |
| 🤔 Maybe | 55–69 | Possibly mis-leveled; consider a follow-up with the panel |
| ❌ No Hire | <55 | Did not meet the bar for this role |

---

## Calibration Notes

The most reliable anti-signal for this role is **answering architectural questions with product or service names** instead of describing the underlying design pattern. A candidate who clearly out-performs this anti-signal — especially on Q4, Q5, and Q6 — is what we're looking for.

Indicators a candidate **clears the bar**:
- Names a pattern *before* naming a tool (and only names tools to illustrate patterns)
- Volunteers downsides of their own design without prompting
- Distinguishes "what" (pattern) from "how" (implementation/tool) when asked about alternatives

Indicators a candidate is **below the bar**:
- Reduces every architecture question to a product name
- Cannot answer "what would break first at 100 clients?" without referring to a vendor solution
- Uses "best practice" as a justification without naming the underlying reasoning

---

## Narrative — required

These three short narratives are what the panel will actually read. Bullets and scores get sanity-checked against the narrative.

### Top 3 strengths

1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

### Top 3 concerns

1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

### Memorable quotes (good or bad)

> "____________________________________________________"

> "____________________________________________________"

> "____________________________________________________"

---

## Final Recommendation

```
☐ Strong Hire
☐ Hire
☐ Maybe — discuss with panel
☐ No Hire

If "Maybe": what specific question would a follow-up interview resolve?
___________________________________________________________________
```

---

## Calibration Tags (optional)

Tick any that apply — helps the panel triangulate against other candidates.

☐ Pattern-thinker (designed from first principles)
☐ Mechanic (executed cleanly but couldn't articulate why)
☐ Tool-namer (defaulted to product names instead of design patterns)
☐ Over-engineer (modularized everything; created complexity)
☐ Under-engineer (left too much hardcoded; would not scale)
☐ Operationally-aware (named drift, locking, rollout pain unprompted)
☐ Cloud-agnostic mindset (truly portable design instincts)
☐ Strong communicator (clear, structured, no jargon-as-decoration)
☐ Coachable (took nudges well, iterated quickly)
☐ Defensive (struggled to accept push-back; rationalized own choices)
