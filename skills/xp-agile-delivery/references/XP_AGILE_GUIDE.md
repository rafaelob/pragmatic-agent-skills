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

## DORA metrics (delivery performance)

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| Deployment frequency | On-demand (multiple/day) | Daily to weekly | Weekly to monthly | Monthly+ |
| Lead time for changes | < 1 hour | 1 day to 1 week | 1 week to 1 month | 1-6 months |
| Change failure rate | < 5% | 5-10% | 10-15% | > 15% |
| Mean time to recovery | < 1 hour | < 1 day | < 1 week | > 1 week |

### Improving DORA metrics
- **Deployment frequency**: automate deployments, reduce batch size, use feature flags.
- **Lead time**: reduce code review latency, automate testing, simplify deployment.
- **Change failure rate**: improve testing, use canary deployments, shift-left quality.
- **MTTR**: improve observability, automate rollback, practice incident response.

> **2025 update**: DORA's 2025 research (report renamed "State of AI-assisted Software Development", from "Accelerate State of DevOps") evolved the classic four into **five** metrics by adding **deployment rework rate** (share of deployments that are unplanned rework), and renamed MTTR to **failed deployment recovery time**. The four classic metrics above remain the valid baseline. See https://dora.dev/guides/dora-metrics/.

## Kanban flow optimization

### WIP limits
- Set WIP limits per column (e.g., "In Progress: 3" for a team of 5).
- When a column hits its limit: help finish existing work before starting new work.
- Reducing WIP typically improves throughput (counter-intuitive but well-established).

### Flow metrics
- **Cycle time** = work completed date - work started date.
- **Lead time** = work completed date - work requested date.
- **Throughput** = items completed per time period.
- Track with a cumulative flow diagram: visualizes WIP, bottlenecks, and throughput.

### Bottleneck resolution
1. Identify the column with the most items waiting.
2. Investigate: is it a capacity issue, a dependency, or a process problem?
3. Address root cause: add capacity, remove dependency, simplify process.
4. Measure improvement: did cycle time decrease?

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

The governing repository's Definition of Done is normative. This reference explains XP practices; it establishes neither a completion checklist nor a separate completion route. Ceremony formats and metric examples above are background, not additional delivery requirements.
