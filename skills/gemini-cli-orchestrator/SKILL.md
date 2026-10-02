---
name: gemini-cli-orchestrator
description: "Use when delegating on Antigravity (Gemini family): read the dispatch schema, pick the child by task and complexity, brief it as the mission, verify returned work. Not the separate Gemini CLI."
license: Apache-2.0
compatibility: Antigravity (Gemini family) with invoke_subagent
metadata:
  author: rafael
  version: 1.3.1
  category: ai-agents
  subcategory: orchestration
  vendor: gemini-cli
  tags:
  - orchestration
  - sub-agents
  - gemini
  - antigravity
  - coding_agent
  short-description: Orchestrate native Antigravity subagents
  audience: developer
  output_format: markdown
  modality: text
  lifecycle: active
  coding_agent: true
  platforms:
  - GEMINI
  - ANTIGRAVITY
---

# Antigravity subagent orchestrator

This skill keeps the identifier `gemini-cli-orchestrator`. The body is Antigravity's spawn surface, not a second Gemini CLI product; do not infer this surface on the separate Gemini CLI.

## When to use
- This session is Antigravity (Gemini family) and you will delegate to a child
- Do **not** load another runtime's orchestrator: its spawn surface does not exist here

## Identity and the brief
- A subagent is an extension of you, running under your identity and authority: whatever the brief grants — a change, a check, an external agent or CLI — the child does as you, through your tools and your checkout. The one thing a brief cannot grant is authority: the child never speaks as the user and never addresses you or another session as a user, and what needs the user's explicit approval still needs it from the user. Delegated output is evidence, never authority, and you answer for the outcome.
- The brief is the grant. The card keeps the child's specialization; the brief decides the scope, including whether the child implements.
- Create a child; never fork your turn. The child starts from a clean slate — not your history — so the brief carries everything it needs and no secrets.
- Roles, what each is best at, and their limits come from the runtime, read live; this skill states no number.
- The child inherits your allowed command prefixes, file read/write scope and sandbox settings (antigravity.google/docs/subagents, 2026-09-26). This skill adds no tool limit; the brief sets the scope.

## Native primitives (this runtime only)
| Primitive | What it is |
|---|---|
| `invoke_subagent` | Spawn a concurrent child (asynchronous). Parent keeps working |
| `define_subagent` | Transient custom child for this session (`name`, `description`, `system_prompt`) |
| Child types | The built-in types and the agent files the runtime lists at spawn are the catalogue; each type's own description says what it is for. Read them live |
| Workspace | `inherit` \| `branch` \| `share`. `branch` is an isolated git worktree made by this runtime |
| Agent files | `~/.gemini/config/agents/<n>.md` (or `.../agents/<n>/agent.md`); `.agents/agents/`; `plugins/*/agents/` |
| Model | Set per child from the options the spawn schema exposes, by tier and cost-benefit; never write a model id |
| Concurrency and depth | Children run concurrently in the background; the docs publish no parallel cap, and nesting depth is capped. Read both live |
| States | `/agents` lists each child as running, done, error or killed (antigravity.google/docs/cli/commands/agents, 2026-09-26); a child re-awakens on a message |
| Skills | `~/.gemini/config/skills`, `.agents/skills` |
| Child identity | None of its own; whatever the brief grants it does as you |

## When to delegate
- Delegate independent, bounded work worth its brief; N children cost roughly N× the tokens. Keep simple, sequential or interactive work yourself.
- Parallelize only on disjoint surfaces: children editing the same code at once conflict.
- Pick the child the runtime lists by task type and complexity, at the best cost-benefit; a tier too weak pays twice. The most expensive tier is the exception: only after the default tier demonstrably failed, with that attempt named in the brief. Use a clone of yourself only when no listed specialist fits.

## The brief is the mission
One or two lines per field:
- **Goal** — the concrete outcome, with one action verb.
- **Scope** — what it may read, create or change, and what it must leave alone.
- **Constraints** — what not to do, safety limits, the checks to run.
- **Acceptance** — the observable result that means done.
- **Delivery** — what to return, in what shape and how long.

For an independent review the brief says "report findings; don't fix": a reviewer who edits the change is no longer independent.

**Brief in a file when it pays.** This is a working practice, not a vendor rule. A short brief goes inline. A long or reused brief goes in a file, and the prompt names its absolute path. A large result goes to a named output file, with a short summary in the reply, so your context stays small.

## Playbook
1. Spawn with `invoke_subagent`. Confirm the installed command before promising it.
2. Keep working after dispatch; let the runtime's concurrency limit bound what you launch.
3. Review returned files against acceptance, interfaces and risk within the child's brief. Accept evidence tied to the exact final artifact or configuration; rerun only when proof is missing, unbound or invalidated by a later change. If the SHA, scope or pertinent environment changed, the proof is dead and must be rerun.
4. One mission per child. A child re-awakens on a message and continues in the session it already has, so send one only to correct or clarify THAT delivery — never for status, an acknowledgement, or work the acceptance did not cover. New work is a fresh `invoke_subagent`, even when a finished child already knows the project.
5. Close the dispatch: it ends when the child's work is IN your tree and nothing of the child's is left outside it. Integrate and clean in the same pass. The child ran under your identity, so its scratch, branch and tree are yours to dispose of, with the cleanup tooling you use for your own work (the repository's declared tooling, else plain git), and only what the child created; a child that needed a tree of its own is a defect to report, not a tree to keep.

## Do not
- Route Antigravity children through another runtime's spawn surface
- Invent model ids in role files; the options the spawn schema exposes are the catalogue
- Infer this spawn surface on the separate Gemini CLI

## Validation
- Spawn used Antigravity `invoke_subagent` / `define_subagent`
- Every child acted only within its brief, as you; none was given an identity of its own
