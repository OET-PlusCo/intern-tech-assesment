# Architecture Discussion Questions

These are the questions your interviewer will work through with you during the discussion phase (~15 min). They are deliberately open-ended. There are no single right answers — we care about **how you reason and what trade-offs you can name**.

You don't need to prepare answers in advance. They're listed here so you know the territory we'll cover.

---

## 1. Monolith vs. Modules

> *"You just broke a monolith into modules. When would you deliberately leave something as a monolith and **not** modularize it?"*

> *"What's the cost of over-modularizing? Have you seen it happen?"*

---

## 2. Resource vs. Module

> *"At what point does a `resource` block deserve to become its own module? What's your rule of thumb?"*

> *"Show me a place in your refactored code where you used a raw `resource` block instead of wrapping it in a module. Why?"*

---

## 3. Multi-Client State Management

> *"You have 10 clients today. Imagine you have 100 in two years. Does your design still work? What breaks first?"*

> *"One client's `terraform apply` fails mid-way and leaves the state locked. What's your operational playbook?"*

---

## 4. The Divergent Client

> *"Client-gamma signs a contract that requires Cloud SQL high availability and a private VPC peering connection. None of the other clients need this. How do you handle the divergence without forking your modules?"*

---

## 5. Blast Radius

> *"You push a change to the module that defines the Cloud Run service. Walk me through what happens between merge and that change reaching all 50 clients in production."*

> *"What stops this change from breaking everyone simultaneously?"*

---

## 6. Cloud-Agnostic Design

> *"If we told you next year that we have to support deploying the same stack to AWS for a specific client, which parts of your design survive and which parts you'd throw away?"*

---

## 7. Secrets and IAM Per Tenant

> *"How is `client-acme`'s database password isolated from `client-beta`'s? What stops a misconfigured Terraform run from leaking one client's resources into another's project?"*

---

## 8. Cost & Onboarding

> *"A salesperson signs a new client at 4pm Friday and promises them a working environment by Monday morning. Walk me through what the onboarding process looks like with your design."*

> *"What's the cheapest version of this that still preserves isolation? What would you cut?"*

---

**Reminder**: Trade-offs over absolutes. "It depends, and here's why" beats "always do X."
