# Pragmatic agent skills

A curated collection of coding-agent workflows in the open [Agent Skills format](https://agentskills.io/home).
Each folder under `skills/` contains a `SKILL.md` and any supporting resources.

## Getting started

Read [Getting started](GETTING_STARTED.md) for installation guidance, task examples and revision
tracking. Choose the skills relevant to your work and install each complete folder, including
its supporting files and license notices.

The workflows cover diagnosis, implementation, review, testing and engineering decisions.
Runtime-specific orchestration skills require the named agent runtime and its subagent tools;
installing a skill does not provide those tools or grant permission to use them.

## Skills

- [`claude-code-orchestrator`](skills/claude-code-orchestrator/SKILL.md): Use when delegating on Claude Code: select a subagent role, brief the task, and start, stop, resume or reconcile a child. Not for peer sessions or other CLIs. Slicing -> xp-agile-delivery.
- [`code-review`](skills/code-review/SKILL.md): Use when asked to review a diff, PR or uncommitted change for correctness and regressions. Not OWASP/authz -> security-review. Not deleting extras -> kill-slop.
- [`codebase-design`](skills/codebase-design/SKILL.md): Use when designing a module's interface (deep modules, small interfaces, seams) or judging whether a shallow module should be deleted, inlined or deepened. Removal with proof -> kill-slop. Moves -> refactoring-catalog.
- [`codex-subagent-routing`](skills/codex-subagent-routing/SKILL.md): Use when delegating on Codex: select an eligible role, brief it as the mission (goal, scope, constraints, acceptance, delivery) and reconcile the delivery. Not for peer sessions or other CLIs.
- [`diagnosing-bugs`](skills/diagnosing-bugs/SKILL.md): Use to reproduce a bug from evidence, or a failing test whose code may be wrong, and isolate one cause before changing code. Not proving a seam is wired -> layered-testing-executor.
- [`docker-compose`](skills/docker-compose/SKILL.md): Use when a change must run against the repo's own Compose project (service won't start, ports, volumes). Reuse `docker compose -p <project>`. Test selection -> layered-testing-executor.
- [`exhaustive-repo-cleanup-audit`](skills/exhaustive-repo-cleanup-audit/SKILL.md): Use when asked to audit or clean up a repository, or identify files safe to delete. Audit every file; delete proven junk only when removal is requested. Dead code -> kill-slop.
- [`gemini-cli-orchestrator`](skills/gemini-cli-orchestrator/SKILL.md): Use when delegating on Antigravity (Gemini family): read the dispatch schema, pick the child by task and complexity, brief it as the mission, verify returned work. Not the separate Gemini CLI.
- [`grok-build-orchestrator`](skills/grok-build-orchestrator/SKILL.md): Use when delegating on Grok Build via spawn_subagent: pick the child by task type and complexity from the live schema and brief it as the mission. Not peer sessions or other CLIs.
- [`kill-slop`](skills/kill-slop/SKILL.md): Use to remove unneeded files, dependencies, abstractions or dead code from code or a diff, with proof; keep behavior. Module shape -> codebase-design. Trade-off -> pragmatic-engineering. PR review -> code-review.
- [`kimi-cli-orchestrator`](skills/kimi-cli-orchestrator/SKILL.md): Use when delegating on Kimi Code CLI: pick the child from its native agent files by task type and complexity, brief it as the mission. Not another runtime's orchestrator, a peer session or another CLI.
- [`layered-testing-executor`](skills/layered-testing-executor/SKILL.md): Use when a changed capability is ready to verify: tests to pick and run, seams to prove reachable, genuine zero vs unknown. Narrowest layer first. Not first failing test -> tdd. Not story Done gate -> xp-agile-delivery.
- [`legacy-code-change`](skills/legacy-code-change/SKILL.md): Use to change code that has no trusted tests, whether a fix, a feature or a refactor request: characterize, cut the smallest seam, red then green. Trusted tests, structure only -> refactoring-catalog. New code -> tdd.
- [`pragmatic-engineering`](skills/pragmatic-engineering/SKILL.md): Use when a design trade-off needs a choice: simplest thing, reversibility, tracer bullet, estimate, "is this over-engineered?". Proven removal -> kill-slop. Interfaces -> codebase-design. Slices -> xp-agile-delivery.
- [`refactoring-catalog`](skills/refactoring-catalog/SKILL.md): Use to restructure code without changing behavior (duplication, unclear intent, coupling) when trusted tests cover it: small moves, stay green. Behavior change -> tdd. Untested code -> legacy-code-change.
- [`security-review`](skills/security-review/SKILL.md): Use for a structured security review: threat modelling, OWASP checks and severity-ranked findings. Not an ordinary correctness pass -> code-review.
- [`tdd`](skills/tdd/SKILL.md): Use when about to write code and its tests for a feature or bugfix and no failing test exists yet: routine test authoring, red-green-refactor. Pruning existing tests -> test-audit. Layers -> layered-testing-executor.
- [`test-audit`](skills/test-audit/SKILL.md): Use when a test's value is in doubt or to audit and prune low-value, implementation-coupled or duplicate tests already in the suite. Writing a new test -> tdd. Layer choice -> layered-testing-executor.
- [`testing-e2e-playwright`](skills/testing-e2e-playwright/SKILL.md): Use when writing, fixing or de-flaking a Playwright/e2e browser test: fixtures, locators, waits, user-visible assertions. Not the pre-delivery UI pass.
- [`windows-shell-interop`](skills/windows-shell-interop/SKILL.md): Use for UnicodeEncodeError, console mojibake (cp1252), PowerShell 5.1 vs 7, or a path/quoting trap across PowerShell, Git Bash, cmd and Windows paths. Not a Linux-only script. Compose volumes -> docker-compose.
- [`worktree-lifecycle`](skills/worktree-lifecycle/SKILL.md): Use when a second concurrent writer needs an isolated tree, or a git worktree needs census, ownership check or disposal. One owner per tree. Not merge conflicts. Whole-repo cleanup is out of scope.
- [`xp-agile-delivery`](skills/xp-agile-delivery/SKILL.md): Use when a story moves from ready to in-progress, or a mission needs slicing. Larger missions: blocked sub-issues in the tracker. Not test layers -> layered-testing-executor. Trade-off doubt -> pragmatic-engineering.

## License

The repository is licensed under Apache-2.0 (see `LICENSE`). Each skill declares its own license
in its `SKILL.md` frontmatter.

## Credits

Skills adapted from other projects ship our Apache-2.0 license for our modifications
(`skills/<name>/LICENSE`) plus the original license (`skills/<name>/LICENSE-<owner>-<repo>.txt`),
and `NOTICE` credits the authors and the ideas we borrowed.

## Contributing

See [Contributing](CONTRIBUTING.md) for bug reports, focused improvements and contributor credits.
Changes to generated content must be applied to its source before the next export.

## Generated files

`skills/`, `README.md`, `NOTICE` and `export-manifest.json` are generated: the manifest records the
source commit and a SHA-256 for every exported file, and the next export overwrites hand edits.
