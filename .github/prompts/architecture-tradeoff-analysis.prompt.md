---
name: architecture-tradeoff-analysis
description: Guides structured system design decision-making through explicit trade-off analysis. Use when choosing between architectural patterns, technologies, or approaches (e.g., event-driven vs REST, monolith vs microservices, SQL vs NoSQL). Focuses on constraints, scalability, cost, and long-term impact rather than defaulting to familiar solutions.
---

# Architecture Trade-off Analysis

## Overview

Architecture is about **choosing between imperfect options**. Every design decision carries trade-offs across scalability, complexity, cost, performance, and team velocity.

This prompt enforces **explicit decision-making**:

- Identify realistic options
- Evaluate trade-offs across key dimensions
- Align the decision with constraints and goals
- Avoid “default choices” or trend-driven decisions

The goal is not to find a perfect solution, but the **best fit for the current context**.

When applied, this prompt should surface the reasoning behind the choice, highlight what is being sacrificed, and make the decision defensible to stakeholders.

---

## When to Use

- Designing a new system or service
- Choosing between architectural patterns (monolith vs microservices)
- Selecting data storage (SQL vs NoSQL)
- Evaluating communication style (REST vs event-driven)
- Scaling an existing system
- Replacing or modernizing legacy components
- Comparing infrastructure options (cloud provider, managed service, container orchestration)
- Assessing integration approaches (batch vs streaming, synchronous vs asynchronous)

---

## Core Principle

**There is no universally “best” architecture — only contextually optimal choices.**

Evaluate decisions against the following fundamental questions:

- What are the explicit goals and constraints?
- What are the realistic alternatives?
- What is the impact on cost, risk, and delivery speed?
- What is the expected lifetime and evolution path of the system?

---

## Recommended Analysis Structure

1. Define the problem clearly.
   - Summarize the desired outcome.
   - List the key constraints (budget, timeline, team skills, compliance, existing platform).

2. Enumerate viable options.
   - Include at least two credible alternatives.
   - Avoid presenting strawman or unrealistic options.

3. Compare trade-offs across dimensions.
   - Scalability and performance
   - Operational complexity and maintenance
   - Cost (development, runtime, and support)
   - Risk and reliability
   - Time to market and team readiness
   - Flexibility for future changes

4. Recommend the best fit.
   - Explain why the chosen option is the strongest fit for the current context.
   - Identify the most significant downside and how it can be mitigated.

5. State validation criteria.
   - Define how success will be measured.
   - Note any conditions that would justify revisiting the decision.

---

## What to Avoid

- Choosing an option solely because it is popular or familiar.
- Ignoring non-functional requirements in favor of technical elegance.
- Treating trade-offs as binary; most decisions involve balancing multiple competing factors.
- Leaving assumptions unstated.
- Suggesting a choice without explaining the why.

---

## Useful Techniques

- Use a small decision matrix to make comparisons explicit.
- Call out dependencies and integration costs.
- Note any existing platform or organizational constraints that influence the choice.
- Keep the analysis concise but sufficiently detailed for review.
