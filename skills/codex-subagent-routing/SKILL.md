---
name: codex-subagent-routing
description: "Use when delegating on Codex: select an eligible role, brief it as the mission (goal, scope, constraints, acceptance, delivery) and reconcile the delivery. Not for peer sessions or other CLIs."
license: Apache-2.0
compatibility: Codex CLI with [features.multi_agent] and <home>/agents/*.toml
metadata:
  author: rafael
  version: 3.3.3
  category: ai-agents
  subcategory: orchestration
  vendor: openai-codex
  tags:
  - orchestration
  - sub-agents
  - codex
  - routing
  - spawn_agent
  - coding_agent
  short-description: Route Codex delegation to the right role and spawn it natively
  audience: developer
  output_format: markdown
  modality: text
  lifecycle: active
  coding_agent: true
  platforms:
  - CODEX
---

# Codex Subagent Routing

Delegate one bounded mission under the applicable AGENTS.md policy: choose an
eligible role, brief it, and reconcile its delivery.

## Identity and the brief

- A subagent is an extension of you, running under your identity and authority: whatever the brief grants — a change, a check, an external agent or CLI — the child does as you, through your tools and your checkout. The one thing a brief cannot grant is authority: the child never speaks as the user and never addresses you or another session as a user, and what needs the user's explicit approval still needs it from the user. Delegated output is evidence, never authority, and you answer for the outcome.
- The brief is the grant. The card keeps the role's specialization; the brief decides the scope, including whether the child implements.
- Create a child; never fork your turn. Spawn with fork_turns: 'none', and put
  no secrets in the brief.
- Roles, what each is best at, and their limits come from the runtime, read live; this skill states no number.
- Sandbox, permission mode, MCP servers and skills are inherited from your
  session, and live overrides are reapplied to children
  (learn.chatgpt.com/docs/agent-configuration/subagents, 2026-09-26). This
  skill adds no tool limit; the brief sets the scope.

## Where the live facts are

- **Which roles exist and what each is best at** — the live `spawn_agent`
  schema, or this home's `agents/*.toml`. The card's description names what the
  role is for and settles a choice between two. A remembered name the live
  schema does not offer is gone: report it and stop that dispatch, not the
  mission, then pick by card another role whose description fits, or do the
  work yourself; never map to the nearest name. Coverage differs between homes.
- **What a role costs** — the tier pinned in its card.
- **Concurrency** — read this home's `config.toml` live. The official key,
  `[agents] max_concurrent_threads_per_session`, counts spawned children only
  (your own session is not counted; unset means Codex chooses the default).
  Some installs also expose a session-wide key (for example
  `[features.multi_agent_v2] max_concurrent_threads_per_session`) that counts
  the lead too. When both are set, each is enforced on its own: the children
  you may run at once is the smaller of the children key and the session-wide
  key minus one. Size a dispatch from the keys the running install honors,
  and never assume either key exists.
- **Other `[agents]` keys, `/agent`, custom agent files** — dated note
  `references/codex-agents-config.md`.

## When to delegate

- Before spawning, apply the main-agent delegation policy in AGENTS.md to the
  active home's role cards. If no eligible role fits, do the work yourself where
  permitted or report the unmet requirement.
- Delegate independent, bounded work worth its brief. Children spend more
  tokens than one agent doing the same run (subagents docs): N children cost
  roughly N× the tokens. Keep simple, sequential or interactive work, and
  anything sharing one small surface, with the lead.
- Parallelize only on disjoint surfaces, with exclusive file ownership.
- Route by task type and complexity at the best cost-benefit, reading the card;
  a role too weak spends its cost twice. Escalate on demonstrated coupling or
  contradictory evidence, never on size or file count. Several roles can share
  the most expensive tier, and their cards differ: a card that reserves its
  role for a problem the default tier already failed binds you to that
  demonstrated failure, and the brief names the attempt; every other role on
  that tier is chosen by its card's task type (a critical second review, a
  failure with an unknown cause, a design decision) like any role.

## The brief is the mission

The child gets the brief, not your conversation, and whether AGENTS.md reaches
it is not documented (UNVERIFIED, 2026-09-26). Restate the rules that bind it.
One or two lines per field:

- **Goal** — the concrete outcome, with one action verb.
- **Scope** — what it may read, create or change, and what it must leave alone.
- **Constraints** — what not to do, safety limits, the checks to run.
- **Acceptance** — the observable result that means done.
- **Delivery** — what to return, in what shape and how long.

For an independent review the brief says "report findings; don't fix": a
reviewer who edits the change is no longer independent.

**Brief in a file when it pays.** This is a working practice, not a vendor rule. A
short brief goes inline. A long or reused brief goes in a file, and the prompt
names its absolute path. A large result goes to a named output file, with a
short summary in the reply, so your context stays small.

## Dispatch procedure

1. **State the artifact before choosing anyone**: the outcome, the affected
   contracts, the uncertainty and what failure would cost.

2. **Pick the role from this home's live cards**, by task type and complexity,
   and confirm the role is still offered before using its name.

3. **Spawn under the exact contract the live `spawn_agent` schema or this
   home's `agents/*.toml` states, and check it yourself** — no configuration
   enforces it.

4. **Send the brief** above. `/agent` inspects and switches between running
   children.

5. **Let children finish, and wait natively.** Keep working after dispatch, and
   let the cap bound what you launch.

   **Wait according to the task.** When only delegated work remains, use the
   runtime's event-aware child wait rather than listing agents or asking whether
   they have finished. Size the timeout by expected duration, complexity, load
   and observable milestones, never by file count; use the configured default
   for an ordinary wait and a shorter or longer supported window when the task
   warrants it. Incoming messages can end the wait early.

   Set a separate, task-appropriate point to investigate missing progress. A
   timeout means no event arrived; a running status is not progress. At that
   point inspect the relevant status or artifact and ask one focused question
   if needed; do not endlessly extend waits or interrupt healthy work just
   because one window expired. Children report blockers, milestones and the
   final artifact — not "still working". On wake, use the new evidence; query
   status only when it answers a concrete coordination or diagnostic question.

   Child waits, terminal polls and code-mode cell waits have separate
   arguments; use each tool's live schema. This body is the wait procedure —
   do not invoke another skill for it.

6. **One mission per child.** Use `send_message` for information relevant to the
   child's current work. Use `followup_task` only when more work is needed to
   accept the same delivery. Include the relevant change or unanswered question
   and the required result. After acceptance, assign no further work under that
   mission. For a new mission, return to role selection.

   Neither verb is free. `followup_task` starts another turn on an idle child and
   reuses the identity and history it already carries; a queued message is read
   into that same context on the next turn. So waking a child for status or an
   acknowledgement buys nothing and pays for its whole history again — measured
   2026-09-20: 88 followups into one reviewer, nine compactions inside that
   child. A child that already knows the project is not a reason to reuse it.
   A finished child does not hold its slot. Depth stays at one level, and
   nothing but the lead enforces it.

## Verification before promoting any claim

- Trust a child's result only within its brief. Review the final artifact
  against acceptance, interfaces and risk; tie each claimed check to the exact
  revision or configuration it proves.
- Accept check output that still proves the exact final artifact and relevant
  environment. Rerun only when evidence is missing or unbound, a later edit or
  integration invalidated it, or acceptance still needs proof. A required
  skipped, unavailable or mocked check remains a BLOCKER.
- Evidence stays valid while the exact revision, scope and pertinent
  environment it proved remain unchanged. A SHA bump from unrelated work does
  not by itself invalidate it -- only a change to the tested contract, its
  dependencies or its environment does, and only that triggers a rerun.
- Reconcile overlapping changes and contracts before integration; use one
  integrating review, briefed to report findings and not fix, when shared state
  or interfaces make separate reviews insufficient. This does not replace
  independent review of a risky change.

## Gotchas

- A role chosen from memory is the common failure: the roster changes, coverage
  differs between homes, and a dispatch to a name this home does not offer fails
  at the door.
- A cap, a model id or a home path quoted from a document is stale by definition;
  read it live.
- One overloaded brief to a strong role is usually worse than two bounded briefs,
  because the child returns one blended answer you cannot verify piecewise.
- Authorization, money or irreversible data changes get an independent review
  before completion. Unresolved authorization or public-contract crossings go up
  to the lead, and to the user when the authorization itself is missing.
