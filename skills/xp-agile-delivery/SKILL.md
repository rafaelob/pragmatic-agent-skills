---
name: xp-agile-delivery
description: "Use when a story moves from ready to in-progress, or a mission needs slicing. Beyond one slice: blocked sub-issues via tdd. Not test layers -> layered-testing-executor. Trade-off doubt -> pragmatic-engineering."
license: Apache-2.0
metadata:
  author: rafael
  version: 1.6.3
  category: process-automation
  subcategory: sop-workflows
  tags:
  - xp
  - agile
  - tdd
  - ci
  - invest
  - user-stories
  - acceptance-criteria
  - coding_agent
  - delivery
  vendor: universal
  short-description: XP values, vertical slices, pairing and risk-sized feedback
  audience: developer
  output_format: markdown
  modality: text
  coding_agent: true
  lifecycle: active
---

# XP delivery with useful feedback

## Start with a usable result
Read the request, current acceptance and work authority. Express the next slice as a consumer-visible result, not a list of layers. The consumer may be a person, API client, worker or library caller. An API-only delivery is legitimate when that API is the agreed product; a UI feature is not complete merely because its API exists.

Keep communication, simplicity, feedback, courage and respect in the decisions: surface ambiguity that changes the solution, remove unnecessary work, exercise the result early and preserve others' valid work. Resolve nonblocking uncertainty during the task instead of requiring another discovery document. Trade-off or over-engineering doubt -> `pragmatic-engineering`.

## Slice into the tracker item, never into a plan file
When the mission is larger than one slice, cut it before writing code: name the real entry point and observable result of each slice, and keep a learning spike, an implemented slice and the full requested outcome as three distinct states. The map is the repo's one declared tracker item (the project's tracker), with native blocked sub-issues when the tracker supports them — never a local plan file, PRD, risk register, test ledger or sprint folder, unless the user explicitly asks for a plan or PRD, in which case that document is the deliverable. Update it when learning changes the next decision, not after every keystroke. A clear low-risk edit needs a short execution sequence, not a plan at all.

## Build, test and integrate
Drive new behavior through `tdd`. Prefer extending an existing meaningful test over creating an overlapping suite. Which layers to run belongs to `layered-testing-executor`.

## Collaborate without manufacturing handoffs
Use a specialist when risk, unfamiliarity or independent work justifies the cost. When pairing, name a driver who writes and a navigator who challenges the diff; hand over write ownership explicitly when switching. A reviewer does not take quality responsibility away from the implementer. Do not force a pair, rotation ceremony or approval chain for every task.

Finish useful work before opening unrelated fronts. Respect human attention, execution budgets and shared machine limits. Urgency reduces batch size and optional work, not authorization, data protection or required acceptance. A deployment-ready change and a deployed feature are different states.

Stop after the slice meets its acceptance and applicable gates. Capture real bottlenecks in the existing tracker; add no velocity dashboard, sprint ledger or retrospective ritual by default.

Read [XP choices](references/xp-choices.md) for a concrete trade-off between testing, pairing, integration and cadence. Read [the XP & Agile guide](references/XP_AGILE_GUIDE.md) for practice tables and story-splitting patterns when a concrete example is needed beyond this skill's principles.

Use [the optional slice note](assets/slice-note.md) only when the existing work item lacks a useful format.
