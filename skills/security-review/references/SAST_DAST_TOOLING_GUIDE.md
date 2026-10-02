<!-- FRESHNESS: Always verify against official docs. Links may change. Last structured: 2026-03 -->

# SAST, DAST & SCA Tooling Guide

## Authoritative sources

- Semgrep documentation: https://semgrep.dev/docs/
- CodeQL documentation: https://codeql.github.com/docs/
- OWASP ZAP: https://www.zaproxy.org/docs/
- Snyk documentation: https://docs.snyk.io/
- Trivy documentation: https://aquasecurity.github.io/trivy/
- Nuclei documentation: https://docs.projectdiscovery.io/tools/nuclei/overview

## SAST (Static Application Security Testing)

### Semgrep

- **What**: fast, pattern-based static analysis supporting 30+ languages. Rules are written in YAML.
- **Strengths**: low false-positive rate; easy to write custom rules; fast CI execution.
- **Use cases**: injection detection, insecure API usage, banned function calls, taint tracking.
- **CI integration**: `semgrep ci` command with `--config auto` for community rules or `--config p/<ruleset>`.
- **Custom rules**: write project-specific rules for internal APIs, banned patterns, or compliance requirements.

```yaml
# Example: detect raw SQL string formatting in Python
rules:
  - id: python-sql-injection
    patterns:
      - pattern: |
          $QUERY = f"...{$VAR}..."
      - pattern-inside: |
          $CURSOR.execute($QUERY, ...)
    message: "Potential SQL injection via f-string formatting"
    severity: ERROR
    languages: [python]
```

### CodeQL

- **What**: semantic code analysis engine by GitHub. Treats code as a queryable database.
- **Strengths**: deep dataflow and taint analysis; finds complex vulnerabilities that pattern-based tools miss.
- **Use cases**: SQL injection with multi-step data flow, XSS through complex transformations, auth bypass.
- **CI integration**: GitHub Actions `github/codeql-action/analyze@24c7eb380a2dc368f2d129e4c65e51d172983a1e` (the official `v4` tag resolved to this full SHA on 2026-08-10). Pin the full SHA; before creating or refreshing a workflow, resolve the current `v4` tag and update the pin instead of committing mutable `@v4`.
- **Custom queries**: write QL queries for project-specific vulnerability patterns. Publish as CodeQL packs.

### Recommended SAST strategy

1. Run Semgrep on every PR (fast, broad coverage, custom rules for project patterns).
2. Run CodeQL on every PR or nightly (deep analysis, catches complex flows).
3. Treat SAST findings as: ERROR = block PR, WARNING = review required, INFO = informational.
4. Document false-positive suppressions inline with justification (e.g., `# nosemgrep: reason`).

## DAST (Dynamic Application Security Testing)

### OWASP ZAP

- **What**: open-source web application security scanner. Proxy-based with active and passive scanning.
- **Modes**:
  - **Passive scan**: observes traffic without modifying requests; finds information disclosure, missing headers, cookies without flags.
  - **Active scan**: sends crafted payloads to find injection, XSS, SSRF, etc. Run only against non-production.
  - **API scan**: import OpenAPI/GraphQL schema for targeted API testing.
- **CI integration**: ZAP Docker image with automation framework. Run against staging in nightly CI.
- **Baseline scan**: `zap-baseline.py` for quick passive-only scan suitable for PR pipelines.

### Nuclei

- **What**: template-based vulnerability scanner. Large community template library.
- **Use cases**: misconfiguration detection, CVE checks, exposed admin panels, default credentials.
- **CI integration**: run against staging with severity threshold (`-severity critical,high`).

### Recommended DAST strategy

1. ZAP baseline (passive) scan on every deployment to staging.
2. ZAP active scan or Nuclei scan weekly or on significant changes.
3. API schema-driven scanning for REST/GraphQL endpoints.
4. Never run active scans against production without explicit authorization.

## SCA (Software Composition Analysis)

### Tools

- **Snyk**: commercial; deep vulnerability database; fix suggestions; license compliance.
- **Dependabot**: GitHub-native; automatic PRs for dependency updates; free for public and private repos.
- **Trivy**: open-source; scans OS packages, language dependencies, container images, IaC.
- **Grype**: open-source; focused vulnerability scanner for containers and filesystems.
- **Renovate**: automated dependency update PRs; highly configurable; supports monorepos.

### SCA CI integration

1. Run on every PR: Snyk test or Trivy filesystem scan.
2. Block on critical/high CVEs with known exploits.
3. Generate SBOM (CycloneDX/SPDX) as a CI artifact for each release.
4. Enable automated update PRs (Dependabot or Renovate) with CI validation.

## CI pipeline integration pattern

```yaml
# Recommended security gate ordering (GitHub Actions example)
jobs:
  sast:
    steps:
      - semgrep ci --config auto
      - codeql analyze

  sca:
    steps:
      - trivy fs --severity CRITICAL,HIGH --exit-code 1 .
      - trivy image --severity CRITICAL,HIGH $IMAGE

  dast:  # Against staging, after deploy
    needs: [deploy-staging]
    steps:
      - zap-baseline.py -t $STAGING_URL
```

## Triage and exception management

- Every suppressed finding must have: justification, reviewer, date, and re-evaluation deadline.
- Maintain a living exceptions list (not scattered in code comments alone).
- Periodically review exceptions (quarterly) to confirm they are still valid.
- Track false-positive rates per tool to tune configurations.
