# Refactor Candidates

Reference for the `tdd` skill. Read after all tests are GREEN before committing the cycle.

**Golden rule: never refactor while RED. Get to GREEN first, then look for refactor candidates.**

---

## What to look for after GREEN

| Candidate | Signal | Move |
|-----------|--------|------|
| **Duplication** | Same logic appears in two or more places | Extract function / class |
| **Long method** | Method exceeds ~20 lines or has multiple levels of abstraction | Break into private helpers (keep tests on public interface) |
| **Shallow module** | Function/class with complex interface but trivial body | Combine or deepen; push complexity behind a simpler face |
| **Feature envy** | Code that uses more data from another module than its own | Move logic to where the data lives |
| **Primitive obsession** | Raw strings, ints, or dicts where a value object would express intent | Introduce a value object or dataclass |
| **Existing code revealed** | The new code exposes a smell in adjacent code | Address now if it is in scope, otherwise out of scope: leave it |

---

## Refactoring rules during TDD

1. **One refactor at a time.** Pick one candidate, apply the move, run tests. Green? Commit. Then repeat.
2. **Tests must stay green throughout.** If any test turns red during refactoring, you changed behavior — revert the last step and investigate.
3. **Do not change test assertions to match new behavior.** Refactoring commits change structure only; failing tests mean a behavior change snuck in.
4. **Keep tests on the public interface.** Even when extracting private helpers, do not add tests for the helpers. Tests remain anchored to observable behavior.
5. **Commit at a green point worth keeping.** Small reversible commits.

---

## Python-flavored examples

### Extract duplication into a shared function

```python
# Before: same validation in two handlers
def create_order(data):
    if data["quantity"] <= 0:
        raise ValueError("quantity must be positive")
    ...

def update_order(order_id, data):
    if data["quantity"] <= 0:
        raise ValueError("quantity must be positive")
    ...

# After: extracted
def _validate_quantity(data: dict) -> None:
    if data["quantity"] <= 0:
        raise ValueError("quantity must be positive")

def create_order(data):
    _validate_quantity(data)
    ...

def update_order(order_id, data):
    _validate_quantity(data)
    ...
```

### Replace primitive obsession with a value object

```python
# Before: raw dict carries money
def apply_discount(total: dict, pct: float) -> dict:
    return {"amount": total["amount"] * (1 - pct), "currency": total["currency"]}

# After: value object carries invariants
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def apply_discount(self, pct: float) -> "Money":
        return Money(self.amount * Decimal(1 - pct), self.currency)
```

### Deepen a shallow module

```python
# Before: caller owns too much logic
def send_welcome_email(user_id):
    user = db.get(user_id)
    template = load_template("welcome")
    body = template.render(name=user.name, plan=user.plan.display_name)
    mailer.send(to=user.email, subject="Welcome!", body=body)

# After: push complexity behind a single-concept interface
def send_welcome_email(user_id):
    user = db.get(user_id)
    mailer.send_template("welcome", recipient=user, context={"plan": user.plan.display_name})
```

---

## What NOT to do

- Do not extract abstractions speculatively ("we might need this later").
- Do not refactor code that is not touched by the current TDD cycle.
- Do not introduce design patterns (Strategy, Observer, etc.) unless a concrete second use case exists right now.
- Do not rewrite working, stable, untouched code during a refactoring pass.

For a full catalog of refactoring moves (Extract Method, Move Method, Replace Conditional with Polymorphism, Parallel Change, etc.) see the `refactoring-catalog` skill.
