---
name: diagnosing-bugs
description: "Use to reproduce a bug from evidence, or a failing test whose code may be wrong, and isolate one cause before changing code. Not proving a seam is wired -> layered-testing-executor."
license: Apache-2.0
metadata:
  tags:
  - debugging
  - bug-diagnosis
  - feedback-loop
  - root-cause-analysis
  - regression
  - code-quality
  - user_level:intermediate
  version: "1.5.3"
  author: coding-agent
  category: code-quality
  subcategory: analysis
  vendor: universal
  lifecycle: active
  coding_agent: true
  audience: developer
  output_format: markdown
  modality: text
  freshness: 2026-08
  upstream: https://github.com/mattpocock/skills
  upstream_mode: adapted
  upstream_baseline_commit: 5b15a47f2d7150f545fbcacbfe381787fc0230dc
  upstream_baseline_date: 2026-08-21
  upstream_author: Matt Pocock
  upstream_path: skills/engineering/diagnosing-bugs/SKILL.md
  adaptation_summary: 'Adopted 1dab982: Phase 6 no longer hands off to a
    user-invoked sibling. House HITL is Python, not bash. Redact section is
    ours-plus-upstream. Loop taxonomy and completion-gate wording stay house.'
  upstream_not_adopted:
    em-dash-sweep: Cosmetic 3216582; house keeps existing punctuation.
    Skill-tool phrasing: House names sibling skills in catalog kebab-case, never
      "call the Skill tool".
    "Ways to construct one, in roughly this order": >-
      The active workflow intentionally groups the upstream ten loop choices into
      four selection buckets in `### Choose one feedback loop`; complete ordered
      setup guidance remains in `references/LOOP_TAXONOMY.md`, and the Python HITL
      implementation is `scripts/hitl_loop_template.py`.
---

# Diagnose by discriminating evidence

Read the actual error, reported scenario and affected revision/configuration. Inspect relevant logs without exposing secrets or personal data. Reduce the symptom to a small repeatable check on the boundary that can reproduce it. A health check or import failure is not a reproduction of a wrong business result.

Form a hypothesis with a predicted observation. Choose the next inspection or experiment that distinguishes plausible causes; do not change several unrelated things or rerun the same failing command without changing the hypothesis. Use a controlled schedule for a suspected race and representative measurement for a performance defect, rather than arbitrary sleeps or speculative optimization.

## Useful regression
When the defect is reproducible, strengthen the existing behavioral test that should have caught it and verify that it fails for the defect and passes after correction. Add a new test only when no existing test can be made sensitive to it: a regression test without a genuine gap in behavior coverage is noise. Avoid duplicating the same assertion across unit, service and browser layers unless each exposes a distinct failure boundary. Read `references/LOOP_TAXONOMY.md` when choosing or constructing the reproduction's pass/fail signal; its last-resort loop is `scripts/hitl_loop_template.py` (copy it, edit `run()`, the human follows the terminal prompts).

If reproduction is unavailable, continue useful permitted static investigation and report the limit. Static reasoning can demonstrate some defects, but it does not demonstrate runtime recovery. Do not manufacture a failing test unrelated to the symptom or claim a runtime fix from a plausible patch alone.

After the correction, check the original scenario and directly related risk, then run applicable project gates. Search for siblings only when the same causal mechanism plausibly applies. Remove owned temporary instrumentation; retain the regression and a brief explanation in the current work item. Do not turn every bug into a whole-repository audit.

When the cause is already established and the fix needs its failing test first, use `tdd`; for a Windows-only path, quoting or encoding failure, use `windows-shell-interop`.
