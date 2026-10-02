---
name: refactoring-catalog
description: "Use when code has real duplication, confusing intent or excess coupling and trusted behavioral tests exist. Gives small safe moves (extract, rename, move), green throughout. No trusted tests -> legacy-code-change."
license: Apache-2.0
metadata:
  tags:
  - code-quality
  - refactoring
  - code-smells
  - tech-debt
  - fowler-catalog
  - openrewrite
  - jscodeshift
  - rector
  - debt-quadrant
  - user_level:intermediate
  version: 1.3.0
  author: coding-agent
  category: code-quality
  subcategory: quality-validation
  vendor: universal
  lifecycle: active
  coding_agent: true
  audience: developer
  output_format: markdown
  modality: text
  freshness: 2026-04
---

# Refactor only what improves the current change

Name the pain: duplicated knowledge, confusing intent, difficult change, excessive coupling or an untestable boundary. Similar code with independent domain meanings need not be unified. Do not refactor solely to meet an invented line limit, layer count or pattern preference.

Find adequate existing behavioral tests. When coverage of the relevant contract is absent, add the smallest characterization needed to make the structural move safe. Distinguish observed legacy behavior from a known defect; do not freeze a defect as a desired contract. Keep intentional behavior changes separately understandable.

Prefer extract, rename, move or simplify over introducing a new engine or framework. Read `references/REFACTORING_MOVES_REFERENCE.md` for the concrete moves (preconditions, mechanics, verification) once the pain is named. Use an existing codemod where appropriate -- read `references/AUTOMATED_REFACTORING_TOOLS.md` for the tool catalog by language before hand-writing an AST transform -- inspect its scope and preserve unrelated WIP. Short green-to-green moves are compatible with a coherent final commit; do not create a PR per micro-edit unless the workflow requires it.

## Test stability through change
Behavioral tests should continue to pass when only implementation changes. Remove coupling to private method names or call order unless the order itself is contractual. Do not add tests for renamed helpers just to replace deleted brittle ones. Retire a test only after its protection is preserved elsewhere, its behavior was removed or its assertion was shown not to protect a relevant requirement.

Rerun affected checks after the structural move and applicable final gates at integration. Do not rerun unrelated full suites after every local rename. Stop when the stated pain is resolved; no speculative adapter, abstraction for hypothetical consumers or broader modernization campaign.

For the interface decision that precedes the move, use `codebase-design`; for choosing which checks must stay green while it happens, use `layered-testing-executor`.
