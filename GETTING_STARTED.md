# Getting started

These are instructions and supporting files for coding agents, packaged in the
[Agent Skills format](https://agentskills.io/home). Choose the skills that fit
your task; you do not need to install the whole collection.

## Get a skill

1. Clone this repository, or download it from GitHub:

   ```sh
   git clone https://github.com/rafaelob/pragmatic-agent-skills.git
   ```

2. Pick a skill from the [catalog](README.md#skills) and read its `SKILL.md`.
3. Follow your agent's documented skill installation process. Install the entire
   `skills/<name>/` folder, including any `references/`, `scripts/`, `assets/`,
   license and notice files. Copying only `SKILL.md` can break relative links and
   omit required supporting material.
4. Confirm that your agent discovers the skill, then ask it to use that skill for
   a concrete task. Discovery paths and invocation syntax depend on the agent.

If your agent has no native skill support but can read local files, explicitly
ask it to read the selected `SKILL.md` and follow its instructions. This is manual
use; it does not enable automatic skill discovery.

## Pick a starting point

| Your task | Start with | Example request |
| --- | --- | --- |
| Explain a failure with an unknown cause | [diagnosing-bugs](skills/diagnosing-bugs/SKILL.md) | "Reproduce this failure and isolate its cause before changing code." |
| Implement a feature or a known fix | [tdd](skills/tdd/SKILL.md) | "Implement this acceptance criterion, starting with the smallest meaningful failing test." |
| Review a change | [code-review](skills/code-review/SKILL.md) | "Review this diff for defects and regressions; include evidence for each finding." |
| Assess whether a design is too complex | [pragmatic-engineering](skills/pragmatic-engineering/SKILL.md) | "Compare these two designs against today's requirements and recommend the simplest adequate option." |
| Verify a finished change | [layered-testing-executor](skills/layered-testing-executor/SKILL.md) | "Identify and run the checks this change needs; report what remains unverified." |

Runtime-specific orchestration skills apply only to the runtime named in their
instructions. A skill describes a workflow; it does not install that runtime,
provide tools or grant permission to act.

## Keep an installation traceable

Record the repository commit you installed (`git rev-parse HEAD` inside this
checkout). When updating, review the diff and replace the complete skill folder
through your agent's installation process. The [export manifest](export-manifest.json)
records the source commit and SHA-256 hashes of the generated files.

For fixes and suggestions, see [Contributing](CONTRIBUTING.md).
