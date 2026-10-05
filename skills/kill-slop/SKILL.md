---
name: kill-slop
description: "Use when code or a diff has unneeded files, dependencies, abstractions (factory of factory) or dead code. Strip them; keep the behavior. Not a PR review -> code-review. Not renames or moves -> legacy-code-change."
license: Apache-2.0
compatibility: Python 3.13+ and git. Windows-safe checker is scripts/check_diff.py.
metadata:
  author: coding-agent
  version: "1.5.3"
  category: code-quality
  subcategory: quality-validation
  vendor: universal
  lifecycle: active
  coding_agent: true
  audience: developer
  output_format: markdown
  modality: text
  short-description: Minimal-diff gate against unrequested files, deps, and drive-by refactors
  tags:
  - kill-slop
  - anti-slop
  - minimal-diff
  - code-quality
  freshness: 2026-08
  upstream: https://github.com/iCodeCraft/anti-slop
  upstream_mode: adapted
  upstream_path: skills/kill-slop/SKILL.md
  upstream_baseline_commit: c50856a01bcc2e9332e9a13f730629622855c91c
  upstream_baseline_date: 2026-08-27
  upstream_author: Imran Gadzhiev (iCodeCraft)
  adaptation_summary: >
    Fork of iCodeCraft kill-slop (MIT). House Python checker replaces bash
    check-diff.sh so Windows/pwsh is first-class. Empty/unreadable scans fail
    (unknown ≠ zero). Not merged with a prose-editing pass: this one is code-diff only. Agent-callable.
  upstream_not_adopted:
    bash-checker: Windows agents cannot run check-diff.sh as the default path
    writing-pass-merge: this is code-diff slop, not a prose-editing pass
---

# Kill slop

Force a minimal, merge-ready diff. Prefer the smallest change that fully solves the stated task.

## Hard rules

- NEVER create a file unless the task clearly needs it or a navigability split below applies
- NEVER refactor unrelated code "while you're here"
- NEVER add comments that restate what the code already says
- NEVER expand scope beyond the user's request
- NEVER invent TODOs, stubs, or "for later" scaffolding
- NEVER search or list outside the workspace root unless the user explicitly asks; outside it, read only a file the governing rules name by path
- NEVER invent Clean Architecture / SOLID folder trees unless the repo already uses that layout
- MUST match existing project patterns before inventing new ones
- MUST prefer editing an existing file over adding a new one
- MUST delete dead code you introduce; do not leave unused imports/vars

## Dead-code finders

Run the finders on the diff's files; go repo-wide only on an explicit "remove dead code" request. Delete only code proven dead: no hit from `git grep -n --untracked` (or `rg -F --hidden --no-ignore-vcs -g '!.git'`) across the repo, config, `.github/`, entrypoints and registrations, and the tests stay green after the deletion. A finder nominates; it never authorizes "delete everything flagged."

- Python: `ruff check --select F401,F811,F841,ERA001`, then `vulture <src> --min-confidence 80`; whitelist proven false positives in a file, never inline.
- TypeScript/JavaScript: `knip` (unused files, exports, dependencies); `tsc --noEmit` with `noUnusedLocals`/`noUnusedParameters` when the project enables them. Use the ecosystem's own equivalent elsewhere.
- Run the finder from the project's declared dev dependencies and manager (`uv run`, `npm run`/`pnpm exec`); never a `uvx`/`npx`/`dlx` stand-in — propose adding a missing one.
- Check before deleting: dynamic dispatch/reflection (`getattr`, registries, plugin entry points), CLI/HTTP route registration, pytest fixtures/conftest, `__all__`/public re-exports, framework hooks/templates/serialization/ORM fields, and any installed or vendored payload that a generator or installer owns.
- Delete in small commits, each carrying the finder output plus the tests as evidence.
- Removing a path takes what only it used: its flags, modes, aliases, fallbacks, state, permissions and config. Verify the surviving flow, including what the deleted path assumed about navigation, permissions or persisted data.

## User intent wins

Default to minimal. If the user **explicitly** asks for more structure, obey that request.

Do not override an explicit ask in the name of kill-slop. If the ask is ambiguous, prefer minimal and say what you skipped.

## File shape

**Default:** colocate. Edit the file/folder that already owns this concern.

**Split only when ALL of these hold:**

1. **Pain now** — the file is already hard to navigate (roughly 300–400 lines, or mixed unrelated concerns) **and** your change would make it worse
2. **One unit** — you are extracting a single cohesive piece with a clear name
3. **Local fit** — the new file follows an existing nearby pattern. If there is no pattern, colocate beside the caller

If only (2) is true, do not split.

## Diff against the asked result

Before writing, name the goal (one sentence), the touch list (files the asked result actually needs) and what you will not do. An extra file or a one-use helper is justified by the problem, not by a file count — there is no fixed file budget.

### Checker (diagnostic, no veto)

The bundled checker is optional diagnosis, never a gate. Read `scripts/check_diff.py` for flags. `OVER_BUDGET` is information; it does not forbid finishing. `SKIP` / `EMPTY_SCAN` means the scan failed — report that, do not treat unknown as clean.

```text
python -X utf8 <path-to-this-skill>/scripts/check_diff.py
python -X utf8 <path-to-this-skill>/scripts/check_diff.py --base HEAD
```

## Style

- Prefer boring, readable code over cleverness
- Handle real error paths the task needs; skip speculative ones
- Names should explain intent; if you need a comment, rename instead
- Tests: one per regression you can name, at the layer that owns it; a bug fix gets its nearest failing test first even where nothing was tested. No test that merely mirrors the implementation

## Output

When summarizing, say what you changed and what you deliberately did **not** change.

## Attribution

Adapted from [iCodeCraft/anti-slop](https://github.com/iCodeCraft/anti-slop) (MIT), skill `kill-slop`.
