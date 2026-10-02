---
name: codebase-design
description: "Use when designing or improving a module's interface (deep modules, small interfaces, clean seams) or finding and assessing shallow modules worth deleting, inlining or deepening. Moves -> refactoring-catalog."
license: MIT
metadata:
  tags:
  - domain-expertise
  - codebase-design
  - deep-modules
  - ousterhout
  - module-design
  - seam
  - testability
  - interface-design
  version: 1.4.2
  author: coding-agent
  category: domain-expertise
  subcategory: frameworks
  vendor: universal
  lifecycle: active
  coding_agent: true
  audience: developer
  output_format: markdown
  modality: text
  freshness: 2026-08
  upstream: https://github.com/mattpocock/skills
  upstream_mode: adapted
  upstream_baseline_commit: 5b15a47f2d7150f545fbcacbfe381787fc0230dc
  upstream_baseline_date: 2026-08-21
  upstream_author: Matt Pocock
  upstream_path: skills/engineering/codebase-design/SKILL.md
  adaptation_summary: 'Harness-neutral subagent dispatch (14bfbbd). Glossary
    location is left to local conventions. House Design Workflow and Checklist kept.'
  upstream_not_adopted:
    em-dash-sweep: Cosmetic 3216582; house keeps existing punctuation.
    Agent-tool: Cursor Task API; this catalog dispatches via the runtime in use.
---

# Codebase Design — Deep Modules

Design **deep modules**: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface. Use this vocabulary and these principles wherever code is being designed or restructured. The aim is leverage for callers, locality for maintainers, and testability for everyone.

## Glossary

Use these terms for the concepts below; they disambiguate "component," "service," "API," or "boundary" when those words are being used loosely for different things in the same discussion.

| Term | Definition | Avoid |
|---|---|---|
| **Module** | Anything with an interface and an implementation. Scale-agnostic: a function, class, package, or tier-spanning slice. | unit, component, service |
| **Interface** | Everything a caller must know to use the module correctly: type signature, invariants, ordering constraints, error modes, required configuration, performance characteristics. | API, signature (too narrow) |
| **Implementation** | What is inside a module. Distinct from **Adapter**: a Postgres repo is a small adapter with large implementation; an in-memory fake is a large adapter with small implementation. | — |
| **Depth** | Leverage at the interface: the amount of behaviour a caller or test can exercise per unit of interface they must learn. A module is **deep** when large behaviour sits behind a small interface; **shallow** when the interface is nearly as complex as the implementation. | impl-lines / interface-lines ratio |
| **Seam** | A place where behaviour can be altered without editing at that place (Feathers). The _location_ at which a module's interface lives. Where to put the seam is its own design decision. | boundary (overloaded with DDD bounded context) |
| **Adapter** | A concrete thing that satisfies an interface at a seam. Describes _role_, not substance. | — |
| **Leverage** | What callers get from depth: more capability per unit of interface learned. One implementation pays back across N call sites and M tests. | — |
| **Locality** | What maintainers get from depth: change, bugs, knowledge, and verification concentrate in one place. Fix once, fixed everywhere. | — |

## Deep vs Shallow

```
Deep module             Shallow module (avoid)
┌──────────────────┐    ┌──────────────────────────────┐
│  Small Interface │    │       Large Interface         │
├──────────────────┤    ├──────────────────────────────┤
│                  │    │   Thin Implementation         │
│ Deep Impl.       │    │   (mostly pass-through)       │
│                  │    └──────────────────────────────┘
└──────────────────┘
```

When designing an interface, ask:
- Can I reduce the number of methods?
- Can I simplify the parameters?
- Can I hide more complexity inside?

## Core Principles

**Depth is a property of the interface, not the implementation.** A deep module can be internally composed of many small, swappable parts — they just are not part of the external interface. A module can have **internal seams** (private to its implementation) as well as the **external seam** at its interface.

**The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through and is earning nothing. If complexity reappears across N callers, it was earning its keep.

**The interface is the test surface.** Callers and tests cross the same seam. If you want to test _past_ the interface, the module is probably the wrong shape.

**Two adapters are evidence of a real seam, not a requirement for one.** A second adapter (typically production + test stand-in) proves something varies across the boundary, which is why it is the easiest justification to check. But it is one sufficient reason, not the only one. A seam is also justified by:

- **independent volatility** — the two sides change for different reasons, on different cadences;
- **an external contract** — the boundary is where a protocol, schema, or published API is honoured;
- **a security boundary** — trust, authorization, or tenancy changes across it, and collapsing it would erase the place the check belongs.

What is *not* a justification is a seam added because a second implementation might appear someday. Absent one of the reasons above, the seam is speculative — the cost is real now and the variation is hypothetical.

## Relationships

- A **Module** has exactly one **Interface** — the surface it presents to callers and tests.
- **Depth** is a property of a **Module**, measured against its **Interface**.
- A **Seam** is where a **Module**'s **Interface** lives.
- An **Adapter** sits at a **Seam** and satisfies the **Interface**.
- **Depth** produces **Leverage** for callers and **Locality** for maintainers.

## Designing for Testability

Good interfaces make testing natural without special arrangements:

1. **Accept dependencies, do not create them.**
   ```typescript
   // Testable — inject the gateway
   function processOrder(order, paymentGateway) {}

   // Hard to test — hardwired dependency
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **Return results, do not produce side effects invisibly.**
   ```typescript
   // Testable — observable return value
   function calculateDiscount(cart): Discount {}

   // Hard to test — side effect on shared state
   function applyDiscount(cart): void { cart.total -= discount; }
   ```

3. **Small surface area.** Fewer methods = fewer tests needed. Fewer parameters = simpler test setup.

## Design Workflow

When applying this skill to a module or cluster:

1. **Name it.** Agree on module, interface, seam, and adapter — use the glossary terms above, not local synonyms.
2. **Measure depth.** Apply the deletion test: if complexity vanishes on deletion, the module is shallow. Count how much a caller must know vs how much behaviour they get.
3. **Classify dependencies.** Use the 4 categories in `references/deepening.md` (in-process / local-substitutable / remote-but-owned / true-external) to decide the testing approach.
4. **Find the seam.** Decide where the interface lives — this is independent of what goes behind it. Justify it with evidence: a second adapter, independent volatility, an external contract, or a security boundary. A seam with none of those is speculative.
5. **Explore alternatives — the exception, not the default.** Design it once and move on; reach for `references/design-it-twice.md`'s parallel sub-agent pattern only for a genuinely high-stakes, hard-to-reverse seam where the right interface is still uncertain after step 4. When it applies: compare candidates on depth/locality/seam, pick the strongest or propose a hybrid, using the specialist subagent the runtime lists by task type (generic/default only when none fits).
6. **Validate.** Apply the interface-as-test-surface check: tests cross the same seam as callers. If tests need to reach past the interface, the module shape is wrong.

## Checking for Shallow Modules

When asked to find or assess shallow modules, examine concrete candidates and apply the deletion test to each. A single caller, a single adapter or a thin wrapper is a lead, never proof: name what the boundary protects (volatility, contract, security, testability) and where its complexity would land without it. A caller count from `rg` misses dynamic dispatch, registrations, configuration and external consumers. For each candidate say delete, inline, deepen or keep, with that reason; change code only when asked, and delete through kill-slop's proof rules. A repo-wide ranked report of deepening opportunities is a larger exercise than this check: run it as its own piece of work, interviewing the owner on each candidate before changing anything.

## Design Checklist

- [ ] Every module has an agreed name using vocabulary from the glossary.
- [ ] Depth is measured as leverage (behaviour per interface unit), not code-line ratio.
- [ ] The deletion test has been applied: deletion reveals complexity redistribution, not nothing.
- [ ] Each seam is justified by evidence from step 4 (a second adapter, independent volatility, an external contract or a security boundary) -- not added on the chance a second implementation might appear.
- [ ] Dependencies are classified by category; testing strategy matches the category.
- [ ] Tests assert on observable outcomes through the interface, not on internal state.

## Rejected Framings

- **Depth as implementation-lines / interface-lines ratio** (Ousterhout original): rewards padding the implementation with dead code. Use depth-as-leverage instead.
- **"Interface" = TypeScript `interface` keyword or public methods**: too narrow. Interface here includes every fact a caller must know, including invariants and error modes.
- **"Boundary"**: overloaded with DDD's bounded context. Say **seam** or **interface**.

## Reference Files

- Read `references/deepening.md` to deepen a cluster of shallow modules: 4 dependency categories, seam discipline, replace-don't-layer testing strategy.
- Read `references/design-it-twice.md` only for the rare high-stakes, hard-to-reverse seam that stays uncertain after step 4, never as the default design path: parallel sub-agent pattern sized to the genuinely distinct candidates worth comparing, compare on depth/locality/seam, give an opinionated recommendation.

## Attribution

Adapted from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT). Original skill: `codebase-design`.
