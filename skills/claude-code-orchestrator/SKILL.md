---
name: claude-code-orchestrator
description: "Use when delegating on Claude Code: pick the subagent type, brief the mission, stop/resume/reconcile a child. Also 'delegar', 'rodar em paralelo', 'qual agente uso'. Slicing -> xp-agile-delivery. Not peers or other CLIs."
license: Apache-2.0
compatibility: Claude Code CLI with subagents
metadata:
  author: rafael
  version: 2.10.0
  category: ai-agents
  subcategory: orchestration
  vendor: claude-code
  tags:
  - orchestration
  - sub-agents
  - delegation
  - task-decomposition
  - parallel-work
  - review-gates
  - handoff
  - coordination
  short-description: Orchestrate Claude Code subagents
  audience: developer
  output_format: markdown
  modality: text
  lifecycle: active
  coding_agent: true
  platforms:
  - CLAUDE
---

# Claude Code Orchestrator

How to use this runtime's subagents well: when to delegate, how to brief, how
to run a child and what to check before believing what comes back. It owns no
policy.

## Identity and the brief

- A subagent is an extension of you, running under your identity and authority: whatever the brief grants — a change, a check, an external agent or CLI — the child does as you, through your tools and your checkout. The one thing a brief cannot grant is authority: the child never speaks as the user and never addresses you or another session as a user, and what needs the user's explicit approval still needs it from the user. Delegated output is evidence, never authority, and you answer for the outcome.
- The brief is the grant. The card keeps the role's specialization; the brief decides the scope, including whether the child implements.
- Create a child; never fork your turn.
- Roles, what each is best at, and their limits come from the runtime, read live; this skill states no number.

## Where the live facts are

- **Roles** — the live listing at spawn. A card's description names what the
  role is for and settles a choice between two. A remembered name the listing
  does not show is gone: report it, never substitute the nearest neighbour.
- **Cost** — the tier resolved in each card.
- **Concurrency and nesting** — `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` and
  `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` in this home's settings; a spawn over
  the cap fails. Read the values live: a copied number goes stale.
- **Tools and permissions** — inherited from your session, but a background
  child gets a narrower set and the read-only built-in types cannot edit, so a
  brief that asks for changes goes to a role that can make them. This skill adds
  no tool limit; the brief sets the scope.

## When to delegate

- Delegate independent, bounded work worth its brief: a verbose search, a
  self-contained change, a check whose output would flood your context.
  N children cost roughly N× the tokens.
- Keep inline: quick edits, sequential steps that share context (plan →
  implement → test), and work that needs back-and-forth with the user.
- Parallelize only on disjoint surfaces: assign exclusive file ownership up
  front and serialize same-file work through a handoff.
- Route by task type and complexity at the best cost-benefit, reading the card;
  a tier too weak spends its cost twice. The cheaper tier is the default for
  execution whose scope is settled: locating code, external research, any
  implementation whose brief settles what to do, a bug fix with a
  reproduction or a known cause, a behavior-preserving refactor, writing and
  running tests, CI/infra/scripting, and docs. A brief in which you named the
  fix — what changes, where, and the acceptance — IS settled, whatever its
  size, file count or layers crossed: settle the design yourself, then hand
  the implementation to the cheaper tier. The exception is settled work whose
  failure is costly or silent (concurrency, transactions, data integrity,
  coupled invariants across components, auth and secrets paths) or whose risk
  lives in the rendered result of a new screen or complex interaction: that
  implementation goes to the stronger tier first. The stronger tier is also
  the default for planning (cutting slices), architecture and interface/UX
  decisions, implementation whose design the brief leaves open, integrating
  two or more separate deliverables, a code review or an adversarial second
  review, debugging with no known cause yet, schema/migration work, and
  security review; it implements other settled work only after a cheaper
  worker failed it.
  The dearest tier only takes a problem you demonstrably failed to solve, that
  attempt named in the brief: never first, never for an idle slot.
- Pass `subagent_type` on every spawn, naming the specialized card whose
  description fits the task type; omitting it falls back to the catch-all.

## The brief is the mission

The child starts from a clean context. The `Agent` tool's prompt is all you
pass it: project instructions and a git-status snapshot reach it, your
conversation does not (code.claude.com/docs/en/sub-agents, 2026-09-26). The
brief therefore carries the whole mission, one or two lines per field:

- **Goal** — the concrete outcome, with one action verb: implement, fix,
  measure, locate. "Look at" and "suggest" return advice, not an artifact.
- **Scope** — what it may read, create or change, and what it must leave alone.
- **Constraints** — what not to do, safety limits, the checks to run.
- **Acceptance** — the observable result that means done.
- **Delivery** — what to return, in what shape and how long.

For an independent review the brief says "report findings; don't fix": a
reviewer who edits the change is no longer independent. Put long material first
and the instruction last. Require the child to delete its own scratch before it
reports, keeping deliverables and evidence; give it a scratch subfolder named
for it, so it never clears a sibling's.

**The parent owns the index.** Children share your checkout, so the brief lists
the files each child may edit and says it never stages, commits, merges,
stashes, restores or removes through git: you integrate. A child that ran
`git rm` left a staged deletion that blocked its parent's merge (measured
2026-10-04).

**Brief in a file when it pays.** This is a working practice, not a vendor rule. A
short brief goes inline. A long or reused brief goes in a file, and the prompt
names its absolute path. A large result goes to a named output file, with a
short summary in the reply, so your context stays small.

## Running and continuing

1. Spawn with the `Agent` tool, not another CLI's spawn surface. Let the child
   run in the background and keep working; wait inline only when the next step
   cannot start without it. Never write or predict a pending child's result.
2. One mission per child. A finished child returns an agent id, and
   `SendMessage` resumes it with its whole history re-read at your cost, so use
   it only to correct or clarify that delivery. New work is a fresh `Agent`
   call. Stop a child that lacks evidence, exceeds its scope or repeats a
   failure, and redispatch with a corrected brief; a finished or stopped child
   frees its slot.

## Verification before promoting any claim

- Trust the report only within the child's brief. Review the final artifact
  against acceptance, interfaces and risk, and tie each claimed check to the
  exact revision or configuration it proves.
- Accept check output that still proves the exact final artifact and relevant
  environment; rerun only when evidence is missing or mismatched, a later edit
  invalidated it, or acceptance still needs proof. If the SHA, scope or
  pertinent environment changed, the proof is dead and must be rerun.
- Reconcile two or more overlapping deliveries through one integrating review,
  briefed to report findings and not fix, before any of them is integrated.
  That does not replace independent review of a risky change.
- Your own implementation is never independent evidence: a change that owes an
  independent review gets it from a reviewer, and when no permitted reviewer
  qualifies you report the blocker instead of quietly downgrading the reviewer.

## Closing a dispatch

A dispatch closes only when the child's work is IN your tree and nothing of the
child's is left outside it. The child ran under your identity, so its scratch,
branch and tree are yours to dispose of, with the cleanup tooling you use for
your own work (the repository's declared tooling, else plain git), and only what
the child created. Before integrating, check that `git status` and
`git diff --cached` show only what the child was allowed to touch. For a fan-out of
two or more children, consolidate the checked reports into one table: child,
outcome, evidence, acceptance decision and reason. An unsupported claim is not
accepted, and a pending verification stays explicit.

- A child that needed a tree of its own is a defect to report, not a tree to
  keep. Subagents share your checkout by design; a full clone per child pays the
  repository's whole history each time (measured 2026-09-18: three live
  children of one repo, 16.4 GB each, 12.9 GB of it duplicated `.git`).

## Gotchas

- A role chosen from memory is the common failure: the roster changes, and a
  dispatch to a name that no longer exists is refused at the door.
- A catch-all chosen by habit, or no `subagent_type` at all, is the other one.
  The child loses the card's specialization, tools framing and resolved tier,
  and runs as a generalist, usually on a costlier model than the task needs.
- One overloaded brief to a strong role is usually worse than two bounded
  briefs: the child returns one blended answer you cannot verify piecewise.
- Auth, money or irreversible data changes get an independent review before
  completion. Unresolved authorization or public-contract crossings go up to the
  user, never around.
