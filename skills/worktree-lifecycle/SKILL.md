---
name: worktree-lifecycle
description: "Use when a second concurrent writer needs an isolated tree, or a git worktree needs census, ownership check or disposal. One owner per tree. Not merge conflicts. Whole-repo cleanup -> exhaustive-repo-cleanup-audit."
license: MIT
compatibility: Any coding agent on a git repository. Uses the worktree and cleanup tooling the
  repository declares (AGENTS.md or README); without any, plain git.
metadata:
  author: coding-agent
  version: 1.3.2
  category: ci-cd
  subcategory: build-pipelines
  vendor: universal
  lifecycle: active
  coding_agent: true
  audience: developer
  output_format: markdown
  modality: text
  short-description: Census, ownership, merge order and disposal of worktrees on a shared tree
  freshness: 2026-09
  tags:
  - git
  - worktree
  - multi-agent
  - shared-tree
  - resource-balancing
---

# Isolate only the work that needs it

Read the project's concurrency policy (its AGENTS.md or README) and run `git worktree list` before creating a tree. Use the harness's native isolation and the worktree tooling the repository declares; with none, plain `git worktree`. A second persistent writer may need a separate tree; do not generalize one project's rule to every harness or native child session.

Confirm owner, branch, base and intended write scope. A directory without a current owner is not disposable. Preserve unknown ownership and pending staged/unstaged work. Do not edit trunk and a slice concurrently as if they were the same workspace.

## Integrate with appropriate evidence
Run fast affected checks within the working slice, then commit through the project's declared commit path (plain `git commit` of explicit paths if none). A merge that changes relevant behavior can invalidate local results; an unrelated new read does not. Do not repeat a check that the same approved evidence already covers.

Do not create a worktree, dependency environment and service stack per micro-task. Do not build a new lifecycle daemon or lock registry. If git or native tooling refuses, investigate the specific owner/state conflict rather than bypassing it.

After integration or explicit abandonment, remove only resources whose ownership and preservation are established: commit what is yours, `git worktree remove <path>` without `--force`, then `git branch -d <branch>`. Age or absence of a visible process is not deletion authority. Stop after the requested lifecycle transition is complete and its readback is confirmed, not after a cleanup sweep across the machine.

## Hard rules
- Never remove, move or reset a tree another writer owns, or whose owner you cannot establish.
- Never force: no `worktree remove --force`, `branch -D`, `reset --hard`, `clean -fd`, `checkout -- <path>`, `restore` or `stash` on a shared tree. Git refuses an unmerged branch or a dirty tree on purpose.
- Never discard uncommitted work; commit or preserve it first.
- With no supported tool for a leftover, delete it file by file, naming each path. If a guard refuses a command, do not bypass it (env var, flag, wrapper): use the supported path, or ask the user for explicit approval of that exact deletion. Approval never lifts a guard, and never hand a refused command to the user to paste and run.

When the integration itself conflicts, use a merge-conflict skill if one is installed.

## Price the tree before you open it
A linked worktree shares the object store and costs the checkout alone. A CLONE costs the checkout plus a full copy of `.git` — and a runtime's `isolation` flag may write a clone while calling it a worktree, so read what it produced rather than what it is named. Measure `.git`, multiply by the number of trees you are about to open, and compare against free disk: five children on a repository with a 13 GB `.git` wrote 81 GB of standalone clones and took the disk from 20 GB free to 1.9 GB (measured 2026-09-18). When the product does not fit, serialize the writes in one tree instead — do not open them and plan to clean up after, because a full disk fails writes silently, including the commit that would have preserved the work.

## When a second tree is justified at all
Never open one for a task that merely feels big. Close it the ordinary way: commit, remove unforced, delete the merged branch. A repository's census or reaping tool is for the tree that will NOT come out clean, not the first thing to reach for.
