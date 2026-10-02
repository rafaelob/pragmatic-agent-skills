<!-- FRESHNESS: Always verify against official docs. Links may change. Last structured: 2026-03 -->

# Threat Modeling Frameworks

## Authoritative sources

- OWASP Threat Modeling: https://owasp.org/www-community/Threat_Modeling
- OWASP Threat Modeling Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html
- STRIDE reference (Microsoft): https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats
- PASTA threat modeling: https://owasp.org/www-pdf-archive/AppSecEU2012_PASTA.pdf
- NIST SP 800-154 (data-centric threat modeling): https://csrc.nist.gov/publications/detail/sp/800-154/draft

## STRIDE

A per-component threat classification framework. For each component in the system, ask whether it is vulnerable to each category.

| Category                  | Threat                                     | Mitigation direction              |
|---------------------------|--------------------------------------------|-----------------------------------|
| **S**poofing              | Attacker impersonates a user or service    | Strong authentication, mutual TLS |
| **T**ampering             | Attacker modifies data in transit or at rest| Integrity checks, signing, MAC    |
| **R**epudiation           | Attacker denies performing an action       | Audit logging, non-repudiation    |
| **I**nformation Disclosure| Attacker accesses unauthorized data        | Encryption, access control, minimization |
| **D**enial of Service     | Attacker disrupts availability             | Rate limiting, redundancy, scaling |
| **E**levation of Privilege| Attacker gains higher permissions          | Least privilege, authorization checks |

### How to apply STRIDE

1. Draw a data flow diagram (DFD) of the system: processes, data stores, data flows, external entities, trust boundaries.
2. For each element crossing a trust boundary, evaluate all 6 STRIDE categories.
3. For each identified threat, assign likelihood (Low/Medium/High) and impact (Low/Medium/High/Critical).
4. Define mitigations and map them to implementation tasks.
5. Prioritize: High-likelihood + High-impact threats first.

## PASTA (Process for Attack Simulation and Threat Analysis)

A 7-stage risk-centric methodology that aligns security with business objectives.

### Stages

1. **Define objectives**: align with business goals, compliance, and risk appetite.
2. **Define technical scope**: enumerate applications, services, infrastructure, and data flows.
3. **Application decomposition**: create DFDs, identify entry points, assets, and trust boundaries.
4. **Threat analysis**: research applicable threats using threat intelligence, CVE databases, and attack libraries.
5. **Vulnerability analysis**: map vulnerabilities to threats using SAST/DAST results, pen test findings, and design weaknesses.
6. **Attack modeling**: build attack trees showing how an attacker chains vulnerabilities to reach objectives.
7. **Risk and impact analysis**: calculate risk scores, prioritize by business impact, define mitigations.

### When to use PASTA vs STRIDE

- **STRIDE**: faster, developer-friendly, good for per-feature or per-sprint threat analysis.
- **PASTA**: more thorough, business-aligned, good for quarterly or major-release security assessments.

## Attack trees

A goal-oriented decomposition of how an attacker might achieve a specific objective.

### Structure

```
Root: Steal user credentials
├── OR: Phish user
│   ├── AND: Send phishing email
│   │   └── AND: User clicks link and enters credentials
│   └── AND: Create fake login page
├── OR: Exploit authentication vulnerability
│   ├── OR: SQL injection in login form
│   └── OR: Credential stuffing (leaked passwords)
├── OR: Intercept credentials in transit
│   └── AND: Downgrade to HTTP + MITM
└── OR: Access credential store
    ├── OR: Exploit database vulnerability
    └── OR: Compromise admin account
```

### How to build attack trees

1. Define the attacker's goal (root node).
2. Decompose into sub-goals using AND/OR logic.
3. Assign attributes: cost, skill required, likelihood, detectability.
4. Identify leaf nodes that are feasible and impactful -- these are the priority threats.
5. Map mitigations to cut off attack paths at the earliest feasible point.

## Lightweight threat modeling for agile teams

For teams integrating threat modeling into sprints:

1. **Scope**: focus on new features, changed data flows, and new external integrations (not the entire system every sprint).
2. **Time-box**: 30-60 minutes per feature using STRIDE.
3. **Participants**: developer, security champion, and product owner (optional).
4. **Artifacts**: lightweight DFD (whiteboard/Miro), threat table, and linked tickets for mitigations.
5. **Tracking**: add threat model findings as security-labeled issues in the backlog.
6. **Review cadence**: full PASTA-style review quarterly or for major architectural changes.

## Threat model document template (minimal)

```markdown
## [Feature/Component Name] Threat Model

**Date**: YYYY-MM-DD | **Reviewer(s)**: names

### Data flow diagram
[Link to diagram or embed image]

### Assets
- [List data and resources worth protecting]

### Trust boundaries
- [List boundaries between different trust levels]

### Threats (STRIDE)
| ID | Category | Threat | Likelihood | Impact | Mitigation | Status |
|----|----------|--------|------------|--------|------------|--------|
| T1 | Spoofing | ...    | High       | High   | ...        | Open   |

### Decisions and assumptions
- [Key assumptions and accepted risks]
```
