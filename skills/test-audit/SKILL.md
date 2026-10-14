---
name: test-audit
description: "Use when a test's value is in doubt or to audit and prune low-value, implementation-coupled or duplicate tests already in the suite. Writing a new test -> tdd. Layer choice -> layered-testing-executor."
license: Apache-2.0
metadata:
  author: rafael
  version: "1.2.0"
  category: code-quality
  subcategory: quality-validation
  vendor: universal
  lifecycle: active
  coding_agent: true
  audience: developer
  output_format: markdown
  modality: text
  freshness: 2026-09
  short-description: Audit and prune low-value tests with evidence
  tags:
  - testing
  - test-audit
  - test-pruning
  - change-detector
  - mocking
  - duplicate-tests
---

# A test is a cost until it earns its place

This skill owns the pruning of tests that already exist: hunt the ones that restate the code, duplicate stronger proof, couple to implementation, or keep test-only production seams alive. Writing a new test, with its gate and bug-regression rule, belongs to `tdd`. Optimize for confidence per line maintained, never for a deletion count.

## Junk patterns

An audit hunts existing tests that match one; `tdd`'s gate refuses a new test that matches one, and reads this list as the single authority.

- probes with no assertion, written to touch lines;
- a value compared with itself, or a copier that mirrors its own input;
- fixtures, inventories, manifests or export lists copied from the source they check;
- greps over source, imports or literal strings in place of running the behavior, and assertions about prose, docs, metadata or trivial mechanics (a getter, a default, an enum value);
- tests about tests, or written only to raise a count or a coverage number;
- private-predicate or call-shape tests already covered at the real boundary;
- the same contract invoked twice;
- per-adapter replays of a shared helper's tests;
- tests that exist only to keep a test-only export, global or wrapper alive, and production code whose only callers are tests;
- expected values produced by the code under test;
- mocks that implement the behavior being asserted, or one identical mock standing in for different APIs;
- fixtures that supply the ordering, receipt or callback the owner should produce, or persistence asserted against a store the path never writes;
- capability tests that restate declared flags without exercising the delivery the flag promises;
- negative controls that pass for an unrelated reason, such as a denial from a different guard or a rejection the path never reaches;
- names or setups that promise more than the input exercises.

## Value bar

A test pays for its upkeep by protecting behavior, a credible regression or an independent contract. In an audit, a test that must change for a behavior-preserving reorganization is suspect, not automatically deletable; `tdd`'s gate still refuses new ones like it.

Before judging a candidate, read the repo's instruction files, then the whole test and its production owner: entry point, callers, callees, sibling implementations, overlapping tests and the history of why it exists. When the test claims behavior of a dependency, read the dependency's source or types.

## Retention bar

Keep a test that independently enforces a public API, protocol, config, migration, storage, security, platform, default, byte-exact output, cross-language, packaging, release or architecture contract. Also keep:

- call order, when order is observable behavior;
- a regression with a credible failure mode;
- a source inspection that is the cheapest independent guard: it fails when the contract changes (the user-facing key, byte or path) and survives an identifier-only refactor;
- a retained test that fails on the baseline. Treat it as a possible product bug: reproduce it and repair the owner, never delete it.

Static or slow is not a deletion reason. A test that resembles the implementation may be the independent contract; prove otherwise before removing it.

## Discovery

Read-only, with evidence reported before any edit. A few high-confidence candidates beat a large speculative inventory. Hunt the junk patterns. On a broad scope, split by area (core, adapters, UI and scripts, a cross-cutting pattern sweep) only when independent readers are available.

Fill every field before deleting a candidate; a missing field means it is not ready:

- exact test name and location;
- the failure it can actually detect;
- non-test callers of the production or support seam it covers;
- the stronger surviving owner-boundary proof, or why none is needed;
- history: why the test or seam exists;
- the production or test-support deletion it unlocks;
- risk, and the focused command that validates it.

## Edit shape

One coherent owner-boundary batch. Delete test-only exports, globals, wrappers and dead production paths instead of keeping aliases. Move a retained regression to its canonical owner; fold repeated package or dependency assertions into one generic contract. Prefer net-negative production LOC. Never add a replacement test that restates the same implementation, and never delete uncertain candidates to raise a count.

## Execution and handoff

To prune one subsystem's whole test surface (every test file a module or component owns), do it as one batch: discover across the whole surface first, fill the evidence fields per candidate, make one edit batch, validate once, hand off once. Keep the plan in the report or PR text, not in a side file. A surface too big for one session is split into coherent batches, never stretched.

Do not edit while a test run is in flight in the same checkout. Validate:

1. Run the smallest owner tests and their siblings with the repo's own runner: the delta only.
2. If you removed a source grep or manifest check, run the script or dry-run that owns the real contract.
3. Run the repo's formatter on the touched files, then `git diff --check`.
4. Read `git diff --numstat` and report production LOC separately from test and test-support LOC.

Hand off:

- root cause and the junk categories removed;
- production simplifications unlocked;
- retained false positives, and why they stay valuable;
- checks actually run, with exit status, and any gap named;
- production LOC versus test LOC;
- named follow-ups.
