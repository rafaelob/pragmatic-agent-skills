<!-- FRESHNESS: Agile and XP practices evolve. Verify against current industry consensus. Last structured: 2026-04-21 -->

# XP & Agile Practices Guide

## Authoritative sources

- Extreme Programming Explained (Kent Beck, 2nd ed. 2004): https://www.oreilly.com/library/view/extreme-programming-explained/0321278658/ | practices summary: https://martinfowler.com/bliki/ExtremeProgramming.html
- Agile Manifesto: https://agilemanifesto.org/
- Scrum Guide (Nov 2020, still current as of last check 2026-07-28): https://scrumguides.org/scrum-guide.html
- Kanban Guide: https://kanban.university/kanban-guide/ | an alternate source cited 2026-07-28 as "2024 revision", UNVERIFIED against the University guide above: https://kanbanguides.org/
- DORA Metrics (Accelerate): https://dora.dev/
- Four rules of simple design (Kent Beck): https://martinfowler.com/bliki/BeckDesignRules.html
- INVEST criteria (Bill Wake): https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/
- SAFe 6.0: https://scaledagileframework.com/

## XP practices summary

### Primary practices
| Practice | Description | Key benefit |
|----------|------------|-------------|
| TDD | Write test first, then code, then refactor | Drives design, catches regressions |
| Pair programming | Two developers, one keyboard | Knowledge sharing, fewer defects |
| Continuous integration | Integrate to main at least daily | Early conflict detection |
| Simple design | Simplest solution that works | Reduces complexity and waste |
| Refactoring | Improve structure without changing behavior | Maintains codebase health |
| Small releases | Ship frequently in small increments | Fast feedback, lower risk |
| Collective code ownership | Anyone can change any code | No knowledge silos |
| Coding standards | Consistent style across the team | Readability, easier reviews |

### Corollary practices
| Practice | Description | When to adopt |
|----------|------------|---------------|
| Real customer involvement | Customer available for questions | When requirements are fluid |
| Incremental deployment | Deploy small changes frequently | After CI is stable |
| Team continuity | Keep teams together across projects | When velocity matters |
| Root cause analysis | Five Whys for recurring issues | After incidents or defects |

## TDD cycle detail

```
1. RED: Write a test that fails (expresses desired behavior)
   - Test should be specific and named for the behavior
   - Run it: confirm it fails for the right reason

2. GREEN: Write minimum code to pass the test
   - Do not optimize, do not generalize
   - Just make the test pass

3. REFACTOR: Improve the code with tests green
   - Extract methods/classes, rename, simplify
   - Run tests after each refactoring step
   - Stop when the code clearly reveals intent
```

### When NOT to use strict TDD
- Exploratory prototyping (spike): write code first, then add tests before merging.
- UI layout/styling: test behavior, not pixels.
- Generated code: test the generator or the configuration, not the output.

## Delivery metrics and flow

No DORA band or Kanban threshold is installed here. The definitions and current thresholds are perishable: read them at https://dora.dev/ when a concrete number is needed.

## Story splitting quick reference

| Strategy | Example | Best for |
|----------|---------|----------|
| By workflow step | Create -> Edit -> Delete | CRUD features |
| By business rule | Base case -> Edge case -> Error case | Complex logic |
| By data type | Users -> Organizations -> Roles | Multi-entity features |
| By operation | Read (list/view) -> Write (create/update) | New modules |
| By interface | API -> Web UI -> Mobile | Multi-platform |
| By NFR | Functional -> Cached -> Paginated | Performance features |

## Definition of Done

The governing repository's Definition of Done is normative. This reference explains XP practices; it establishes neither a completion checklist nor a separate completion route. Ceremony formats above are background, not additional delivery requirements.
