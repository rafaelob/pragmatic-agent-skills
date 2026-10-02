---
name: security-review
description: "Use for a structured security review: threat modelling, OWASP checks and severity-ranked findings. Not an ordinary correctness pass -> code-review."
license: Apache-2.0
metadata:
  author: coding-agent
  version: 1.2.1
  category: code-quality
  subcategory: code-review
  vendor: universal
  lifecycle: active
  coding_agent: true
  tags:
  - security
  - review
  - user_level:advanced
  audience: developer
  output_format: markdown
  modality: text
---

# Review the affected security boundary

Read the change, intended actors, data sensitivity and existing controls. Trace attacker-controlled input to the effect it can cause. Expand beyond the diff when the changed boundary depends on another component; do not launch a generic audit of the whole portfolio. Read `references/THREAT_MODELING_FRAMEWORKS.md` when the boundary or actors are unclear enough to warrant STRIDE, PASTA or DREAD before scoping checks.

Check the applicable authorization, tenant isolation, input limits, secret handling and safe failure. The client or model cannot supply its own authority. A prompt, annotation or hidden button is not a substitute for enforcement. Keep nonapplicable threat categories out of the work instead of mechanically filling every checklist. Read `references/OWASP_TOP10_2025_CHECKLIST.md` for the category-by-category detection, fix and test patterns; read `references/RATIONALIZATIONS_TO_REJECT.md` before dismissing a plausible material risk as not applicable, not for an obviously unrelated category.

## Use tests that can expose the violation
Prefer the relevant existing negative test plus its permitted control. Exercise the real enforcement point: a mocked authorization decision cannot prove access isolation. Choose abuse inputs for the changed vector, not every theoretical attack. Simple local fixtures are preferable to a new scanning service for a local fix.

Use scanners already approved for the target and interpret findings. Read `references/SAST_DAST_TOOLING_GUIDE.md` when choosing or interpreting a SAST/DAST/SCA tool. Do not run live scans, destructive inputs or external data egress merely because credentials exist. Do not raise security thresholds, remove negative cases or mark unavailable checks passed for speed.

Report exploit path, consequence, evidence and scope. Distinguish a confirmed defect from untested exposure. Reuse valid test evidence and retest the corrected boundary; no mandatory repeated full audit. Stop when the scoped review is complete, with any unresolved material security risk explicitly blocking the claim it affects.
