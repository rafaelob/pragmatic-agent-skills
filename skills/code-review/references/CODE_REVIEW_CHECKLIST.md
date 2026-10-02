<!-- FRESHNESS: Always verify against project-specific linter/formatter configs. Last structured: 2026-03 -->

# Code Review Checklist

## Authoritative sources

- OWASP Code Review Guide: https://owasp.org/www-project-code-review-guide/
- Google Engineering Practices - Code Review: https://google.github.io/eng-practices/review/
- Microsoft Code Review Best Practices: https://learn.microsoft.com/en-us/devops/develop/code-reviews

## Baseline code smells (Fowler) -- optional reference

Optional smell baseline, consulted only when the change at hand suggests one. A documented repo standard always overrides a smell below when it endorses what the smell would flag. Each smell is a judgement call ("possible Feature Envy"), never a hard violation -- report it as an optional preference, not a demonstrated defect, and skip what the configured linter/formatter already enforces.

Source: Martin Fowler, *Refactoring* (2nd ed.), ch. 3; adopted via `mattpocock/skills`' `skills/engineering/code-review/SKILL.md`.

| Smell | What it is | Fix |
|---|---|---|
| Mysterious Name | A function, variable, or type whose name doesn't reveal what it does or holds | Rename it; if no honest name comes, the design is murky |
| Duplicated Code | The same logic shape appears in more than one hunk or file | Extract the shared shape, call it from both |
| Feature Envy | A method that reaches into another object's data more than its own | Move the method onto the data it envies |
| Data Clumps | The same few fields or params keep travelling together | Bundle them into one type, pass that |
| Primitive Obsession | A primitive or string standing in for a domain concept that deserves its own type | Give the concept its own small type |
| Repeated Switches | The same switch/if-cascade on the same type recurs across the change | Replace with polymorphism, or one map both sites share |
| Shotgun Surgery | One logical change forces scattered edits across many files | Gather what changes together into one module |
| Divergent Change | One file or module is edited for several unrelated reasons | Split so each module changes for one reason |
| Speculative Generality | Abstraction, parameters, or hooks added for needs the spec doesn't have | Delete it; inline back until a real need shows |
| Message Chains | Long `a.b().c().d()` navigation the caller shouldn't depend on | Hide the walk behind one method on the first object |
| Middle Man | A class or function that mostly just delegates onward | Cut it, call the real target direct |
| Refused Bequest | A subclass or implementer that ignores or overrides most of what it inherits | Drop the inheritance, use composition |

## Correctness

- [ ] Business logic matches acceptance criteria / ticket requirements
- [ ] All code paths terminate correctly (no infinite loops, no unreachable code)
- [ ] Error handling is explicit: no swallowed exceptions, no bare except/catch-all
- [ ] Null/undefined/empty-collection cases handled at boundaries
- [ ] State mutations are atomic where required (transactions, locks)
- [ ] Backward compatibility preserved for public APIs / shared contracts
- [ ] Data transformations are validated (types, ranges, formats)

## Readability

- [ ] Names reveal intent: variables, functions, classes, modules
- [ ] Functions have single responsibility
- [ ] Comments explain "why" not "what"; no noise comments
- [ ] Complex logic has explanatory comments or is extracted to named functions

## Maintainability

- [ ] Clear module boundaries; no layer violations (UI accessing DB directly)
- [ ] Dependencies injected at edges; no hidden singletons or global state
- [ ] New code follows existing project conventions and patterns
- [ ] No code duplication that warrants extraction (three or more occurrences)
- [ ] Configuration externalized (no hardcoded URLs, ports, credentials)

## Test coverage

- [ ] New behavior has corresponding tests
- [ ] Tests assert meaningful outcomes (not just "no error thrown")
- [ ] Edge cases covered: empty input, boundary values, error paths
- [ ] Existing tests updated if behavior changed (no stale assertions)
- [ ] Mocks used only at external boundaries with explicit contracts

## Security

- [ ] No SQL/NoSQL/command/template injection via unsanitized input
- [ ] Auth checks present on every protected endpoint/resource
- [ ] No IDOR: resource access validated against requesting user
- [ ] Sensitive data not logged, not in error messages, not in client bundles
- [ ] No hardcoded secrets, tokens, or API keys
- [ ] New dependencies checked for known CVEs
- [ ] Cryptographic operations use vetted libraries with adequate parameters

## Performance

- [ ] No N+1 queries; batch/join where possible
- [ ] Database queries use appropriate indexes; no full table scans on large tables
- [ ] Result sets bounded (pagination, LIMIT, stream processing)
- [ ] No blocking I/O in async contexts
- [ ] Caching has TTL and invalidation strategy
- [ ] Hot-path changes profiled or benchmarked if performance-sensitive
