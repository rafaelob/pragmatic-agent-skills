# Contributing

Small, concrete improvements are welcome. For help choosing and using a skill,
start with [Getting started](GETTING_STARTED.md).

## Report a problem or suggest a change

[Open an issue](https://github.com/rafaelob/pragmatic-agent-skills/issues) with:

- The skill name and repository commit you used.
- The task or prompt, with a minimal example and no credentials or private data.
- The expected behavior and what actually happened.
- Your agent/runtime and version when the problem depends on them.
- A proposed correction and its verification, if you have one.

State what you observed separately from what you suspect. A documentation typo
needs only the file, the relevant text and the correction.

## Understand the generated files

As explained in the [README](README.md#generated-files), `skills/`, `README.md`,
`NOTICE` and `export-manifest.json` are generated from a separate source catalog.
The next export replaces direct edits to those files.

An issue or a focused pull request can show a proposed change to generated
content. The maintainer needs to apply an accepted correction to the source and
regenerate the export so it survives future updates. Do not manually update
manifest hashes to make an edited export appear regenerated.

The hand-written guides, including this file and `GETTING_STARTED.md`, can be
changed directly here. Keep pull requests focused on one problem, explain the
resulting behavior, check affected links and include any validation limits.
Preserve existing licenses and upstream credits.

## Contributors

- [Rafael Bittencourt](https://github.com/rafaelob) maintains and curates the collection.
- Codex (OpenAI), an AI assistant, contributed the getting-started and contribution
  guides at the maintainer's request.

See [NOTICE](NOTICE) for upstream authors and ideas credited by the exported
skills. Commit history records individual changes and co-authorship.
