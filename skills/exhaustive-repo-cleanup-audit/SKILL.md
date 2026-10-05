---
name: exhaustive-repo-cleanup-audit
description: "Use when asked to audit or clean up a repository, or identify files safe to delete. Audit every file; delete proven junk only when removal is requested. Dead code -> kill-slop."
license: Apache-2.0
metadata:
  tags:
  - code-quality
  - cleanup
  - repo-hygiene
  - audit
  - coverage-proof
  - dead-code
  - junk-files
  - filesystem-inventory
  - user_level:intermediate
  version: "1.5.1"
  author: coding-agent
  category: code-quality
  subcategory: quality-validation
  vendor: universal
  lifecycle: active
  coding_agent: true
  audience: developer
  output_format: markdown
  modality: text
  freshness: 2026-09
---

# Exhaustive Repo Cleanup Audit

## Scope

Turn a broad cleanup request into a coverage-backed audit. Only an ACTION request ("clean up the repo", "remove the junk") then removes the junk FILES proven safe; anything else — a QUESTION ("what can I delete?"), an audit, a review — gets the report with a "Would remove" column and deletes nothing. Report everything uncertain with the proof still missing. Keep what was mechanically enumerated/read separate from what is semantically safe to remove. Dead CODE is only nominated here; deleting it is `kill-slop`'s job.

### Direction of the wiring proof

This skill proves that NOTHING uses a file, so it can go. `layered-testing-executor` proves that SOMETHING reaches a new surface, so a change can be called delivered. Pick by direction: cleaning an existing tree is here; judging whether a fresh diff is reachable is there. A no-caller finding here is a reason to delete, never evidence that a feature is wired, and a passing seam matrix there says nothing about whether an old file is still needed.

## Workflow

1. Confirm scope, workspace, branch and dirty state. Note every tracked modification you did not make and every linked worktree (`git worktree list`): that is another writer's WIP, never a target.
2. Build two inventories:
   - Git-visible: `git status --short --branch`, tracked files, ignored/untracked summary, recent diffs.
   - Filesystem-visible: hidden folders, dotfolders, ignored files, generated artifacts, caches, symlinks/reparse points, large directories.
3. Do not recurse into reparse points (symlinks/junctions) unless explicitly required; count them separately.
4. If the user asked to "read everything", read every regular file bytewise enough to prove access; record file count, bytes, unreadable count and enumeration errors. Never print secrets or `.env*` contents; count them and report the contents as suppressed. Count and byte-total generated/vendor trees (`node_modules/`, `.venv/`, `dist/`, `build/`, `target/`, `vendor/`, `.git/objects/`, package caches) without reading them bytewise, and state that exclusion in Coverage, unless the user names one as a target.
5. Keep coverage (what was enumerated/read, counts, errors, exclusions, live-worktree caveats) separate from judgment (candidates, wiring evidence, false-positive risk, action).
6. After coverage, run the semantic checks: junk files (below), duplicate or obsolete reference packs, generated caches and stale exports, oversized evidence artifacts, docs links to historical folders, and dead code (below).
7. On an action request remove the proven junk (below); on a question list it as "Would remove". Everything else is a report row, never a delete.
8. If the user explicitly requested parallel subagents, split read-only coverage by non-overlapping surfaces, pick the specialist the runtime lists by task type, and review their evidence locally before relying on it. Removal stays with you.
9. Write the report so another engineer can reproduce every decision.

## Junk files

Git holds no copy of an untracked file: deleting one is permanent.

- Untracked: removable only in the accidental-name class (shell-redirect or typo names like `nul`, `-`, `=1.2`, `'`, `2>&1`, a mangled absolute path `C:Users...`, `$null`) or when this session created it. Everything else untracked — `*.orig`, `*.rej`, `*.bak`, `* - Copy*`, swap files, `PLAN.md`, `notes.txt` — may be a deliberate backup or an in-progress patch: reported, never deleted.
- Tracked: stray dumps, scratch outputs, duplicate or superseded reports, accidental names.

Proof before removing, all four:

1. Tracked: `git grep -n --untracked <name>` (or `rg -F --hidden --no-ignore-vcs -g '!.git' -- <name>`) finds it nowhere, `.github/` included, and nothing finds it by convention: `LICENSE`, `CONTRIBUTING.md`, `CODEOWNERS`, `renovate.json`, `.github/**`, tool configs (`pyproject.toml`, `package.json`, `*.config.*`), folders a docs site globs.
2. It is not a test fixture: nothing under a test data or snapshot folder (`tests/fixtures/`, `testdata/`, `__snapshots__/`).
3. It is outside the protected roots: lockfiles, changelogs, generated or installed files stamped with a managed-file marker, and every path the repository's AGENTS.md or README declares as state, governance or reference material (see Stop Lines Declared by the Repo).
4. It is not another writer's WIP: not in a linked worktree, not a tracked modification you did not make.

Removal:

- Untracked: delete it by name, one literal path at a time, never a glob or a recursive sweep.
- Tracked: `git rm` by literal path, then run the build or check that could reference the file (not the full suite); commit by explicit path through the commit tooling the repository declares (plain `git commit -- <paths>` if none), the message listing each file with its proof.
- No backup, quarantine, `archive/` or `old/` folder: for tracked files git is the archive.
- Anything that misses one proof is reported, never deleted.

## Dead code

Nominate only, with `kill-slop`'s finders and false-positive checks; deleting code is its job.

## Report Shape

```markdown
# Cleanup Audit

## Coverage
- Workspace, branch, date, command/tool path; git-visible and filesystem inventories.
- Regular files read, bytes read, read/enumeration errors; explicit exclusions and why.

## Removed (a question: Would remove)
| Path | Tracked? | Proof (class or git grep, not fixture, not protected, not WIP) | Commit |

## Candidates Needing Proof
| Candidate | Type | Why suspicious | Proof still missing | Risk |

## Stop Lines
- What must not be deleted broadly.

## Next Steps
- Ordered, bounded increments with validation (dead code -> kill-slop).
```

## Guardrails

- Never run or recommend `git clean -xdf`, deleting `.git`, deleting `.env*`, or deleting evidence folders as a broad sweep.
- Never infer "junk" or "dead" from age, size or name alone; require the proofs above.
- A live worktree moves: report count mismatches between passes.
- If validation cannot run, say so and keep the audit open.
- A work-tracking folder or file (`sprints/`, `TODO.md`) is retired only when the repository's own instructions (AGENTS.md, README or contributing doc) explicitly say so; otherwise leave it. When retired: a reported finding in an audit-only request; on an action request, move any live items into the tracker item the project declares, then delete it like any other proven junk once it is empty.

## Stop Lines Declared by the Repo (never removal targets)

Read the repository's AGENTS.md or README for paths it declares as live state, coordination data, governance, reference material or installed/managed payload. Keep them out of every candidate list and name them under Stop Lines. Untracked or gitignored status proves nothing: tooling often ignores live state on purpose, and gitignored never means safe to delete. A file with no importer is not dead code if a managed-file marker or the repo's docs say a tool installed it.

- **Rescue refs and parked worktrees, the path an audit most often mistakes for junk.** Never propose worktree, stash, reflog or gc cleanup; each is another writer's preserved work until its owner or the repo's own docs say otherwise.

## Validation

Before finishing: `git show --stat <removal commit>` lists exactly the tracked removals reported, the build or check that could reference each file ran green on it (not the full suite), and each untracked deletion is reported with its class. A question changed nothing. Check the report has both the coverage and judgment layers, and that no secret material was printed.
