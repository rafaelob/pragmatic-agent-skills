---
name: layered-testing-executor
description: "Use when a changed capability is ready to verify: tests to pick and run, seams to prove reachable, genuine zero vs unknown. Narrowest layer first. Not first failing test -> tdd. Not story Done gate -> xp-agile-delivery."
license: Apache-2.0
compatibility: Any AI coding agent (Claude Code, Codex CLI, Cursor, Windsurf, Gemini CLI). Requires git
  diff or change description; collect mode also requires a runnable test toolchain.
metadata:
  author: rafael
  version: 1.7.1
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
First inspect existing affected tests. Add or extend a test only for a distinct uncovered failure, invariant or contract — apply `test-audit`'s authoring gate (Contract, Regression, Owner, Seam) as reasoning to decide whether a candidate case earns that, and load `test-audit` itself when a case's value, overlap or removal is uncertain; this section only routes it once it does. Use unit/domain checks for local rules; component tests for local interaction; a real integration for the collaborator behavior at issue; browser journeys for browser-dependent or cross-boundary outcomes. These are choices, not a ladder whose every rung must run.

## Retire what proves nothing
To retire or prune tests, use `test-audit`.

A copy-only UI edit does not by itself require UI→API→database. Verify its render, overflow or accessible name as relevant. Config syntax does not prove effective precedence or runtime behavior; test those only where affected. A mocked provider can prove local recovery logic, not that provider's live API. An absent required real integration is BLOCKED, not a mocked substitute.

## Execute and reuse precisely
Use the project's existing runner, lock and environment. Reuse an accepted result as is; re-run it only when the move touched the code, config or dependencies it covered (dirty changes included). Same HEAD alone is insufficient. Preserve exit status and runner summaries. A deliberately empty lint result may be valid; an empty test suite proves no behavior.

Run fast affected checks during iteration.

## Prove the seam, and keep zero distinct from unknown
A layer passing is not the caller arriving. For a changed capability, start at the accepted entry point — UI action, public function, API, CLI, event or worker — and name only the real seams on that path and which of them one real run proves; add a separate command and verdict only for a seam that run does not reach or cannot distinguish; code invoked solely in tests is not evidence of application wiring, and a health endpoint is not a registered route. Inspect both trigger and effect, and observe a persistence claim through the real read path. A UI→API→persistence run happens only when the acceptance crosses API, persistence or auth — an untouched surface creates no obligation.

Then keep the outcome's meaning: zero collection, timeout, failure, xfail, deselection, skip and an unreadable result are not interchangeable with a pass, and a fallback of zero, an empty list or a success badge must not erase a failure. The counterexample is the cheapest proof — the same empty payload after a completed run and after a failed run must produce different consumer behaviour.

## Escalate or finish
Investigate a failure at the smallest responsible seam instead of adding a heavier suite. Widen for an uncovered contract, cross-cutting effect, concurrency/data risk, known escape or explicit gate—not merely because a generic file category matched. Unrelated blocked checks need not stop independent safe work, but still prevent the completion claim that depends on them.

Report one line per check that actually ran — command, verdict, any gap — in the existing work record. Group identical skip causes instead of producing a row for every deselected test. Stop when acceptance and required checks are satisfied with no distinct residual risk.

Read [selection examples](references/test-selection.md) for ambiguous cases, evidence reuse and safe retirement.

Use [the optional evidence note](assets/evidence-note.md) only for a nontrivial result that lacks an existing project format.

For the red-green loop of one behavior, use `tdd`; when a browser journey is the only honest boundary, use `testing-e2e-playwright`.
