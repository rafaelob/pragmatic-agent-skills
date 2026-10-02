---
name: tdd
description: "Use when about to write code for a feature or bugfix and no failing test exists yet. Red-green-refactor. Layers -> layered-testing-executor. Untested -> legacy-code-change; unknown cause -> diagnosing-bugs."
license: MIT
metadata:
  tags:
  - tdd
  - red-green-refactor
  - test-driven-development
  - behavioral-testing
  - mocking
  - tracer-bullet
  - pytest
  version: 1.5.2
  author: coding-agent
  category: code-quality
  subcategory: quality-validation
  vendor: universal
  lifecycle: active
  coding_agent: true
  audience: developer
  output_format: markdown
  modality: text
  freshness: 2026-06
  upstream: https://github.com/mattpocock/skills
  upstream_mode: adapted
  upstream_baseline_commit: 5b15a47f2d7150f545fbcacbfe381787fc0230dc
  upstream_baseline_date: 2026-08-21
  upstream_author: Matt Pocock
  upstream_path: skills/engineering/tdd/SKILL.md
  upstream_not_adopted:
    cursor-skill-tool: Upstream says `call the Skill tool with "codebase-design"`. This catalog is harness-neutral and already names `codebase-design` as a reference, not a Cursor tool call.
    em-dash-sweep: Repo-wide em-dash removal (3216582) is cosmetic here; house voice keeps em-dashes that separate a constraint from its reason.
---

# Test-driven development, not test-count development

## Before writing a test
The story's own acceptance test, not the unit suite, says it is finished, and a test earns its place only by proving something nothing else already proves. Start from that acceptance test (`testing-e2e-playwright` when it is a browser journey), then apply `test-audit`'s authoring gate (Contract, Regression, Owner, Seam) as reasoning while you write each candidate case: a case that fails it is not written. Load `test-audit` itself when a case's value, overlap or removal is uncertain, not once per assertion.

Add or extend a focused case for the next meaningful distinction that survives the gate, owned by the existing test that most naturally covers it. The test must exercise production code with an expected result derived from a requirement, worked example, independent oracle or valid invariant—not by copying the same production calculation into the assertion. See [good and bad tests](references/tests.md) when unsure whether a candidate test is well-formed.

Observe RED for the intended behavior. A missing runtime, unrelated import error or no tests collected is a setup problem, not useful RED. For a known bug, demonstrate the regression with the smallest representative input where feasible.

Implement the simplest change that satisfies the case and existing contracts. Test doubles are useful at the boundary outside the assertion's scope; do not mock away the persistence, authorization or transport behavior you claim to test. See [when to mock](references/mocking.md) when the boundary is unclear. Do not unit-test framework primitives, private helpers or uncovered lines to raise coverage; coverage points at an untested behavior, it is never a quota.

Refactor while green when a local change improves clarity or reduces current coupling. See [refactor candidates](references/refactoring.md) for concrete signals once tests are green. Keep structural moves distinguishable from changed behavior; no mandatory new architecture or reviewer for each rename. Rerun affected checks after meaningful changes, not after unchanged reads.

## Naming the exception
Add a case only for a distinct rule, boundary, failure or historical escape; a parameterized table may express several at once. An internal name, copied constant, getter, enum value, dataclass default, source-text match or mock echo is never a consumer contract on its own. A test written after the code that only restates it is a change detector: delete it or rewrite it against behavior — to retire a test already in the suite, use `test-audit`.

A spike may use test-during exploration, with the production contract verified before merge; it is not permission to postpone all testing. Stop when accepted behavior and material risks are covered, not when every imagined input has an example.

See [useful test examples](references/useful-test-examples.md) when deciding between a behavioral assertion and an implementation mirror.

For choosing which layers a finished change must run, use `layered-testing-executor`; when the failure's cause is still unknown, use `diagnosing-bugs`.
