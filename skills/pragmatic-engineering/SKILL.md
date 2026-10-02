---
name: pragmatic-engineering
description: "Use when an engineering trade-off needs a choice: simplest thing, reversibility, tracer bullet or prototype, DRY, broken windows, estimate uncertainty, \"is this over-engineered?\". Slicing a story -> xp-agile-delivery."
license: Apache-2.0
metadata:
  author: coding-agent
  version: 1.0.0
  category: domain-expertise
  subcategory: frameworks
  vendor: universal
  lifecycle: active
  coding_agent: true
  audience: developer
  output_format: markdown
  modality: text
  freshness: 2026-10
  short-description: Everyday engineering trade-offs, from Pragmatic Programmer ideas plus XP values
  tags:
  - pragmatic-programmer
  - extreme-programming
  - trade-offs
  - simplicity
  - dry
  - tracer-bullets
  - broken-windows
  - estimation
---

# Pragmatic engineering

How a coding agent makes everyday trade-offs: what to build, how much, how reversibly, and when to stop. It distils ideas from *The Pragmatic Programmer* (Thomas & Hunt, 20th anniversary ed.; tips cited as "T<n>", numbers as listed at pragprog.com/tips, checked 2026-10-02) and the Extreme Programming values (simplicity, communication, feedback, courage, respect), in our own words. Read the book for the reasoning; this file says what to do. Items marked "adapted" are our extension of a tip, not the book's claim.

## Decision procedure

Stop exploring once a step settles the choice, but always price the undo (step 3) before acting, and run steps 5 and 6 on what you do.

1. **Name the consumer and the outcome.** Who uses the result, and what observable thing proves it works? A present requirement or caller justifies work; a hypothetical one does not.
2. **Pick the simplest thing that meets today's outcome.** Reuse project code, then the standard library, then a maintained dependency, before writing new machinery.
3. **Price the undo.** Easy to reverse: decide fast, take the smaller step. Hard to reverse (public API, data format, schema, deletion, shared state): narrow the step and state the rollback first.
4. **Spend the cheapest effort that removes the biggest uncertainty.** Need a real implementation to grow from: tracer bullet. Need an answer you will throw away: prototype. Nothing unknown: just do it.
5. **Get feedback from the real path** (test, command, rendered result) before the next step.
6. **Leave the touched area no worse**, and report what you left undone.

## Principle to behaviour

| Idea | What you do |
|---|---|
| Easy to change (ETC; T14) | Between two designs, pick the one whose likely next change touches fewer places. Without a clear winner take the simpler one; do not design for a guessed future (T43). |
| DRY (T15) | One authority per rule, constant or schema fact. Duplicated knowledge gets one home; code that merely looks alike stays apart. Three similar lines beat a premature abstraction. |
| Orthogonality (T17, T44) | Keep a change local: editing one component should not force edits in unrelated ones. Prefer small interfaces and passed-in data over globals and chained calls. Interface design -> `codebase-design`. |
| No final decisions (T18) | Hide a genuinely volatile choice (vendor, store, format) behind one seam. Do not build a plugin system for a decision nobody will revisit. |
| Tracer bullet (T20) | A thin end-to-end path through the real layers that you keep and widen. It is production code, so it gets the production checks. |
| Prototype (T21) | A throwaway that answers ONE named question. Record the answer, then delete or harden it; it never becomes the product by drift. |
| Broken windows (T5) | On the path you touch, fix small rot you meet (stale comment, dead branch, failing neighbour test). Rot elsewhere is reported to the owner, not folded into the diff. |
| Good-enough software (T8, T36) | Treat quality as a requirement agreed with the user, not endless polish. Deliver what the outcome needs, state known limits, never ship behaviour you know is wrong. |
| Small steps (T42) | One change, one check, then the next. If you cannot say what the last step proved, it was too big. Slicing a story -> `xp-agile-delivery`. |
| Not by coincidence (T62, T34) | Do not keep code you cannot explain because it passes. Say why it failed before, why it passes now, what would break it again. Prove assumptions. |
| Debug from evidence (T31, T32) | Reproduce first, read the actual error, test one hypothesis at a time. Unknown cause -> `diagnosing-bugs`; first failing test -> `tdd`. |
| Refactor early and often (T65) | Restructure in small behaviour-preserving steps with tests green, apart from feature changes. Real duplication and unclear intent earn it; taste alone does not. |
| Estimates (T23, T24, T64) | Give a range with its assumptions and what would move it; re-estimate as the code teaches you. Performance claims are timed, not assumed (T64). |
| Finish what you start (T40, adapted) | Close what you open, or hand it over explicitly. Remove your own scratch files, branches and processes before reporting done. |
| Crash early (T38) | Fail loudly at the first violated assumption; do not swallow errors to look green. Adapted: an unmeasured thing is reported as unmeasured, never as zero. |
| Eliminate, then automate | Ask first whether the step can disappear. Automate what stays with the project's own formatter, linter and scripts, so style is not argued in review. |
| XP values | Communication: surface uncertainty that changes the decision. Courage: challenge an unsupported assumption, delete what is dead, admit your own mistake. Respect: keep diffs small and other people's work intact. |

## "Is this over-engineered?"

Ask each question; a bad answer means cut, defer or reuse.

- Is there a present consumer or requirement for it? If not, defer.
- Does an existing mechanism (code, library, platform feature) already do the job? If so, reuse it.
- Can you state in a few sentences why it exists and how it fails? If not, simplify or understand it first.
- Does the abstraction give a present benefit, such as isolating a volatile choice or enabling a test? A single-caller abstraction without one is tidiness, not design.

An extra found in a diff is stripped with `kill-slop`, keeping the behaviour.

## Red flags

- "We might need it later" with no named consumer.
- A flag, layer or config key with one caller and one possible value.
- A copied block whose knowledge now lives in two places.
- A spike that grows tests, config and users without a decision to promote it.
- A TODO, comment or skipped test standing in for a decision about debt on the path you are changing.
- A fix nobody can explain; a big-bang change with no intermediate runnable point.
- A confident estimate or "done" with no evidence behind it.
- Broken-window zeal: fixing everything nearby until the diff cannot be reviewed.

## What this is not

- Not a process: no ceremony, planning documents or gates of its own.
- Not a style guide: it never overrides the repository's conventions or the user's explicit instructions.
- Not a licence to skip tests or safety checks in the name of "simple".
- Not a rule against abstraction: a seam that already pays for itself stays.
- Not a substitute for the book: it records decisions, not the book's arguments or examples.
