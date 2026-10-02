# When to Mock

Reference for the `tdd` skill. Read when deciding whether something should be mocked.

---

## The Rule

**Mock at system boundaries only. Never mock things you own and control.**

### Mock (at boundaries)

- External third-party APIs (payment gateways, email providers, SMS services)
- Time and randomness (`datetime.now()`, `uuid.uuid4()`, `random`)
- File system when tests must remain fast and isolated
- External databases — but prefer a real test DB over a mock when feasible

### Do not mock

- Your own classes, modules, or services
- Internal collaborators (classes/functions you wrote)
- Anything you control

The test for "should I mock this?" is: **is this a boundary between my system and the outside world?** If yes, mock it. If it is code you own, test through it.

---

## Designing for Mockability at Boundaries

Good mockability comes from good design, not from test-specific patching.

### 1. Use dependency injection

Inject external dependencies; do not create them internally.

```python
# GOOD: dependency injected — easy to substitute in tests
def process_payment(order: Order, payment_client: PaymentClient) -> Receipt:
    return payment_client.charge(order.total)

# BAD: dependency created internally — requires patching internals
def process_payment(order: Order) -> Receipt:
    client = StripeClient(settings.STRIPE_KEY)
    return client.charge(order.total)
```

```typescript
// GOOD: injected
function processPayment(order: Order, paymentClient: PaymentClient): Promise<Receipt> {
  return paymentClient.charge(order.total);
}

// BAD: self-instantiated
function processPayment(order: Order): Promise<Receipt> {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

In pytest, inject via fixtures:

```python
@pytest.fixture
def fake_payment_client():
    class Fake:
        def charge(self, amount):
            return Receipt(status="confirmed", amount=amount)
    return Fake()

def test_payment_succeeds(fake_payment_client):
    result = process_payment(order_fixture(), fake_payment_client)
    assert result.status == "confirmed"
```

### 2. Prefer SDK-style interfaces over generic dispatchers

Each external operation gets its own explicit function. This makes each mock return one specific shape with no conditional logic inside the test.

```typescript
// GOOD: each function is independently mockable
const api = {
  getUser:    (id: string)   => fetch(`/users/${id}`),
  getOrders:  (userId: string) => fetch(`/users/${userId}/orders`),
  createOrder: (data: Order) => fetch('/orders', { method: 'POST', body: JSON.stringify(data) }),
};

// BAD: generic dispatcher requires conditional mock logic
const api = {
  fetch: (endpoint: string, options?: RequestInit) => fetch(endpoint, options),
};
```

```python
# GOOD: protocol / ABC with explicit operations
class UserRepository(Protocol):
    def get(self, user_id: str) -> User: ...
    def save(self, user: User) -> None: ...
    def list_orders(self, user_id: str) -> list[Order]: ...

# BAD: generic data-access blob
class Repository(Protocol):
    def query(self, sql: str, params: tuple) -> list[dict]: ...
```

SDK-style benefits:
- One mock per operation; no conditional logic in test setup
- Clear which operations a test exercises
- Type-safe stubs per operation (mypy / TypeScript strict)

---

## Mocking Time and Randomness

```python
# pytest with freezegun
from freezegun import freeze_time

@freeze_time("2026-06-29")
def test_subscription_expires_after_30_days():
    sub = create_subscription(start_date=date(2026, 6, 29))
    assert sub.expires_on == date(2026, 7, 29)

# or inject a clock
def create_subscription(start_date: date, *, clock=date.today) -> Subscription:
    return Subscription(start=start_date, expires=start_date + timedelta(days=30))
```

---

## Quick Checklist

```
[ ] Mocked thing is at a system boundary (external API, time, FS)
[ ] Not mocking classes/functions I own
[ ] External dependency is injected, not self-instantiated
[ ] Interface is SDK-style (one function per operation)
[ ] No conditional logic inside the mock itself
[ ] Prefer a real test DB over mocking the DB layer when feasible
```
