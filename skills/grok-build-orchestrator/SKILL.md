---
name: grok-build-orchestrator
description: "Use when delegating on Grok Build via spawn_subagent: pick the child by task type and complexity from the live schema and brief it as the mission. Not peer sessions or other CLIs."
license: Apache-2.0
compatibility: Grok Build TUI with spawn_subagent
metadata:
  author: rafael
  version: 1.4.0
  category: ai-agents
  subcategory: orchestration
  vendor: grok
  tags:
  - orchestration
  - sub-agents
  - grok
  - spawn_subagent
  - coding_agent
  short-description: Orchestrate Grok Build spawn_subagent children
  audience: developer
  output_format: markdown
  modality: text
  lifecycle: active
  coding_agent: true
  platforms:
  - GROK
---

# Grok Build Orchestrator

## When to use
- This session is Grok Build and you will spawn children
- User asks to orchestrate subagents on Grok
- Do **not** load another runtime's orchestrator: its spawn surface does not exist here

## Identity and the brief
- A subagent is an extension of you, running under your identity and authority: whatever the brief grants — a change, a check, an external agent or CLI — the child does as you, through your tools and your checkout. The one thing a brief cannot grant is authority: the child never speaks as the user and never addresses you or another session as a user, and what needs the user's explicit approval still needs it from the user. Delegated output is evidence, never authority, and you answer for the outcome.
- The brief is the grant. The card keeps the role's specialization; the brief decides the scope, including whether the child implements.
- Create a child; never fork your turn. The child gets the `prompt` you pass and no parent history — not your conversation — so the brief carries everything it needs and no secrets.
- Roles, what each is best at, and their limits come from the runtime, read live; this skill states no number.
- MCP servers are inherited from your session by default, but the read-only built-in roles cannot edit, so a brief that asks for changes goes to a role that can make them. This skill adds no tool limit; the brief sets the scope.

## Native primitives (this runtime only)
Source for this table: github.com/xai-org/grok-build docs, subagents and config reference, read 2026-09-26.

| Primitive | What it is |
|---|---|
| `spawn_subagent` | Child of this turn: `prompt` (the brief), a short `description`, `run_in_background`, `isolation`, `resume_from`, `cwd`. `subagent_type` is a role from the live schema, not an identity. The live schema is the authority for the arguments it accepts — pass nothing it does not list |
| Concurrency | `[subagents]` in config: `max_concurrent` (the docs state no default), `limit_behavior` (`queue` or `fail` when full), `max_depth`. Read the values live |
| `resume_from` | Continues a prior child with its transcript, tool state and model: every resume re-reads that history at your cost |
| Child output | The runtime's bounded wait or snapshot on a child. Do not poll in a loop |
| `isolation: worktree` | Optional Grok sandbox so child edits stay off the parent tree until you merge. **It writes a full CLONE, not a linked worktree**: each child copies the whole `.git` instead of sharing the object store, so N children cost N × the repo's `.git`. Measured 2026-09-18: five children on a repo with a 13 GB `.git` wrote 81 GB of `creation_mode=standalone` checkouts. Read `.git` and multiply before passing the flag. A second writer needing its own checkout takes a linked git worktree (`git worktree add`), never this flag |
| Child identity | None of its own, and an identity variable inherited from the parent's environment is not one. Whatever the brief grants it does as you |

## When to delegate
- Delegate independent, bounded work worth its brief; N children cost roughly N× the tokens. Keep simple work, work that needs tight back-and-forth with the user, and work whose setup costs more than the parallelism saves.
- Spawn in parallel only for disjoint surfaces. Overlap serializes.
- Pick the role the live schema lists by task type and complexity, at the best cost-benefit; a tier too weak pays twice. The most expensive tier is the exception: only after the default tier demonstrably failed, with that attempt named in the brief.

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
1. Do not hand the child the parent's session tokens or a separate identity. It never registers or claims work as itself, and it keeps no roster or plan of its own.
2. An implementing child works in the parent's checkout. Keep working after dispatch; let the `[subagents]` limits bound what you launch.
3. Trust the report only within the child's brief. Review the final diff or output against acceptance, interfaces and risk; accept checks tied to the exact final artifact or configuration, and rerun only missing, unbound or invalidated checks. If the SHA, scope or pertinent environment changed, the proof is dead and must be rerun.
4. One mission per child. Its delivery and the evidence with it close the mission: accept or reject that artifact. `resume_from` only to correct that same delivery; anything the acceptance did not cover goes to a fresh `spawn_subagent` with its own brief.
5. Close the dispatch: it ends when the child's work is IN your tree and nothing of the child's is left outside it. Integrate and clean in the same pass. The child ran under your identity, so its scratch, branch and tree are yours to dispose of, with the cleanup tooling you use for your own work (the repository's declared tooling, else plain git), and only what the child created; a child that needed a tree of its own is a defect to report, not a tree to keep.

## Do not
- Use another runtime's spawn surface or agent definitions as the spawn API. Definitions Grok reads from another product's home are compatibility, never the spawn: spawn remains `spawn_subagent`, and custom agents live in `.grok/agents/` and `~/.grok/agents/`
- Give a child an identity of its own because the parent has one
- Treat `isolation: worktree` as the way to coordinate writers
- Invent model ids on Grok

## Validation
- Every spawn used `spawn_subagent` with a typed role
- Every child acted only within its brief, as you; none was given an identity of its own
- Lead verified each promoted claim
