---
name: layered-testing-executor
description: "Use when a changed capability is ready to verify: tests to pick and run, seams to prove reachable, genuine zero vs unknown. Narrowest layer first. Not first failing test -> tdd."
license: Apache-2.0
compatibility: Any AI coding agent (Claude Code, Codex CLI, Cursor, Windsurf, Gemini CLI). Requires git
  diff or change description; collect mode also requires a runnable test toolchain.
metadata:
  author: rafael
  version: "1.7.5"
  category: process-automation
  subcategory: sop-workflows
  vendor: universal
  tags:
  - process-automation
  - testing
  - layered
  - change-type
  - test-router
  - evidence
  - regression
  - unit
  - integration
  - e2e
  - agents-md
  - functional-first
  - skill_level:intermediate
  audience: developer
  output_format: markdown
  modality: text
  agents_md_sections:
  - '4'
  - '7'
  lifecycle: active
  coding_agent: true
---

# Select useful tests for this change

## Find the real contract
Read the diff, acceptance, declared runner and applicable verification policy. Include relevant staged, unstaged and generated changes. Group by changed behavior and trust boundary, not by a mandatory row for every file. A one-line config change can have broad impact; a large generated diff can have a narrow owner.

## Select the smallest adequate proof
First inspect existing affected tests. Add or extend a test only for a distinct uncovered failure, invariant or contract (writing the test → `tdd`; pruning existing ones → `test-audit`). Use unit/domain checks for local rules; component tests for local interaction; a real integration for the collaborator behavior at issue; browser journeys for browser-dependent or cross-boundary outcomes. These are choices, not a ladder whose every rung must run.

A copy-only UI edit does not by itself require UI→API→database. Verify its render, overflow or accessible name as relevant. Config syntax does not prove effective precedence or runtime behavior; test those only where affected. A mocked provider can prove local recovery logic, not that provider's live API. An absent required real integration is NO_VERDICT, not a mocked substitute.

## Execute precisely
Use the project's existing runner, lock and environment. Preserve exit status and runner summaries. A deliberately empty lint result may be valid; an empty test suite proves no behavior.

## Prove the seam, and keep zero distinct from unknown
A layer passing is not the caller arriving. For a changed capability, start at the accepted entry point — UI action, public function, API, CLI, event or worker — and name only the real seams on that path and which of them one real run proves; add a separate command and verdict only for a seam that run does not reach or cannot distinguish; code invoked solely in tests is not evidence of application wiring, and a health endpoint is not a registered route. Inspect both trigger and effect, and observe a persistence claim through the real read path. When a UI→API→persistence run is owed is the global testing rule's call.

Then keep the outcome's meaning. A check ends in one of three states:

- **PASS**: it ran to completion and its result was read, at the exact head being merged. Only this is a merge verdict; a pass recorded at another head is evidence for that head.
- **FAIL**: it ran and the result is a failure.
- **NO_VERDICT**: everything else — zero collection, timeout, xfail, deselection, skip, an unreadable result, a dispatch-only exit, a collect on a head that has moved, a stopped machine, a CPU refusal, an absent required real integration, an exhausted budget, an unavailable checker. Print `NO_VERDICT <code> <reason> next=<status read>`, where the status read is the read-only command that settles it, and never describe the check as passed.

A fallback of zero, an empty list or a success badge must not erase a failure. The counterexample is the cheapest proof — the same empty payload after a completed run and after a failed run must produce different consumer behaviour.

## Escalate or finish
Investigate a failure at the smallest responsible seam instead of adding a heavier suite. Widen for an uncovered contract, cross-cutting effect, concurrency/data risk, known escape or explicit gate—not merely because a generic file category matched. Unrelated blocked checks need not stop independent safe work, but still prevent the completion claim that depends on them.

Report one line per check that actually ran — command, verdict (PASS, FAIL or NO_VERDICT), any gap — in the existing work record. Group identical skip causes instead of producing a row for every deselected test.

Read [selection examples](references/test-selection.md) for ambiguous cases, evidence reuse and safe retirement.

Use [the optional evidence note](assets/evidence-note.md) only for a nontrivial result that lacks an existing project format.

For the red-green loop of one behavior, use `tdd`; when a browser journey is the only honest boundary, use `testing-e2e-playwright`.

For a costly invariant over cancellation, retries or response ordering, inspect
an existing project-local verification skill. If none covers the risk, propose
an explicitly scoped bounded check rather than installing a global verifier.
Keep model/code correspondence, bounds and a failing real-code mutation with the
result. Generated sequential cases alone do not prove interleavings; a budget
limit and an unavailable checker are NO_VERDICT, never a stronger pass.
