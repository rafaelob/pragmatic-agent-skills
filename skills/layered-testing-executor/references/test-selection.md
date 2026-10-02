# Select the cheapest reliable evidence

Use this reference only for an ambiguous test-selection or suite-maintenance decision. It is not a new classification system to implement.

## Selection examples

| Change | First useful feedback | Broader verification only when justified |
|---|---|---|
| Formatting/comment without executable effect | Existing formatter, diff review, relevant document render | Contract-sensitive text, generated parser input or required gate |
| Internal rename | Type/compile and affected existing behavior | Dynamic name lookup or public API affected |
| Local business rule | Domain/service examples and boundaries | Wiring changed or cross-boundary acceptance |
| Persistence or RLS | Actual database/role integration at the changed invariant | Migration, concurrency or release contract |
| Adapter serialization | Consumer/schema contract and malformed input | Runtime/protocol integration changed |
| Local UI visual fix | Focused render/reflow check | Shared global component or required browser target |
| Save/async flow | Relevant interaction plus responsible effect | Durable state, retries, cancellation or cross-service acceptance |
| Config precedence | Real loader with appropriate overlays | Environment behavior or deployment impact |
| Runtime/dependency update | Build/type plus affected consumers | Broad compatibility or required release matrix |
| Generated or externally owned artifact | Supported readback or native format validator | Testing the implementation belongs to its owner project |

## Evidence reuse

Check what the result actually covered: relevant code including dirty changes, runner version/dependencies, configuration/flags, fixtures/data and any mutable external state. Prefer an existing CI/runner record; do not invent a cache or schema to automate this judgment.

A new session or another skill loading is not a reason to rerun. A changed lockfile, relevant source, configuration, fixture or service state can be. A performance result may depend on workload and host. A security boundary change may invalidate previous negative tests even if the visible UI is unchanged.

## Failures, skips and scope

Investigate a failure locally instead of escalating blindly. Group many tests with one unavailable dependency into one precise gap when the runner summary gives the denominator. Do not misreport deselected, skipped or xfail as passing. A blocked required integration prevents its related completion claim, not every independent safe action.

## Retiring low-value tests

Retiring or pruning tests belongs to `test-audit`. Do not silently disable project-required checks; propose their evidence-backed revision through the existing owner.

A representative example is the optional `assets/evidence-note.md`. Reuse the repository's format instead whenever available.
