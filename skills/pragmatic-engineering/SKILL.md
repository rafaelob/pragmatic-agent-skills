---
name: pragmatic-engineering
description: "Use when a design trade-off needs a choice: simplest thing, reversibility, tracer bullet, estimate, \"is this over-engineered?\". Proven removal -> kill-slop. Interfaces -> codebase-design. Slices -> xp-agile-delivery."
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

How a coding agent makes everyday trade-offs: what to build, how much, how reversibly, and when to stop. It distils ideas from *The Pragmatic Programmer* (Thomas & Hunt) and the Extreme Programming values, in our own words. Read the book for the reasoning; this file says what to do.

## Decision procedure

Stop exploring once a step settles the choice, but always price the undo (step 2) before acting, and run steps 4 and 5 on what you do.

1. **Name the consumer and the outcome.** Who uses the result, and what observable thing proves it works? A present requirement or caller justifies work; a hypothetical one does not.
2. **Price the undo.** Easy to reverse: decide fast, take the smaller step. Hard to reverse (public API, data format, schema, deletion, shared state): narrow the step and state the rollback first.
3. **Spend the cheapest effort that removes the biggest uncertainty.** Need a real implementation to grow from: tracer bullet. Need an answer you will throw away: prototype. Nothing unknown: just do it.
4. **Get feedback from the real path** (test, command, rendered result) before the next step.
5. **Leave the touched area no worse**, and report what you left undone.

## Principle to behaviour

| Idea | What you do |
|---|---|
| Easy to change (ETC) | Between two designs, pick the one whose likely next change touches fewer places. Without a clear winner take the simpler one; do not design for a guessed future. |
| Orthogonality | Keep a change local: editing one component should not force edits in unrelated ones. Prefer small interfaces and passed-in data over globals and chained calls. Interface design -> `codebase-design`. |
| No final decisions | Hide a genuinely volatile choice (vendor, store, format) behind one seam. Do not build a plugin system for a decision nobody will revisit. |
| Tracer bullet | A thin end-to-end path through the real layers that you keep and widen. It is production code, so it gets the production checks. |
| Prototype | A throwaway that answers ONE named question. Record the answer, then delete or harden it; it never becomes the product by drift. |
| Good-enough software | Treat quality as a requirement agreed with the user, not endless polish. Deliver what the outcome needs, state known limits, never ship behaviour you know is wrong. |
| Refactor early and often | Restructure in small behaviour-preserving steps with tests green, apart from feature changes. Real duplication and unclear intent earn it; taste alone does not. |
| Estimates | Give a range with its assumptions and what would move it; re-estimate as the code teaches you. Performance claims are timed, not assumed. |

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
