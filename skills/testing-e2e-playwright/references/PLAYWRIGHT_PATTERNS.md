# Playwright Patterns Guide

> Freshness: Verify Playwright APIs and configuration against https://playwright.dev/docs/ before adoption. Playwright releases frequently with potential breaking changes.

## Selector Best Practices

### Priority order (most stable to least)
1. **Role selectors**: `page.getByRole('button', { name: 'Submit' })` -- accessible, resilient.
2. **Test IDs**: `page.getByTestId('submit-btn')` -- stable, team-controlled.
3. **Text/label**: `page.getByText('Welcome')`, `page.getByLabel('Email')` -- user-visible.
4. **CSS/XPath**: `page.locator('.btn-primary')` -- fragile, last resort.

### Anti-patterns to avoid
- Auto-generated class names (e.g., `css-1a2b3c`): break on rebuild.
- Nth-child selectors: break when DOM order changes.
- XPath with deep nesting: unmaintainable.
- `page.locator('#id')` when the ID is auto-generated.

### Stable test ID convention
```html
<!-- In application code -->
<button data-testid="checkout-submit">Place Order</button>
```
```typescript
// In test
await page.getByTestId('checkout-submit').click();
```
Use `data-testid` attribute; strip from production builds if desired.

## Page Object Model (POM)

### Structure convention
```
e2e/
  pages/
    login.page.ts
    dashboard.page.ts
    checkout.page.ts
  components/
    navbar.component.ts
    modal.component.ts
  fixtures/
    auth.fixture.ts
  tests/
    checkout.spec.ts
    dashboard.spec.ts
```

### POM rules
- One class per page/major component.
- Encapsulate selectors and user actions.
- Methods return void or the next page object (for navigation).
- Do NOT put assertions in POMs -- keep them in test files.
- Use TypeScript for type safety and autocompletion.

### Composition over inheritance
```typescript
// Compose shared components into pages
export class CheckoutPage {
  readonly navbar: NavbarComponent;
  readonly cart: CartComponent;

  constructor(private page: Page) {
    this.navbar = new NavbarComponent(page);
    this.cart = new CartComponent(page.getByTestId('cart-panel'));
  }
}
```

## Authentication Patterns

### Storage state (recommended)
```typescript
// Global setup: login once, save state
const authFile = '.auth/user.json';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill(process.env.TEST_USER_EMAIL!);
  await page.getByLabel('Password').fill(process.env.TEST_USER_PASSWORD!);
  await page.getByRole('button', { name: 'Sign in' }).click();
  await page.waitForURL('/dashboard');
  await page.context().storageState({ path: authFile });
});
```

### Multi-role testing
```typescript
// playwright.config.ts
projects: [
  { name: 'setup', testMatch: /auth\.setup\.ts/ },
  { name: 'admin', use: { storageState: '.auth/admin.json' }, dependencies: ['setup'] },
  { name: 'member', use: { storageState: '.auth/member.json' }, dependencies: ['setup'] },
]
```

### API-based auth (faster alternative)
```typescript
// Skip UI login; set auth token directly
const token = await getTestToken({ role: 'admin' });
await page.context().addCookies([{ name: 'session', value: token, url: baseURL }]);
```

## CI Setup Patterns

### GitHub Actions (complete example)
```yaml
name: E2E Tests
on: [push]
jobs:
  e2e:
    runs-on: ubuntu-latest
    container:
      image: mcr.microsoft.com/playwright:v<CURRENT_VERSION>-noble  # pin to your project's Playwright version
    steps:
      - uses: actions/checkout@<full-sha>  # current major v6; pin to full SHA
      - uses: actions/setup-node@<full-sha>  # current major v6; pin to full SHA
        with:
          node-version-file: '.node-version'  # commit a line verified as Active/Maintenance LTS
      - run: npm ci
      - run: npx playwright test
        env:
          CI: true
          BASE_URL: http://app:3000
      - uses: actions/upload-artifact@<full-sha>  # current major v7; pin to full SHA
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 14
```

### Sharding for large suites
```yaml
strategy:
  fail-fast: false
  matrix:
    shard: [1/4, 2/4, 3/4, 4/4]
steps:
  - run: npx playwright test --shard=${{ matrix.shard }}
```

### Merge sharded reports
```yaml
- name: Merge reports
  run: npx playwright merge-reports --reporter=html ./all-blob-reports
```

## Accessibility with axe-core

### Setup
```bash
npm install -D @axe-core/playwright
```

### Usage in tests
```typescript
import AxeBuilder from '@axe-core/playwright';

test('page meets WCAG 2.1 AA', async ({ page }) => {
  await page.goto('/dashboard');
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .exclude('.third-party-widget')  // known third-party violations
    .analyze();
  expect(results.violations).toEqual([]);
});
```

### Integrate into every page test
```typescript
// Shared fixture
async function checkAccessibility(page: Page) {
  const { violations } = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze();
  expect(violations).toEqual([]);
}
```

## Official Documentation Links
- Playwright docs: https://playwright.dev/docs/
- Playwright test runner: https://playwright.dev/docs/test-intro
- Locators guide: https://playwright.dev/docs/locators
- Visual comparisons: https://playwright.dev/docs/test-snapshots
- Authentication: https://playwright.dev/docs/auth
- CI: https://playwright.dev/docs/ci
- axe-core Playwright: https://github.com/dequelabs/axe-core-npm/tree/develop/packages/playwright
