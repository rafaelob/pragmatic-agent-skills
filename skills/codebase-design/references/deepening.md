# Deepening

How to deepen a cluster of shallow modules safely, given their dependencies. Assumes the codebase-design vocabulary — **module**, **interface**, **seam**, **adapter**.

## Dependency Categories

When assessing a candidate for deepening, classify its dependencies. The category determines how the deepened module is tested across its seam.

### 1. In-process

Pure computation, in-memory state, no I/O. Always deepenable — merge the modules and test through the new interface directly. No adapter needed.

### 2. Local-substitutable

Dependencies you can run locally in the test suite: a disposable instance of the production database engine, an in-memory filesystem. Deepenable if one exists. The seam is internal; no port at the module's external interface. A claim about persistence, locking, migrations or query behaviour needs the real engine: SQLite or PGLite standing in for Postgres does not prove it.

### 3. Remote but Owned (Ports & Adapters)

Your own services across a network boundary (microservices, internal APIs). Define a **port** (interface) at the seam. The deep module owns the logic; the transport is injected as an **adapter**. Tests use an in-memory adapter. Production uses an HTTP/gRPC/queue adapter.

Recommendation shape: _"Define a port at the seam, implement an HTTP adapter for production and an in-memory adapter for testing, so the logic sits in one deep module even though it is deployed across a network."_

### 4. True External (Mock)

Third-party services (Stripe, Twilio, SendGrid, etc.) you do not control. The deepened module takes the external dependency as an injected port; tests provide a mock adapter.

## Seam Discipline

**Justify the seam before introducing a port.** Use the criteria under "Two adapters are evidence of a real seam, not a requirement for one" in `SKILL.md`: a second adapter is one sufficient reason, and independent volatility, an external contract or a security boundary are the others. A seam for a variation that might appear someday is indirection without leverage.

**Internal seams vs external seams.** A deep module can have internal seams (private to its implementation, used by its own unit tests) as well as the external seam at its interface. Do not expose internal seams through the external interface just because tests use them.

## Testing Strategy: Replace, Don't Layer

- Delete an old unit test on a shallow module only when you can name the test at the deepened module's interface that now proves its behavior. With no surviving proof, keep it or port the behavior first.
- Write new tests at the deepened module's interface. The **interface is the test surface**.
- Tests assert on observable outcomes through the interface, not on internal state.
- Tests should survive internal refactors. If a test must change when the implementation changes, it is testing past the interface — fix the seam placement, not the test.
