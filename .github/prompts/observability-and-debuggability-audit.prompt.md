---
name: observability-and-debuggability-audit
description: Ensures systems are observable, traceable, and debuggable in production environments.
---

# Observability & Debuggability Audit

## Overview

This audit evaluates whether a service, integration, or system change has sufficient operational visibility and diagnostic support to be understood, supported, and debugged in production.

The goal is not just to verify that code runs; it is to verify that the runtime behavior can be observed end to end, that failures can be detected early, and that incidents can be investigated without guesswork.

This prompt is intended for changes that introduce new data flows, external integrations, background processing, or stateful service behavior where production supportability is a material requirement.

### Why this matters

Observability is the ability to understand a system's internal state from its external outputs. Without it, incidents are much harder to detect, troubleshoot, and resolve.

A well-observed system enables operators and developers to answer:

- What happened?
- When did it happen?
- Why did it happen?
- How can it be fixed?

When this audit is applied to a change, the focus should be on whether the required runtime signals are available, not just whether the code compiles or passes unit tests.

## Scope

This audit is appropriate for changes that affect:

- API request handling and backend services
- Batch jobs, scheduled tasks, and worker pipelines
- Event-driven systems and message processing
- Third-party integrations and external API calls
- Stateful services, caches, and persistence layers
- Deployment, configuration, or runtime behavior that impacts production support

It is less applicable to small UI-only cosmetic changes, pure documentation edits, or isolated test code without production-side effects.

## Focus Areas

### Logging Quality

Evaluate whether logs are structured, consistent, and useful for post-incident analysis.

- Structured logging: logs should use strongly typed fields, JSON objects, or key/value pairs rather than ad hoc free-form text.
  - Prefer schema-aligned log fields over embedded string parsing.
  - Avoid concatenating multiple values into a single message field.
- Appropriate log levels: debug is for development or verbose diagnostics, info is for normal operation, warning is for recoverable issues, and error is for failures that require investigation.
  - Ensure info-level logs do not contain sensitive or excessively verbose data.
  - Reserve error-level logs for actual faults, not control flow.
- Sensitive data protection: secrets, credentials, authentication tokens, and PII should never be logged; redaction or omission should be enforced.
  - Validate that any user-provided content is sanitized before logging.
  - Review logs for accidental exposure of internal system state.
- Format consistency: log payload schemas, timestamp formats, and severity labels should remain stable across the services in scope.
  - Use a shared logging standard where available.
  - Ensure timestamps are in UTC or otherwise normalized.
- Correlation support: request IDs, trace IDs, or operation IDs should be included so logs can be correlated across multiple components.
  - Correlate logs with traces and metrics using the same identifier where possible.
- Context-rich messages: logs should capture the relevant state (request path, user identifier, payload type, error code) needed to understand what happened.
  - Capture the business context, not only the technical event.
- Log volume: avoid excessive debug noise in production, and ensure logs are sampled or rate-limited where appropriate.
  - Identify noisy success paths and ensure they do not overwhelm the logging pipeline.

#### Recommended checks for logging

- Are log statements consistent in structure and format?
- Does every error path emit an error or warning log?
- Are debug logs gated behind configuration and disabled by default in production?
- Are any logs writing raw request/response payloads without redaction?
- Can a production incident be traced through the logs alone?

### Metrics Quality

Evaluate whether the system exposes meaningful metrics for both business outcomes and operational health.

- Business metrics: measure domain-relevant outcomes such as transactions completed, items processed, customer actions, or success/failure ratios.
  - Business metrics should answer whether the feature is working from a customer or product perspective.
- Health metrics: track availability, error rates, latency percentiles, queue depth, thread pool saturation, retries, and resource exhaustion.
  - Health metrics detect systemic degradation before business impact becomes severe.
- Alerting hooks: there should be a clear mapping from metric thresholds to operational alerts, with thresholds documented or justified.
  - Alerts should have a clear action and owner.
- Cardinality control: metrics should avoid unbounded label cardinality and should be designed to preserve performance in metric storage.
  - Ensure labels are limited to safe domains such as service name, region, or environment.
- Metric ownership: the new or changed metrics should have clear ownership and a documented intent for their use.
  - Metrics should be named and described clearly.
- Event counters vs gauges: use the correct metric type for cumulative counts, current state, or latency distributions.
  - Counters for totals, gauges for instantaneous values, histograms/summaries for latency distributions.

#### Recommended checks for metrics

- Are there metrics for success and failure rates of the new flow?
- Are latency distributions captured for high-impact operations?
- Can the team create alerts from the metrics without additional instrumentation?
- Do the metrics use any unbounded or high-cardinality labels?
- Is the metric intent documented in comments, dashboards, or runbooks?

### Traceability

Evaluate whether requests and events can be traced across service boundaries and asynchronous workflows.

- Distributed tracing: trace IDs or span IDs must propagate across HTTP requests, RPC calls, message queues, and background jobs.
  - Ensure trace context is passed through any network or messaging layer.
- Correlation identifiers: each logical operation should carry a stable correlation ID through the lifecycle of the request or event.
  - Correlation IDs should be present in logs, metrics, and traces.
- Async context propagation: trace context must survive retries, scheduled jobs, worker queues, and callback handlers.
  - Verify that background workers retain the originating request context.
- Sampling strategy: the tracing strategy should be defined, including how sampling is configured and how representative traces are chosen.
  - Confirm whether tracing is sampled, and if so, that failure paths are always captured.
- Trace fidelity: traces should include meaningful operation names, timestamps, durations, status codes, and failure markers.
  - Avoid generic or anonymous span names.
- Trace coverage: critical paths should be instrumented, not just entry points.
  - Missing spans on key service boundaries are a serious gap.

#### Recommended checks for traceability

- Can the end-to-end path be reconstructed from trace data?
- Do background jobs and asynchronous handlers appear in the same trace when they belong to the same workflow?
- Are retries, redirects, and downstream calls visible in the trace?
- Is the trace name and metadata meaningful for operational debugging?
- Has the tracing strategy been documented for this change?

### Error Context

Evaluate whether failures produce actionable diagnostics instead of opaque or generic errors.

- Actionable error messages: errors should state what failed, why it failed, and what to inspect next.
  - Error messages should avoid generic text like "operation failed" without context.
- Stack trace hygiene: stack traces should be available for diagnostics but not expose internal secrets or irrelevant implementation details.
  - Ensure that production error reports do not leak database credentials, API keys, or internal state.
- Debug metadata: include request IDs, user IDs, transaction IDs, relevant parameters, and state snapshots in error reports.
  - Only include metadata that assists diagnosis without exposing sensitive data.
- Failure reporting: there should be a documented path for how exceptions are surfaced to monitoring, alerting, or incident management.
  - Verify that critical exceptions are not silently swallowed.
- Graceful degradation: the system should fail safely, preserve composability, and avoid cascading failures when possible.
  - Failures in one component should not bring down unrelated functionality.
- Retries and backoff: transient failures should be retried with backoff, and retries should be visible in metrics or logs.
  - Retries should not hide the original root cause.

#### Recommended checks for error context

- Does every major failure path include an explanatory error log or exception?
- Are errors exposed to monitoring with the right severity?
- Can an operator identify the failed component and request ID from the error output?
- Are fatal and non-fatal failures clearly distinguished?
- Are retry loops instrumented so that retries are visible and not silent?

### Monitoring & Alerting

Evaluate whether monitoring is complete and whether operational behavior is visible in dashboards and alerts.

- Key business metrics present: the change exposes the right signals for validating success and detecting failures.
- System health metrics tracked: the service should expose core metrics such as request rate, error rate, latency, CPU, memory, and queue size.
- Alerting hooks available: there should be actionable alerts tied to meaningful symptoms like elevated error rates or service degradation.
- Dashboard coverage: monitoring dashboards should exist or be easily created for the impacted flows.
- Cross-component coverage: observability should span all dependent services, not just the local process.
- Monitoring strategy documented: the expected observability posture for the feature should be stated clearly for reviewers and operators.
- Coverage gaps identified: any known blind spots should be explicitly documented and accepted.

#### Recommended checks for monitoring & alerting

- Are service-level indicators present for the new feature?
- Does the change add or modify alerts, and are they justified?
- Is there an operational dashboard that reflects the new behavior?
- Have known blind spots been documented and mitigated?
- Are the monitoring metrics accessible to the team in the current observability stack?

### Production Debuggability

Evaluate whether incidents can be reproduced, investigated, and resolved in production-like conditions.

- Failure reconstruction: there should be enough telemetry to reconstruct the sequence of events leading to a failure.
- Workflow replay: the system should allow replay of requests, events, or jobs when needed to reproduce a problem.
- Staging parity: there should be a plausible way to reproduce failures in staging or test environments with realistic data.
- Production access: operators and engineers should have access to logs, traces, metrics, and error reports needed for root-cause analysis.
- Debugging strategy: the overall approach for investigating production issues should be defined and aligned with the change.
- Post-mortem readiness: the change should not introduce new black boxes that are impossible to explain after the fact.

#### Recommended checks for production debuggability

- Has the team identified the expected failure modes for this change?
- Is there a documented incident response path for this feature?
- Can a developer reproduce the failure in staging or test using the same inputs?
- Are observability artifacts available to support a post-mortem investigation?
- Is there a mechanism to trace from a customer complaint back to a specific operation or event?

## Observability Failure Modes

Reviewers should explicitly consider whether the change introduces any of these failures:

- Invisible failures: errors that occur without logs, metrics, or traces.
- Misleading signals: log or metric fields that are wrong, stale, or inconsistent.
- Untraceable executions: asynchronous work that cannot be linked back to the originating request.
- Alert fatigue: overly sensitive alarms or noisy metrics that create operational distraction.
- Blind spots: unmonitored dependencies or steps that are not instrumented.
- Partial observability: only the start or end of a workflow is visible, leaving the middle opaque.
- High-cardinality metrics: unbounded labels that can cripple metric storage.
- Missing retry visibility: repeated retries that are invisible or indistinguishable from fresh failures.
- Silent failures during startup, configuration reload, or shutdown.
- Inconsistent log formatting across service versions or environments.

## Common Observability Anti-patterns

- Logging raw request payloads without redaction.
- Using print statements instead of structured logging.
- Emitting metrics only for success paths and not failure paths.
- Instrumenting entry points but not downstream processing.
- Storing state or configuration in logs rather than using dedicated metrics.
- Relying on ad hoc error messages instead of structured error reports.
- Assuming the reviewer's environment is the same as production.
- Treating observability as an afterthought rather than a design requirement.

## Review Process

Use this audit in three passes:

1. Verify the data sources and side effects: identify where the change reads/writes state, emits events, or calls external services.
   - Map inputs, outputs, and side effects.
   - Identify which systems must be observable for correct operation.
   - Determine whether the change touches both synchronous and asynchronous components.
2. Check each observability dimension: logging, metrics, tracing, error context, monitoring, and production debuggability.
   - Evaluate both the new code and the existing instrumentation it depends on.
   - Identify gaps between the code path and the operational signals.
   - Document whether the change adds new observability responsibilities or merely relies on existing coverage.
3. Validate the evidence: ensure there are concrete artifacts such as log examples, dashboard rules, alert definitions, or instrumentation docs.
   - Ask for examples when the implementation claims observability without backing evidence.
   - Verify that the proposed instrumentation is actually deployed or included in the change.

### Review Artifacts

A strong observability review includes one or more of the following artifacts:

- Example log entries for normal and failure paths
- Metric definitions or configuration snippets for new counters/gauges/histograms
- Trace diagrams or exported trace examples for the main flow
- Alert rules or service-level indicator definitions
- Dashboard widgets or query examples for key metrics
- Runbook or on-call guidance for the changed behavior

If none of these artifacts exist, the review should raise a question about observability completeness.

### Operational Readiness Checklist

The change should be evaluated against operational readiness criteria in addition to observability:

- [ ] Does the change include a way to detect failure automatically?
- [ ] Are there clear signal types for success, failure, and degradation?
- [ ] Can the on-call team distinguish between application issues and infrastructure issues?
- [ ] Is there a documented escalation path for incidents caused by this change?
- [ ] Has the team identified the expected recovery behavior for transient failures?

### Example Review Findings

These example findings can help reviewers express the gap clearly:

- "Logging is present, but it is unstructured and cannot be reliably parsed by the log ingestion system."
- "The new batch job emits success metrics, but there is no failure counter or latency histogram."
- "Trace context is not propagated through the message queue consumer, so backend retries are invisible in end-to-end traces."
- "Error reports include stack traces, but the request ID is missing, making correlation difficult."
- "There is no alert defined for elevated error rate in the new API endpoint."

### Decision Guidance

When choosing an output decision, consider both current state and risk:

- GOOD: The change has sufficient instrumentation, and the available signals enable incident detection and triage.
  - Logging, metrics, traces, and monitoring are all aligned with the new behavior.
  - There are concrete artifacts or examples demonstrating the observability.
- INSUFFICIENT_OBSERVABILITY: The change has incomplete or inconsistent instrumentation.
  - The feature may work, but failures cannot be reliably detected or diagnosed.
  - This is a signal to require additional observability work before merge.
- CRITICAL_GAP: The change introduces a major blind spot.
  - Key failure modes are invisible, or tracing/logging is absent for critical flows.
  - This should block merge until visibility improves.
- VERIFICATION_REQUIRED: The change may appear acceptable, but claims of observability are unverified.
  - Evidence such as dashboards, traces, or runbook updates is needed before approval.

### When to Escalate

Escalate the observability review if any of the following apply:

- The change affects compliance-sensitive or security-sensitive systems.
- The change introduces a new integration with an external dependency.
- The change adds a new stateful service, queue, or retry mechanism.
- The team is unsure whether the instrumentation will actually be deployed in production.
- There is no documented on-call action for the new behavior.

### Common Observability Glossary

- Signal: any runtime output that conveys state, such as logs, metrics, traces, events, or alerts.
- Event: a point-in-time record, usually in logs or audit trails.
- Metric: a quantitative measure of system behavior over time.
- Trace: an end-to-end record of work across service boundaries.
- Correlation ID: an identifier that ties together logs, metrics, and traces for one logical request or workflow.
- Alert: a notification condition based on signal thresholds or anomalies.
- Dashboard: a curated view of one or more signals for operational monitoring.
- Runbook: a documented guidance document for operators responding to incidents.

### Evaluation Checklist

- [ ] Logging is structured, levelled, and traceable.
- [ ] Sensitive data is not emitted in logs or error messages.
- [ ] Business and health metrics are defined and documented.
- [ ] Trace context propagates across all relevant boundaries.
- [ ] Errors include enough context for investigation.
- [ ] Monitoring and alerting hooks are identified.
- [ ] Production failure reconstruction is feasible.
- [ ] Known observability gaps are documented.
- [ ] Alerting thresholds and owner actions are documented.
- [ ] The change does not introduce unbounded metric cardinality.
- [ ] Asynchronous workflows can be correlated back to user-facing requests.
- [ ] Error paths are instrumented and visible in metrics/logs.
- [ ] Any new observability instrumentation has been tested or verified.
- [ ] The change includes an operational artifact (dashboard, alert, log sample, or runbook).
- [ ] Existing instrumentation is reused where appropriate rather than duplicated.

## Output Decision

- GOOD: Observability is sufficient for production use, and failures can be diagnosed with the available logs, traces, metrics, and dashboards.
- INSUFFICIENT_OBSERVABILITY: The change lacks important diagnostic signals, tracing support, or error context and needs observability improvements before approval.
- CRITICAL_GAP: There is a serious absence of logging, tracing, or error context that makes the system effectively unobservable in production and blocks merge.
- VERIFICATION_REQUIRED: The change may be acceptable, but the observability claims must be validated with concrete evidence such as dashboards, alerts, instrumentation tests, or runbook updates.
