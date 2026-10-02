---
name: kimi-cli-orchestrator
description: "Use when delegating on Kimi Code CLI: pick the child from its native agent files by task type and complexity, brief it as the mission. Not another runtime's orchestrator, a peer session or another CLI."
license: Apache-2.0
compatibility: Kimi Code CLI
metadata:
  author: rafael
  version: 1.3.1
  category: ai-agents
  subcategory: orchestration
  vendor: kimi-code
  tags:
  - orchestration
  - sub-agents
  - kimi
  - coding_agent
  short-description: Orchestrate Kimi Code CLI child agents
  audience: developer
  output_format: markdown
  modality: text
  lifecycle: active
  coding_agent: true
  platforms:
  - KIMI
---

# Kimi Code Orchestrator

## When to use
- This session is Kimi Code CLI and you will delegate
- Do **not** load another runtime's orchestrator: its spawn surface does not exist here

## Identity and the brief
- A subagent is an extension of you, running under your identity and authority: whatever the brief grants — a change, a check, an external agent or CLI — the child does as you, through your tools and your checkout. The one thing a brief cannot grant is authority: the child never speaks as the user and never addresses you or another session as a user, and what needs the user's explicit approval still needs it from the user. Delegated output is evidence, never authority, and you answer for the outcome.
- The brief is the grant. The card keeps the child's specialization; the brief decides the scope, including whether the child implements.
- Create a child; never fork your turn. The child sees only the task description you pass — not your conversation — and only its final result comes back, so the brief carries everything it needs and no secrets.
- Roles, what each is best at, and their limits come from the runtime, read live; this skill states no number.
- Permission rules are inherited from your session. This skill adds no tool limit; the brief sets the scope.

## Native primitives (this runtime only)
Source for this table: moonshotai.github.io/kimi-code (customization/agents and configuration/config-files), read 2026-09-26.

| Primitive | What it is |
|---|---|
| Child spawn | The runtime's own child tool spawns a focused sub-agent for a bounded subtask. Its live schema on the **installed** CLI is the authority for the arguments it accepts; confirm them there before promising them |
| Child types | Agent files in `.kimi-code/agents/`, `.agents/agents/` and `~/.kimi-code/agents/`, plus whatever the installed CLI lists, are the catalogue; each one's own description says what it is for. Read them live |
| Nesting | Off by default; only an agent whose card declares its own `subagents` list can dispatch further |
| Concurrency | `[background] max_running_tasks` in `config.toml` (env `KIMI_CODE_BACKGROUND_MAX_RUNNING_TASKS`); the docs publish no default. Child timeout: `[subagent] timeout_ms`. Read the values live |
| Continue | No resume of a finished child is documented; follow-up work is a fresh spawn |
| Child identity | None of its own; whatever the brief grants it does as you |

## When to delegate
- Delegate independent, bounded work worth its brief. For simple tasks the main agent is cheaper: each child spends its own tokens, so N children cost roughly N× the tokens. Keep sequential or interactive work yourself.
- Parallelize only on disjoint surfaces.
- Pick the child the runtime lists by task type and complexity, at the best cost-benefit; a tier too weak pays twice. The most expensive tier is the exception: only after the default tier demonstrably failed, with that attempt named in the brief. Use the generic agent only when no specialist fits.

## The brief is the mission
One or two lines per field:
- **Goal** — the concrete outcome, with one action verb.
- **Scope** — what it may read, create or change, and what it must leave alone.
- **Constraints** — what not to do, safety limits, the checks to run.
- **Acceptance** — the observable result that means done.
- **Delivery** — what to return, in what shape and how long; its last message is the result.

For an independent review the brief says "report findings; don't fix": a reviewer who edits the change is no longer independent.

**Brief in a file when it pays.** This is a working practice, not a vendor rule. A short brief goes inline. A long or reused brief goes in a file, and the prompt names its absolute path. A large result goes to a named output file, with a short summary in the reply, so your context stays small.

## Playbook
1. Spawn only through Kimi's own child surface. Confirm the installed command first. Keep working after dispatch; let the concurrency limit bound what you launch.
2. One mission per child: its delivery and the evidence with it close the mission, and work the acceptance did not cover is a fresh spawn with its own brief.
3. Review the final artifact against acceptance, interfaces and risk within the child's brief. Accept reported check output when it proves the exact final artifact or configuration; rerun only when evidence is missing, unbound or invalidated by a later change. If the SHA, scope or pertinent environment changed, the proof is dead and must be rerun.
4. Close the dispatch: it ends when the child's work is IN your tree and nothing of the child's is left outside it. Integrate and clean in the same pass. The child ran under your identity, so its scratch, branch and tree are yours to dispose of, with the cleanup tooling you use for your own work (the repository's declared tooling, else plain git), and only what the child created; a child that needed a tree of its own is a defect to report, not a tree to keep.

## Do not
- Use another runtime's spawn surface as if it were Kimi's
- Give a child an identity of its own

## Validation
- Spawn used Kimi's own child surface and this home's agent files
- Every child acted only within its brief, as you; none was given an identity of its own
