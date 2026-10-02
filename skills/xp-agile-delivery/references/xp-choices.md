# XP choices under real constraints

## Values without ritual

The XP values are communication, simplicity, feedback, courage and respect. Keep them as decision guides, not counters or mandatory report headings.

Practical default: clarify the usable result, implement a small slice with test feedback, integrate while the change is understandable and gather the consumer's response. Reuse the established work authority.

## Choices

- **TDD and exploration:** new behavior and repeatable defects normally benefit from a behavioral failing test. A bounded exploratory spike can discover the testable contract. Do not merge unvalidated production behavior under the label “spike”.
- **Pairing:** use one driver and a navigator for a concrete benefit such as unfamiliar code or independent challenge. Native subagents do not automatically provide human-style independence; check their evidence. Do not require two agents for a trivial edit.
- **Collective ownership:** team members may improve shared code under the project rules. That does not mean concurrent unrestricted writes to the same uncommitted files.
- **Small releases:** a complete slice is usable by its actual consumer. A library or API may be that consumer-facing product. Do not invent a UI/database for it. Keep the user's full requested scope visible.
- **Integration:** fast tests run during iteration; the existing required gate verifies the integration candidate. Do not accumulate long-lived disconnected layers, but do not bypass protected branches or authorization to mimic trunk-based development.
- **Sustainable work:** limit simultaneous work and repeated validation when machine capacity, account budgets or human review are the bottleneck. Finishing matters more than creating activity.
- **Urgency:** reduce the batch and optional work. Required authorization, safety and affected acceptance remain. A mock may be valid for a local assertion but never proves a live integration.

The original XP reference also mixes Scrum/Kanban and metrics. Treat these as optional supporting techniques. No DORA category, story points, fixed ceremony duration or generic CI target is installed as a requirement here.

Use `assets/slice-note.md`, a short slice note, only when no existing work item already communicates the slice. Do not create a second tracker.
