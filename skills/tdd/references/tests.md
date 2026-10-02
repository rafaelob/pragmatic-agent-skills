# Good and Bad Tests

Reference for the `tdd` skill. Read when deciding whether a test is well-formed before committing it to the cycle.

---

## Good Tests

**Integration-style**: exercise real code paths through public APIs; they verify behavior the caller cares about, not internal mechanics.

### Python example (pytest)

```python
# GOOD: Tests observable behavior through the public interface
def test_user_can_checkout_with_valid_cart(checkout, cart_factory, payment_method):
    cart = cart_factory()
    cart.add(product)
    result = checkout(cart, payment_method)
    assert result.status == "confirmed"
```

### TypeScript example (Jest — clearest for async flows)

```typescript
// GOOD: Tests observable behavior
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

Characteristics:

- Tests behavior users/callers care about
- Uses public API only
- Survives internal refactors
- Describes WHAT, not HOW
- One logical assertion per test

---

## Bad Tests

### Implementation-detail tests

Coupled to internal structure — they break on refactors even when behavior has not changed.

```typescript
// BAD: Verifies an internal call, not the outcome
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

Red flags:

- Mocking internal collaborators (things you own and control)
- Testing private methods
- Asserting on call counts or call order
- Test breaks when renaming an internal function
- Test name describes HOW, not WHAT

### Bypassing the interface to verify state

```typescript
// BAD: Goes behind the interface to check persistence directly
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// GOOD: Verifies through the interface the caller would use
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```

### Python equivalent

```python
# BAD: Leaks into persistence layer
def test_create_user_saves_to_db(session):
    create_user(name="Alice")
    row = session.execute(text("SELECT * FROM users WHERE name = 'Alice'")).first()
    assert row is not None

# GOOD: Verifies through the public interface
def test_create_user_is_retrievable(create_user, get_user):
    user = create_user(name="Alice")
    retrieved = get_user(user.id)
    assert retrieved.name == "Alice"
```

---

## Tautological Tests

The expected value is recomputed the same way the code computes it, so the test can never disagree with the code.

```typescript
// BAD: expected mirrors the implementation — break the code and the assertion breaks with it
test("calculateTotal sums line items", () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, i) => sum + i.price, 0);  // same logic as SUT
  expect(calculateTotal(items)).toBe(expected);
});

// GOOD: expected is an independent known literal from a worked example
test("calculateTotal sums line items", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```

```python
# BAD
def test_calculate_total():
    items = [{"price": 10}, {"price": 5}]
    expected = sum(i["price"] for i in items)  # same logic as SUT
    assert calculate_total(items) == expected

# GOOD
def test_calculate_total():
    assert calculate_total([{"price": 10}, {"price": 5}]) == 15
```

**Rule**: the expected value must come from an independent source of truth — a known-good literal, a worked example from the spec, or a previously validated oracle. If deriving the expected value requires running the same algorithm the code runs, the test is tautological.

---

## Quick Checklist

```
[ ] Test describes behavior (WHAT), not implementation (HOW)
[ ] Test uses public interface only — no private methods, no internal mocks
[ ] Test survives an internal rename or refactor
[ ] Expected values are independent literals, not recomputed from the code
[ ] One logical assertion per test
[ ] Test name reads like a behavioral specification
```
