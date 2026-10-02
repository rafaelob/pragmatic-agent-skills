# Design It Twice

When the user wants to explore alternative interfaces for a chosen deepening candidate, use this parallel sub-agent pattern. Based on "Design It Twice" (Ousterhout) — the first interface idea is rarely the best.

Assumes the codebase-design vocabulary — **module**, **interface**, **seam**, **adapter**, **leverage** — and the 4 dependency categories (in-process, local-substitutable, remote-but-owned, true-external) described in the skill body.

## Process

### 1. Frame the Problem Space

Before spawning sub-agents, write a user-facing explanation of the problem space for the chosen candidate:

- The constraints any new interface must satisfy.
- The dependencies it relies on and which dependency category they fall into.
- A rough illustrative code sketch to make constraints concrete — not a proposal, just grounding.

Show this to the user, then immediately proceed to Step 2. The user reads while the sub-agents work in parallel.

### 2. Spawn Sub-agents

Spawn at least two sub-agents in parallel, one per genuinely different design pressure worth comparing for this seam; add a third or fourth only when another candidate constraint actually applies here, never to hit a headcount. Each must produce a **radically different** interface for the deepened module. Use this runtime's own spawn path — never a Cursor-only Agent tool.

Give each agent a distinct design constraint, drawn from whichever of these apply:

- **Minimize:** "Minimize the interface — aim for 1–3 entry points max. Maximize leverage per entry point."
- **Maximize flexibility:** "Maximize flexibility — support many use cases and extension points."
- **Optimize for common case:** "Optimize for the most common caller — make the default case trivial."
- **Ports & Adapters (if applicable):** "Design around ports & adapters for cross-seam dependencies."

Each agent's brief must include: file paths, coupling details, dependency category (in-process / local-substitutable / remote-but-owned / true-external), and what sits behind the seam. Use consistent codebase-design vocabulary (module, interface, seam, adapter, leverage) in every brief — and include the project's domain glossary so every sub-agent names the domain the same way too, not just the architecture. Take the terms from wherever the project keeps that glossary (a glossary or context file, a domain doc) rather than guessing a path. If the project has no glossary, say so explicitly in the brief, so the agents converge on the code's existing vocabulary instead of each coining its own.

Each sub-agent outputs:

1. Interface (types, methods, params — plus invariants, ordering, error modes).
2. Usage example showing how callers use it.
3. What the implementation hides behind the seam.
4. Dependency strategy and adapters.
5. Trade-offs — where leverage is high, where it is thin.

### 3. Present and Compare

Present designs sequentially so the user can absorb each one, then compare them in prose. Contrast by:

- **Depth** — leverage at the interface.
- **Locality** — where change concentrates.
- **Seam placement** — where the interface lives and what it hides.

After comparing, give your own **opinionated recommendation**: which design is strongest and why. If elements from different designs combine well, propose a hybrid. Be decisive — the user wants a strong read, not a menu.
