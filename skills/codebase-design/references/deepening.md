# Deepening

How to deepen a cluster of shallow modules safely, given their dependencies. Assumes the codebase-design vocabulary — **module**, **interface**, **seam**, **adapter**.

## Dependency Categories

When assessing a candidate for deepening, classify its dependencies. The category determines how the deepened module is tested across its seam.

### 1. In-process

Pure computation, in-memory state, no I/O. Always deepenable — merge the modules and test through the new interface directly. No adapter needed.

### 2. Local-substitutable

Dependencies that have local test stand-ins (PGLite for Postgres, in-memory filesystem, SQLite for relational stores). Deepenable if a stand-in exists. The deepened module is tested with the stand-in running in the test suite. The seam is internal; no port at the module's external interface.

### 3. Remote but Owned (Ports & Adapters)

Your own services across a network boundary (microservices, internal APIs). Define a **port** (interface) at the seam. The deep module owns the logic; the transport is injected as an **adapter**. Tests use an in-memory adapter. Production uses an HTTP/gRPC/queue adapter.

Recommendation shape: _"Define a port at the seam, implement an HTTP adapter for production and an in-memory adapter for testing, so the logic sits in one deep module even though it is deployed across a network."_

### 4. True External (Mock)

Third-party services (Stripe, Twilio, SendGrid, etc.) you do not control. The deepened module takes the external dependency as an injected port; tests provide a mock adapter.

## Seam Discipline

**One adapter = hypothetical seam. Two adapters = real seam.** Do not introduce a port unless at least two adapters are justified (typically production + test). A single-adapter seam is indirection without leverage.

**Internal seams vs external seams.** A deep module can have internal seams (private to its implementation, used by its own unit tests) as well as the external seam at its interface. Do not expose internal seams through the external interface just because tests use them.

## Testing Strategy: Replace, Don't Layer

- Old unit tests on shallow modules become waste once tests at the deepened module's interface exist — delete them.
- Write new tests at the deepened module's interface. The **interface is the test surface**.
- Tests assert on observable outcomes through the interface, not on internal state.
- Tests should survive internal refactors. If a test must change when the implementation changes, it is testing past the interface — fix the seam placement, not the test.
