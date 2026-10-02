<!-- FRESHNESS: Always verify against official docs. Links may change. Last structured: 2026-03 -->

# Automated Refactoring Tools Reference

Practical reference for setting up and using automated refactoring tools across language ecosystems.

## Tool catalog (by language)

| Language | Tool | Capabilities | License |
|----------|------|-------------|---------|
| Java | **OpenRewrite** | Recipe-based AST transforms; framework migrations; code style | Apache 2.0 |
| Java/Kotlin | **IntelliJ IDEA** refactorings | IDE-assisted: extract, move, rename, inline (safe) | Community/Paid |
| JavaScript/TypeScript | **jscodeshift** | AST-based codemods (Facebook) | MIT |
| JavaScript/TypeScript | **ts-morph** | TypeScript AST manipulation API | MIT |
| PHP | **Rector** | Automated refactoring and upgrades | MIT |
| Scala | **Scalafix** | Rule-based Scala refactoring | Apache 2.0 |
| Python | **Ruff** | Linting + autofixes (very fast, Rust-based) | MIT |
| Python | **Bowler** | AST-based refactoring (Facebook, archived) | MIT |
| Python | **rope** | Python refactoring library | LGPL |
| .NET | **Roslyn Analyzers** | Code analysis + fixes | MIT |
| Multi-language | **Comby** | Structural search and replace | Apache 2.0 |
| Multi-language | **Semgrep** | Pattern-based code transformation | LGPL |

## OpenRewrite (Java/Kotlin/Groovy)

Recipe-based AST transformations for framework migrations, code style, and vulnerability fixes.

```kotlin
// build.gradle.kts
plugins { id("org.openrewrite.rewrite") version "7.x.x" }
rewrite { activeRecipe("org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_3") }
dependencies { rewrite("org.openrewrite.recipe:rewrite-spring:5.x.x") }
```

```bash
./gradlew rewriteDryRun   # preview
./gradlew rewriteRun      # apply
./gradlew rewriteDiscover  # list recipes
```

Key recipes: `UpgradeSpringBoot_3_3`, `UpgradeToJava21`, `MigrateJunit5`, `CommonStaticAnalysis`.

## jscodeshift (JavaScript/TypeScript)

AST-based codemods with jQuery-like API.

```javascript
// transform.js -- rename import source
module.exports = function(fileInfo, api) {
  const j = api.jscodeshift;
  return j(fileInfo.source)
    .find(j.ImportDeclaration, { source: { value: 'old-module' } })
    .forEach(path => { path.node.source.value = 'new-module'; })
    .toSource();
};
```

```bash
npx jscodeshift -t transform.js src/
npx jscodeshift -t transform.js --dry src/   # preview
npx jscodeshift -t transform.ts --parser tsx src/  # TypeScript
```

## Rector (PHP)

Automated PHP refactoring and upgrades.

```php
// rector.php
return RectorConfig::configure()
    ->withPaths([__DIR__ . '/src'])
    ->withSets([SetList::PHP_83, SetList::CODE_QUALITY, SetList::DEAD_CODE]);
```

```bash
vendor/bin/rector process --dry-run  # preview
vendor/bin/rector process            # apply
```

## Scalafix (Scala)

Rule-based Scala refactoring. Built-in rules: `RemoveUnused`, `OrganizeImports`, `ExplicitResultTypes`.

```bash
sbt "scalafix --check"   # verify
sbt scalafix              # apply
```

## Ruff (Python)

Extremely fast linter and formatter (Rust-based) with auto-fix.

```toml
# pyproject.toml
[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "RUF"]
fixable = ["ALL"]
```

```bash
ruff check --fix src/     # auto-fix
ruff check --diff src/    # preview
ruff format src/           # format
```

Key rule groups: `UP` (pyupgrade), `F401` (unused imports), `I` (isort), `SIM` (simplify), `B` (bugbear).

## Comby (Multi-Language)

Structural search and replace that understands code structure.

```bash
comby 'print(:[arg])' 'logger.info(:[arg])' .py -d src/
comby 'assertEqual(:[a], :[b])' 'assert :[a] == :[b]' .py -d tests/ -in-place
```

## CI Integration

### Pre-commit Hook

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.x.x
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

### GitHub Actions

```yaml
jobs:
  python-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<full-sha>  # current major v6; pin to full SHA
      - uses: astral-sh/ruff-action@<full-sha>  # pin third-party actions to full SHA
        with: { args: "check --diff" }
  java-rewrite:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<full-sha>  # current major v6; pin to full SHA
      - uses: actions/setup-java@<full-sha>  # pin to full SHA
        with: { distribution: temurin, java-version: 21 }
      - run: ./gradlew rewriteDryRun
```

## References

- OpenRewrite: https://docs.openrewrite.org/
- jscodeshift: https://github.com/facebook/jscodeshift
- Rector: https://getrector.com/documentation
- Scalafix: https://scalacenter.github.io/scalafix/
- Ruff: https://docs.astral.sh/ruff/
- Comby: https://comby.dev/docs/
