---
name: testing-e2e-playwright
description: "Use when writing, fixing or de-flaking a Playwright/e2e browser test: fixtures, locators, waits, user-visible assertions. Not the pre-delivery UI pass."
license: Apache-2.0
metadata:
  author: coding-agent
  version: 1.3.1
  category: code-quality
  subcategory: quality-validation
  vendor: universal
  lifecycle: active
  coding_agent: true
  tags:
  - testing
  - e2e
  - playwright
  - user_level:intermediate
  audience: developer
  output_format: markdown
  modality: text
---

# Browser tests with a distinct purpose

Identify the user journey and why a lower-level check cannot establish it. Read the installed runner, configuration, supported browsers and existing tests. Extend a journey only when it adds a distinct contract; do not duplicate it for every nearby skill or module. Read `references/PLAYWRIGHT_PATTERNS.md` for concrete selector, fixture, network and visual-regression patterns; read `references/DOC_LINKS.md` for the official-docs pointers behind them.

Use isolated data and authorization fixtures. Prefer API or fixture setup over replaying irrelevant UI setup in every test, without bypassing the behavior under test. Control time and nondeterministic external boundaries where appropriate. A simulated provider response can prove the UI reaction, not the provider connection. No paid generation, real messaging or production mutation without authorization.

Pick a scenario representative of the changed risk, not the easiest happy path: realistic data volume, a failure or recovery branch and a permission edge when they apply. End with a repeatable artifact — the command plus the runner report, trace or screenshots — that another person can rerun and compare.

Drive roles, labels and meaningful user interactions rather than incidental DOM structure or arbitrary waits. Assert a user-observable result or durable effect. For pure calculation permutations, use the responsible domain tests and retain a representative wiring journey, not hundreds of browser cases.

## Keep signals reliable
Use existing waiting/assertion primitives and sanitized failure traces. A retry that succeeds after failure is flaky evidence, not an unqualified first-run PASS. Investigate fixture isolation, timing and system behavior before raising retries or timeouts. Quarantine only with an explicit gap, owner and correction path; it does not restore the protected claim by itself.

A changed global component, browser-specific defect or required matrix can justify broader runs. Otherwise choose relevant journeys and required gates. Do not rerun unchanged successful suites for reassurance. Zero collected tests, old assets or unavailable required dependencies prove nothing about the journey. Stop when the intended browser behavior is evidenced without unexplained flakiness affecting the claim.

The pre-delivery pass over a changed screen (real browser, every state, accessibility, the real backend) is a separate done-gate: run it before calling the UI done, and do not stretch a test to stand in for it. When a cheaper layer can hold the same rule, use `layered-testing-executor`.
