---
name: legacy-code-change
description: "Use when changing code with no trusted tests (characterize, cut the smallest seam, red then green). Trusted tests -> refactoring-catalog. New code -> tdd. Unknown cause -> diagnosing-bugs."
license: Apache-2.0
metadata:
  author: coding-agent
  version: 1.0.9
  category: code-quality
  subcategory: quality-validation
  vendor: universal
  lifecycle: active
  coding_agent: true
  audience: developer
  output_format: markdown
  modality: text
  tags:
  - legacy
  - characterization-testing
  - seam
  - sprout
  - wrap
  - golden-master
  - approval-testing
  - refactoring
  - safety-net
---

# Legacy Code Change

Legacy code is code without tests you trust. Cleaning it up first would refactor without a net, judging correctness against what you *think* it does: pin the behavior first, then change it.

## Workflow

### 1. Characterize the observed behavior — quirks included

At the real seam, pin only the behavior being changed and what it can reach. Start with one deliberately
wrong assertion and run it to reveal the observed value; then cover reachable branches, boundaries and
error paths. Mark deliberate quirks, such as `test_..._quirk_preserves_trailing_space`, instead of
normalizing them.

For wide output, use one golden-master/approval snapshot. Stop when the net covers the change and
blast radius; do not characterize an entire module for a small fix.

### 2. Cut the smallest seam that lets the test run

Often there is nowhere to observe from: the logic is buried in a 400-line method
that hits the database, the clock, and the network. Take the **smallest** change
that creates a testable boundary — and make it behavior-preserving.

- **Sprout.** Write the new behavior as a **new** function or class, fully
  tested on its own, and call it from one line in the old code. The legacy mess
  stays untouched; the new logic is born under test. Default choice.
- **Wrap.** Rename the old method, create a new one with the original name that
  calls the old one, and put the new behavior in the wrapper. Use when the new
  behavior must run before/after the existing one on every call.
- **Break a dependency**, minimally: extract an interface, parameterize a
  constructor, extract-and-override in a test subclass, inject the clock. Only
  as much as the test needs.

Seam changes are **structural, never semantic**: same behavior, new boundary.
Land them separately from the change you actually came to make.

### 3. Write the new behavior test before changing anything

Write and run the failing test at the real seam, implement only enough to make it green, then rerun
the original characterization loop.

If a pinned behavior conflicts with the intended result, decide explicitly whether it is a bug or a
contract; never rewrite the pin silently. If no correct seam exists, record that architectural finding
instead of substituting a shallow test.

### 4. Exercise real collaborators; Remove the temporary harness

Exercise the changed path against real collaborators at least once; a test-double-only boundary is
unproven. Remove temporary harnesses, debugging, dead toggles and redundant characterization tests; keep
tests that pin undecided behavior.

Size the seam and the new-behavior test to the change, not to the whole legacy module. Once its checks pass, remove the scaffolding and stop; widen coverage again only when a new change, a failure or an unresolved concern gives a reason, not as routine re-checking of what is already green.

### 5. Refactor green-to-green; keep the final diff clean

Refactor with `refactoring-catalog` for named moves, tests after each. Keep behavior-preserving structure changes separable from behavior changes; separate commits when they help a bisect or let a reviewer read the risky one alone.

## Gotchas

- Control nondeterminism (clock, randomness, ordering) before pinning behavior.
- Do not fix unrelated bugs while characterizing.

## Validation checklist

- [ ] The changed behavior and reachable blast radius are characterized; quirks and nondeterminism are explicit.
- [ ] The seam is structural and the new-behavior test was observed red before the fix.
- [ ] Real collaborators were exercised, or the boundary is explicitly BLOCKED.
- [ ] Temporary scaffolding is removed and intentional pins have reasons.

## Cross-references

- `tdd`: the red-green loop this borrows (there the behavior is new, here it exists). `diagnosing-bugs`: unknown cause, diagnose first. `codebase-design`: seam and module vocabulary. `layered-testing-executor`: which layers the change owes (decide from the project's own test layers, preferring the narrowest layer that proves the behavior).
- Replacing the system instead of changing it is its own incremental migration (strangler-style cutover, parity checks), not a stretched version of this workflow.

## Attribution

Practice vocabulary from Michael Feathers, *Working Effectively with Legacy
Code* (2004) — characterization tests, seams, sprout and wrap. Approval/golden-master
testing per Llewellyn Falco's approvals work.
