<!-- FRESHNESS: Always verify against official docs. Links may change. Last structured: 2026-04 -->

# OWASP Top 10:2025 Security Checklist

> Scoped use: consult only the categories relevant to the changed trust boundary. Keep nonapplicable categories out of the work instead of mechanically filling every section.

## Authoritative sources

- OWASP Top 10: https://owasp.org/Top10/
- OWASP Testing Guide: https://owasp.org/www-project-web-security-testing-guide/
- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
- OWASP ASVS (Application Security Verification Standard): https://owasp.org/www-project-application-security-verification-standard/

## A01: Broken Access Control (includes SSRF)

- **Detection**: manual review of every endpoint for authorization checks; automated IDOR testing; DAST crawling; review server-side code that makes HTTP requests based on user input; check for URL/IP allowlisting.
- **Fix patterns**: enforce authorization at API layer AND data layer (row-level security). Deny by default. Validate object ownership on every request. Disable CORS wildcards. Disable directory listing. For SSRF: validate and sanitize all URLs from user input; use allowlists for permitted domains/IPs; block requests to internal/private IP ranges (10.x, 172.16-31.x, 192.168.x, 169.254.x, localhost); disable HTTP redirects or validate each hop; use network segmentation (egress firewall rules).
- **Test**: attempt to access resources belonging to other users/tenants without authorization; supply internal URLs, cloud metadata endpoints (169.254.169.254), and DNS rebinding payloads.

## A02: Security Misconfiguration

- **Detection**: scan for default credentials; check for unnecessary open ports/services; review HTTP security headers; check error page verbosity.
- **Fix patterns**: harden all environments (dev, staging, prod). Remove default accounts and sample applications. Set security headers (CSP, X-Content-Type-Options, X-Frame-Options, Strict-Transport-Security). Disable verbose error messages in production. Automate configuration with IaC.
- **Test**: scan with Nuclei or ZAP for misconfigurations; verify headers with securityheaders.com.

## A03: Software Supply Chain Failures

- **Detection**: SCA tools (Snyk, Dependabot, Trivy, Grype); check for EOL runtimes/frameworks; audit CI/CD plugins and third-party GitHub Actions; inspect install scripts in dependencies; review package provenance.
- **Fix patterns**: maintain a dependency inventory (SBOM). Enable automatic dependency updates. Define severity-based patching SLAs. Remove unused dependencies. Pin versions with lockfiles and hash verification. Verify provenance with SLSA attestations. Pin GitHub Actions to full-length commit SHAs. Use private registries or proxy caches. Review and restrict install scripts in dependencies.
- **Test**: run SCA scans (locally, or in CI when it runs); audit transitive dependencies; verify artifact signatures and provenance; check for typosquat or hijacked packages.

## A04: Cryptographic Failures

- **Detection**: grep for weak algorithms (MD5, SHA1, DES, RC4, ECB mode); check TLS configuration; review key storage.
- **Fix patterns**: use AES-256-GCM for symmetric encryption, SHA-256+ for hashing, CSPRNG for random values. Enforce TLS 1.2+ (prefer 1.3). Store keys in secret managers or HSMs, not in code. Classify data and encrypt sensitive fields at rest.
- **Test**: verify TLS configuration with tools like testssl.sh; check for hardcoded secrets.

## A05: Injection

- **Detection**: SAST rules for string concatenation in SQL/NoSQL/OS commands/LDAP queries; template injection patterns.
- **Fix patterns**: use parameterized queries/prepared statements for all database access. Use ORM query builders. Validate and sanitize all inputs. For OS commands: avoid them entirely or use allowlists with strict validation. For templates: use auto-escaping engines.
- **Test**: fuzz inputs with injection payloads; review raw query construction.

## A06: Insecure Design

- **Detection**: threat modeling; architecture review for missing security controls.
- **Fix patterns**: implement threat modeling early in design. Use secure design patterns (fail securely, defense in depth, least privilege). Rate limit sensitive operations. Implement business logic abuse controls.
- **Test**: abuse case testing; business logic bypass attempts.

## A07: Authentication Failures

- **Detection**: review authentication flows for weak credential policies, missing MFA, credential stuffing exposure.
- **Fix patterns**: implement phishing-resistant MFA (passkeys/FIDO2). Enforce strong password policies or eliminate passwords. Rate-limit and monitor login attempts. Use secure session management (server-side session state or short-lived signed tokens, rotated on login and privilege change, HttpOnly/Secure/SameSite cookies, enforced idle and absolute timeouts). Invalidate sessions on password change.
- **Test**: attempt credential stuffing; test session fixation; verify MFA enforcement.

## A08: Software and Data Integrity Failures

- **Detection**: review CI/CD pipeline for unsigned artifacts; check for insecure deserialization; verify dependency integrity.
- **Fix patterns**: sign artifacts and verify signatures. Use Subresource Integrity (SRI) for CDN resources. Verify lockfile hashes. Never deserialize untrusted data with unsafe deserializers (pickle, yaml.load, Java ObjectInputStream). Use SLSA provenance.
- **Test**: verify artifact signatures; test deserialization with crafted payloads.

## A09: Security Logging and Alerting Failures

- **Detection**: review logging configuration for coverage gaps; check for missing alerting on security events.
- **Fix patterns**: log authentication events (success, failure, lockout), authorization failures, input validation failures, and application errors. Include context (who, what, when, where) but NOT sensitive data. Centralize logs. Set up alerts for anomalous patterns. Ensure log integrity (immutable/append-only storage). Ensure alerts are actionable and routed to on-call personnel.
- **Test**: trigger security events and verify they appear in logs with correct detail; verify alerting triggers.

## A10: Mishandling of Exceptional Conditions

- **Detection**: review error handling paths for silent exception swallowing, missing resource cleanup, unchecked return values, missing timeouts on external calls, and error conditions that bypass security controls.
- **Fix patterns**: handle all error paths explicitly; never silently swallow exceptions. Avoid leaking stack traces or internal paths in responses. Implement proper resource cleanup in all error paths. Define and enforce timeouts for external calls. Use circuit breakers for cascading failure prevention. Validate assumptions about input ranges, null/empty values, and overflow. Ensure exceptional conditions fail closed (do not bypass security controls).
- **Test**: fuzz with malformed inputs and boundary values; test timeout and resource exhaustion scenarios; verify error responses do not leak internal details; confirm security controls remain enforced under error conditions.

## Negative-test triggers by attack vector

A change is security-sensitive when it touches auth/session, secrets, uploads/parsers, a public endpoint, external fetch/redirects, a query (SQL/NoSQL/LDAP/GraphQL), HTML rendering, a subprocess/shell exec, CI/CD, a container, or network exposure. Run the matching negative test; do not run the ones a change did not trigger.

| Attack vector | Trigger | Negative test |
|---|---|---|
| Auth bypass | Auth/session change | Access without valid credentials; expect 401/403 |
| BOLA/IDOR | Resource-access change | Access another actor's resource by manipulating an ID |
| Privilege escalation | Permission/role change | Perform an admin-only action as a lesser role |
| Injection | Query/subprocess change | Send an injection payload in a user-controlled parameter |
| Path traversal | File-handling change | Attempt a `../../` directory escape |
| SSRF | External fetch/redirect change | Redirect to an internal/loopback address or metadata endpoint |
| Unsafe upload | Upload/parser change | Upload an executable, oversized or malformed file |
| Secret leakage | Secret/config change | Confirm secrets absent from logs, responses and error messages |

## Prioritization approach

1. Start with A01 (Broken Access Control, includes SSRF) and A05 (Injection) -- highest exploitability and impact.
2. Address A04 (Cryptographic Failures) and A07 (Authentication Failures) for data protection and identity security.
3. Then A02 (Security Misconfiguration), A03 (Supply Chain), A08 (Integrity).
4. Address A10 (Mishandling of Exceptional Conditions) and A09 (Logging/Alerting) for operational resilience.
5. Finally A06 (Insecure Design) as ongoing design hygiene.
