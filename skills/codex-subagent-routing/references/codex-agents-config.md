# Codex `[agents]` config, `/agent`, and custom agent files

Fetched 2026-09-15 from the live OpenAI pages (not from memory). Model
identifiers on those pages perish; this note names keys and paths only.

- Subagents: https://developers.openai.com/codex/subagents
- Config sample: https://developers.openai.com/codex/config-sample
- Config reference: https://developers.openai.com/codex/config-reference
- CLI slash commands: https://developers.openai.com/codex/cli/slash-commands

The spawn contract and the depth rule are measured on the installed CLI; the
official pages do not publish every argument. Re-read the live `spawn_agent`
schema before treating a remembered argument as real.

## `[agents]` in `config.toml`

Global subagent settings live under `[agents]`. Keys on the pages above
today:

| Key | What the page says |
|---|---|
| `agents.enabled` | Enable or disable multi-agent tools (default true). |
| `agents.max_concurrent_threads_per_session` | Cap concurrently open **spawned** threads, **excluding the primary**. Unset → Codex chooses the default. `agents.max_threads` is a legacy alias. |
| `agents.default_subagent_model` | Default model for spawned agents. An explicit spawn value wins. |
| `agents.default_subagent_reasoning_effort` | Default reasoning effort for spawned agents. An explicit spawn value wins. |
| `agents.interrupt_message` | Record a model-visible message when a turn is interrupted (default true). |

Do not copy a number or a model id from this table into a dispatch. Read
the live config and the live schema.

**Cap wording differs between sources.** The official key excludes the
primary thread; how the installed CLI actually counts is a local measurement
the official pages do not publish. Read the key and its unit live before
sizing a dispatch; this page is the config-file vocabulary only.

## `/agent`

On the CLI surface, `/agent` (also documented as `/subagents`) inspects
and switches between agent threads while they run. It is a thread
switcher, not a spawn API. `/fork` on the same slash-commands page forks
the current **chat**, which is a different verb.

## Custom agent TOML

Official custom agents are standalone TOML files:

- personal: `~/.codex/agents/`
- project: `.codex/agents/`

Each file is one agent. Required fields on 2026-09-15: `name`,
`description`, `developer_instructions`. Optional session keys (model,
effort, sandbox, MCP, skills) may appear; omitted keys inherit from the
parent. The `name` field is the identity, not the filename. A custom
file whose `name` matches one of the runtime's built-in agents wins over
the built-in; the built-ins are whatever the live schema lists.

The **role cards** this skill routes by are the custom-agent TOML files of
the active Codex home: `agents/*.toml` under that home. With the default
home this is the same directory as the personal root above
(`~/.codex/agents/`); with a relocated or per-install home (for example
`CODEX_HOME` pointing elsewhere) it is that home's own `agents/`. Read the
cards from where the running install keeps them, do not invent another root,
and do not treat OpenCode's skill search path as a Codex agent directory.
Official source for the roots: https://learn.chatgpt.com/docs/agent-configuration/subagents,
read 2026-10-02.

## What stays out of this note

`spawn_agent` is named on the config-reference page as a
`features.multi_agent` tool, without a published argument schema.
`fork_turns` was not on the official pages fetched 2026-09-15. Both
remain local measurements until the docs publish them.
