# DOC_LINKS — testing-e2e-playwright

Reference hub for the `testing-e2e-playwright` skill: selectors, Page Object Model, visual regression, network interception, auth state reuse, CI sharding, mobile emulation, and accessibility integration.

## Official documentation

- Playwright portal: https://playwright.dev/
- Playwright for Node.js: https://playwright.dev/docs/intro
- Playwright for Python: https://playwright.dev/python/
- Playwright for .NET: https://playwright.dev/dotnet/
- Playwright for Java: https://playwright.dev/java/
- API reference (JS/TS): https://playwright.dev/docs/api/class-playwright
- Locators: https://playwright.dev/docs/locators
- Auto-waiting: https://playwright.dev/docs/actionability
- Trace Viewer: https://playwright.dev/docs/trace-viewer
- Storage state / auth reuse: https://playwright.dev/docs/auth
- Network mocking: https://playwright.dev/docs/network
- Browser contexts: https://playwright.dev/docs/browser-contexts
- Visual comparisons: https://playwright.dev/docs/test-snapshots
- Component testing: https://playwright.dev/docs/test-components
- Test parallelism & sharding: https://playwright.dev/docs/test-parallel | https://playwright.dev/docs/test-sharding
- Playwright configuration: https://playwright.dev/docs/test-configuration
- Playwright fixtures: https://playwright.dev/docs/test-fixtures
- Playwright reporters: https://playwright.dev/docs/test-reporters
- Docker image: https://playwright.dev/docs/docker
- CI recipes: https://playwright.dev/docs/ci
- Releases: https://github.com/microsoft/playwright/releases
- Device descriptors source: https://github.com/microsoft/playwright/blob/main/packages/playwright-core/src/server/deviceDescriptorsSource.json

## Specs & RFCs

- WebDriver BiDi (W3C): https://w3c.github.io/webdriver-bidi/
- Chrome DevTools Protocol: https://chromedevtools.github.io/devtools-protocol/
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- ARIA 1.2: https://www.w3.org/TR/wai-aria-1.2/
- Accessibility name computation: https://www.w3.org/TR/accname-1.2/
- axe-core rule descriptions: https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md

## Guides & tutorials

- Playwright best practices (official): https://playwright.dev/docs/best-practices
- Playwright blog: https://playwright.dev/blog
- Applitools + Playwright: https://applitools.com/docs/topics/integrations/playwright/
- Chromatic + Playwright visual tests: https://www.chromatic.com/docs/playwright
- Kent C. Dodds "Testing Trophy": https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications
- axe-core + Playwright: https://github.com/dequelabs/axe-core-npm/tree/develop/packages/playwright
- Cypress → Playwright migration: https://playwright.dev/docs/cypress
- Selenium → Playwright migration: https://playwright.dev/docs/selenium

## Tools & libraries

- @playwright/test runner: https://playwright.dev/docs/api/class-test
- @axe-core/playwright: https://github.com/dequelabs/axe-core-npm/tree/develop/packages/playwright
- playwright-lighthouse: https://github.com/abhinaba-ghosh/playwright-lighthouse
- playwright-bdd (Cucumber): https://vitalets.github.io/playwright-bdd/
- Percy for Playwright (visual): https://www.browserstack.com/docs/percy
- Applitools Eyes: https://applitools.com/
- Checkly (synthetic monitoring): https://www.checklyhq.com/docs/
- msw (network mocking): https://mswjs.io/docs/
- Playwright MCP server: https://github.com/microsoft/playwright-mcp
- Playwright test generator (`codegen`): https://playwright.dev/docs/codegen
- Allure / Monocart / HTML reporters: https://docs.qameta.io/allure/ | https://github.com/cenfun/monocart-reporter

## Freshness

- Last verified: 2026-04-21
- Playwright bundles pinned browser builds (Chromium, Firefox, WebKit) — match the Playwright version to the browser matrix at https://playwright.dev/docs/browsers; do not mix and match.
- WebDriver BiDi support is stable in Playwright; CDP is still the default transport for Chromium.
- `@playwright/test` sharding supports load-balanced shards (`--shard=1/4` plus shard-aware reporters) — use blob + merge-reports for aggregated HTML.
- Component testing is still experimental for Vue/React/Svelte/Solid — check framework adapter compatibility before adopting in CI.
- Playwright Docker image is published as `mcr.microsoft.com/playwright:v<version>-jammy` (Node) and `-noble` variants; verify the exact tag at each upgrade.
- **Update (verified 2026-07-28)**: the "component testing is still experimental" line above is superseded for `@playwright/test` >= 1.62 (released 2026-07-24) -- component testing moved to a stable, built-in stories-and-galleries model at that release (see the installed `@playwright/test` changelog and migration guide for the full mechanics). The experimental-adapter caveat above still applies to any project still on `@playwright/experimental-ct-react`/`-vue`/`-svelte` and to versions before 1.62 -- check the installed `@playwright/test` version before relying on either claim.
