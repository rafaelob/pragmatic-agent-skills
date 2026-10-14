---
name: tdd
description: "Use when about to write code and its tests for a feature or bugfix and no failing test exists yet: routine test authoring, red-green-refactor. Pruning existing tests -> test-audit. Layers -> layered-testing-executor."
license: Apache-2.0
metadata:
  tags:
  - tdd
  - red-green-refactor
  - test-driven-development
  - behavioral-testing
  - mocking
  - tracer-bullet
  - pytest
  version: "1.6.0"
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
The story's own acceptance test, not the unit suite, says it is finished, and a test earns its place only by proving something nothing else already proves. Start from that acceptance test (`testing-e2e-playwright` when it is a browser journey). This skill owns writing the routine test; `test-audit` owns pruning the ones already in the suite.

Put each candidate case through this gate as you write it. A missing answer means the case is not written yet.

1. **Contract.** Which observable behavior, invariant or independent contract does it protect?
2. **Regression.** Which credible change to the code makes it fail?
3. **Owner.** Why does existing coverage not already catch that? A contract has one primary owner, at the strongest boundary that can see it. A second layer needs its own risk that the owner cannot reach, such as a transport or lifecycle failure. Extend a table or shared fixture instead of adding a near-copy.
4. **Seam.** Does it need production code (an export, flag, wrapper or injection hook) that no production caller needs? If so, test at the real boundary instead.

A case that matches a pattern in `test-audit`'s junk patterns also fails the gate, unless it guards a contract on its own. Load `test-audit` for that list when a case's value or overlap is uncertain, not once per assertion. A case that breaks under a refactor that preserves behavior asserts implementation: rewrite it at the owning boundary.

Add or extend a focused case for the next meaningful distinction that survives the gate, owned by the existing test that most naturally covers it. The test must exercise production code with an expected result derived from a requirement, worked example, independent oracle or valid invariant—not by copying the same production calculation into the assertion. See [good and bad tests](references/tests.md) when unsure whether a candidate test is well-formed.

Observe RED for the intended behavior. A missing runtime, unrelated import error or no tests collected is a setup problem, not useful RED. For a known bug, demonstrate the regression with the smallest representative input where feasible: the test must fail on the pre-fix code, for the reason the bug exists, and pass after the fix. One that never failed proves the mock, not the fix. When the pre-fix failure cannot be reproduced (the old environment is gone, or the failure is nondeterministic), say so as a weaker-evidence limit instead of claiming a red that was never observed. One regression at the owner boundary covers the bug; do not replay it at every layer it crosses.

Implement the simplest change that satisfies the case and existing contracts. Test doubles are useful at the boundary outside the assertion's scope; do not mock away the persistence, authorization or transport behavior you claim to test. See [when to mock](references/mocking.md) when the boundary is unclear. Do not unit-test framework primitives or private helpers.

Refactor while green when a local change improves clarity or reduces current coupling. See [refactor candidates](references/refactoring.md) for concrete signals once tests are green. Keep structural moves distinguishable from changed behavior; no mandatory new architecture or reviewer for each rename.

## Naming the exception
Add a case only for a distinct rule, boundary, failure or historical escape; a parameterized table may express several at once. An internal name, copied constant, getter, enum value, dataclass default, source-text match or mock echo is never a consumer contract on its own. A test written after the code that only restates it is a change detector: delete it or rewrite it against behavior — to retire a test already in the suite, use `test-audit`.

A spike may use test-during exploration, with the production contract verified before merge; it is not permission to postpone all testing. Stop when accepted behavior and material risks are covered, not when every imagined input has an example.

See [useful test examples](references/useful-test-examples.md) when deciding between a behavioral assertion and an implementation mirror.

For choosing which layers a finished change must run, use `layered-testing-executor`; when the failure's cause is still unknown, use `diagnosing-bugs`; when the code to change has no trusted tests, use `legacy-code-change`.
