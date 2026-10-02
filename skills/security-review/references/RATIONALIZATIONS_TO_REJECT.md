# Rationalizations to reject

Read this before closing a security finding as "not applicable". These are the excuses that skip a control.

| Excuse | Reject because |
|---|---|
| "It's only internal" | Internal is still a trust boundary. IDOR and SSRF do not need the public internet |
| "We'll add auth later" | An unauthenticated write is the product until auth ships |
| "The framework handles that" | Name the middleware and the config. An unnamed handler is absent |
| "Nobody would send that input" | Attackers send that input. Instantiate it |
| "HTTPS is enough" | TLS does not stop XSS, CSRF, IDOR, or injection |
| "We don't store secrets in git" | Check env files, CI logs, client bundles, and error responses |
| "It's a prototype" | Prototypes get deployed. Mark the risk with owner and sunset or fix it |
| "The linter is green" | Linters do not prove authorization. Trace the actor to the sink |

A skipped class without this table filled is "not hunted", never "clean".
