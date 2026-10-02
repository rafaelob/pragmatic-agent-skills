# Pragmatic agent skills

A small, hand-picked set of agent skills in the open Agent Skills format: one folder per skill
under `skills/`, each with a `SKILL.md`.

## Skills

- [`claude-code-orchestrator`](skills/claude-code-orchestrator/SKILL.md): Use when delegating on Claude Code: pick the subagent type, brief the mission, stop/resume/reconcile a child. Also 'delegar', 'rodar em paralelo', 'qual agente uso'. Slicing -> xp-agile-delivery. Not peers or other CLIs.
- [`code-review`](skills/code-review/SKILL.md): Use when asked to review a diff, PR or uncommitted change for correctness, regressions and unneeded complexity. Not OWASP/authz -> security-review. Not deleting extras -> kill-slop.
- [`codebase-design`](skills/codebase-design/SKILL.md): Use when designing or improving a module's interface (deep modules, small interfaces, clean seams) or finding and assessing shallow modules worth deleting, inlining or deepening. Moves -> refactoring-catalog.
- [`codex-subagent-routing`](skills/codex-subagent-routing/SKILL.md): Use when delegating on Codex: select an eligible role, brief it as the mission (goal, scope, constraints, acceptance, delivery) and reconcile the delivery. Not for peer sessions or other CLIs.
- [`diagnosing-bugs`](skills/diagnosing-bugs/SKILL.md): Use to reproduce a bug from evidence, or a failing test whose code may be wrong, and isolate one cause before changing code. Not proving a seam is wired -> layered-testing-executor.
- [`docker-compose`](skills/docker-compose/SKILL.md): Use when a change must run against the repo's own Compose project (service won't start, ports, volumes). Reuse compose -p <project>. Test picks -> layered-testing-executor.
- [`exhaustive-repo-cleanup-audit`](skills/exhaustive-repo-cleanup-audit/SKILL.md): Use when asked to clean up a repo ("limpar o repo", "remove the junk") or what it can delete ("o que dá pra apagar"): audits every file, deletes proven junk only on an action request. Dead code -> kill-slop.
- [`gemini-cli-orchestrator`](skills/gemini-cli-orchestrator/SKILL.md): Use when delegating on Antigravity (Gemini family): read the dispatch schema, pick the child by task and complexity, brief it as the mission, verify returned work. Not the separate Gemini CLI.
- [`grok-build-orchestrator`](skills/grok-build-orchestrator/SKILL.md): Use when delegating on Grok Build via spawn_subagent: pick the child by task type and complexity from the live schema and brief it as the mission. Not peer sessions or other CLIs.
- [`kill-slop`](skills/kill-slop/SKILL.md): Use when code or a diff has unneeded files, dependencies, abstractions (factory of factory) or dead code. Strip them; keep the behavior. Not a PR review -> code-review. Not renames or moves -> legacy-code-change.
- [`kimi-cli-orchestrator`](skills/kimi-cli-orchestrator/SKILL.md): Use when delegating on Kimi Code CLI: pick the child from its native agent files by task type and complexity, brief it as the mission. Not another runtime's orchestrator, a peer session or another CLI.
- [`layered-testing-executor`](skills/layered-testing-executor/SKILL.md): Use when a changed capability is ready to verify: tests to pick and run, seams to prove reachable, genuine zero vs unknown. Narrowest layer first. Not first failing test -> tdd. Not story Done gate -> xp-agile-delivery.
- [`legacy-code-change`](skills/legacy-code-change/SKILL.md): Use when changing code with no trusted tests (characterize, cut the smallest seam, red then green). Trusted tests -> refactoring-catalog. New code -> tdd. Unknown cause -> diagnosing-bugs.
- [`pragmatic-engineering`](skills/pragmatic-engineering/SKILL.md): Use when an engineering trade-off needs a choice: simplest thing, reversibility, tracer bullet or prototype, DRY, broken windows, estimate uncertainty, "is this over-engineered?". Slicing a story -> xp-agile-delivery.
- [`refactoring-catalog`](skills/refactoring-catalog/SKILL.md): Use when code has real duplication, confusing intent or excess coupling and trusted behavioral tests exist. Gives small safe moves (extract, rename, move), green throughout. No trusted tests -> legacy-code-change.
- [`security-review`](skills/security-review/SKILL.md): Use for a structured security review: threat modelling, OWASP checks and severity-ranked findings. Not an ordinary correctness pass -> code-review.
- [`tdd`](skills/tdd/SKILL.md): Use when about to write code for a feature or bugfix and no failing test exists yet. Red-green-refactor. Layers -> layered-testing-executor. Untested -> legacy-code-change; unknown cause -> diagnosing-bugs.
- [`test-audit`](skills/test-audit/SKILL.md): Use when adding/changing a test or auditing/pruning low-value, implementation-coupled or duplicate tests. Not red-green -> tdd. Not layer choice -> layered-testing-executor. Untested code to change -> legacy-code-change.
- [`testing-e2e-playwright`](skills/testing-e2e-playwright/SKILL.md): Use when writing, fixing or de-flaking a Playwright/e2e browser test: fixtures, locators, waits, user-visible assertions. Not the pre-delivery UI pass.
- [`windows-shell-interop`](skills/windows-shell-interop/SKILL.md): Use for UnicodeEncodeError, console mojibake (cp1252), PowerShell 5.1 vs 7, or a path/quoting trap across PowerShell, Git Bash, cmd and Windows paths. Not a Linux-only script. Compose volumes -> docker-compose.
- [`worktree-lifecycle`](skills/worktree-lifecycle/SKILL.md): Use when a second concurrent writer needs an isolated tree, or a git worktree needs census, ownership check or disposal. One owner per tree. Not merge conflicts. Whole-repo cleanup -> exhaustive-repo-cleanup-audit.
- [`xp-agile-delivery`](skills/xp-agile-delivery/SKILL.md): Use when a story moves from ready to in-progress, or a mission needs slicing. Beyond one slice: blocked sub-issues via tdd. Not test layers -> layered-testing-executor. Trade-off doubt -> pragmatic-engineering.

## License

The repository is licensed under Apache-2.0 (see `LICENSE`). Each skill declares its own license
in its `SKILL.md` frontmatter.

## Credits

Skills adapted from other projects keep the original license in their folder
(`skills/<name>/LICENSE*`), and `NOTICE` credits the authors and the ideas we borrowed.

## Generated files

`skills/`, `README.md`, `NOTICE` and `export-manifest.json` are generated: the manifest records the
source commit and a SHA-256 for every exported file, and the next export overwrites hand edits.
