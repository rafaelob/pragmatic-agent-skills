---
name: code-review
description: "Use when asked to review a diff, PR or uncommitted change for correctness, regressions and unneeded complexity. Not OWASP/authz -> security-review. Not deleting extras -> kill-slop."
license: Apache-2.0
metadata:
  tags:
  - code-quality
  - code-review
  - pr-review
  - pull-request
  - quality-gate
  - severity-scoring
  - standards-compliance
  - architecture-review
  - commit-hygiene
  - user_level:advanced
  version: 2.4.4
  author: rafael
  category: code-quality
  subcategory: quality-validation
  vendor: universal
  short-description: Evidence-based PR and code review, findings split into defect, hypothesis and preference
  audience: developer
  output_format: markdown
  modality: text
  coding_agent: true
  replaces: pr-reviewer
  lifecycle: active
  upstream: https://github.com/mattpocock/skills
  upstream_author: Matt Pocock
  adaptation_summary: 'Partial graft, not a fork of the upstream skill: from skills/engineering/code-review/SKILL.md
    at c0d6901 (2026-08-06) this skill keeps the Spec vs Standards finding tags and the Fowler smell
    baseline in references/CODE_REVIEW_CHECKLIST.md. Everything else is house text. The upstream MIT
    text ships as LICENSE-mattpocock-skills.txt; the skill as a whole is Apache-2.0.'
---

# Review the change, not your preferred rewrite

Read the request, diff, affected contracts and available test evidence. Focus on behavior, safety, compatibility and maintenance problems introduced or exposed by this change. Review the actual candidate including relevant uncommitted changes; a HEAD label alone does not identify a dirty tree.

For a finding, explain the location, plausible input or call path, incorrect result and why it matters. Separate a demonstrated defect, a hypothesis needing a check and an optional preference. No minimum finding count. Do not reject a correct idiomatic design because another design is fashionable.

## Review tests for information
Ask what failure each new test detects, whether it exercises production behavior, and whether its expected result is independent. Flag brittle snapshots, mock-only assertions, exact incidental wording, duplicate layers and unchanged trivial wrappers when they add no distinct protection. Do not demand another test merely because a file changed or a percentage dropped; preserve any genuinely required threshold until its owner changes it.

Request a targeted additional check only for a concrete uncovered risk. Reuse valid evidence from the implementer after checking candidate, configuration and scope. Evidence from a different environment cannot prove that environment's integration. No automatic full rerun, new test framework or expanded audit.

Report the material findings and limits. A read-only review does not authorize edits, CI changes or remote scans. Approve or finish the review once the requested scope is assessed; repeat only for a changed candidate, answered blocker or newly discovered risk. A review report is not a replacement for the project's release decision.

See [an optional finding example](assets/finding-example.md) when a substantive defect needs a structured explanation. Read `references/CODE_REVIEW_CHECKLIST.md` for an optional Fowler smell baseline, consulted only when the change at hand suggests one.

Write the finding in the shape of `assets/finding-example.md`, or of `assets/pr_review_template.md` when the project wants a fixed review write-up. For a defect whose cause the review can only suspect, use `diagnosing-bugs`; for proving the change is reachable end to end, use `layered-testing-executor`.
