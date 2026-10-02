<!-- FRESHNESS: Always verify against official docs. Links may change. Last structured: 2026-03 -->

# Refactoring Moves Quick Reference

Condensed reference for common refactoring moves with preconditions, mechanics, and examples.

## Core moves: preconditions, mechanics, verification

The five most frequently used moves, with full step-by-step mechanics.

**Extract Method**
- Preconditions: code block has a clear purpose; all variables are available in scope.
- Mechanics: (1) identify code to extract; (2) create new method with intention-revealing name; (3) copy code; (4) replace variables with parameters or return values; (5) replace original code with method call.
- Verification: run existing tests; behavior must be identical.

**Move Method/Function**
- Preconditions: method uses more features of another class; target class exists.
- Mechanics: (1) examine all features used by the method in its current class; (2) check sub/superclass usage; (3) declare method on target; (4) copy body; (5) adjust references; (6) redirect original to delegate or remove.
- Verification: run tests for both source and target classes.

**Replace Conditional with Polymorphism**
- Preconditions: switch/if-else on type code that drives different behavior.
- Mechanics: (1) create class hierarchy or strategy interfaces; (2) move each branch into overriding method; (3) replace conditional with polymorphic call.
- Verification: run tests; each branch should have test coverage.

**Introduce Parameter Object**
- Preconditions: group of parameters that appear together across multiple methods.
- Mechanics: (1) create a class/record with the grouped fields; (2) replace parameter lists with the new object; (3) look for behavior to move into the new object.
- Verification: run tests; callers updated.

**Extract Class**
- Preconditions: class has multiple responsibilities (violates SRP).
- Mechanics: (1) identify cohesive subset of fields and methods; (2) create new class; (3) move fields and methods; (4) establish relationship (composition).
- Verification: run tests for both classes.

## Method-Level Refactorings

### Extract Method

**Preconditions**: code block performs a distinct task; variables are accessible.

```python
# Before
def print_invoice(invoice):
    print("=== Invoice ===")
    for item in invoice.items:
        total = item.quantity * item.price
        print(f"  {item.name}: {total}")
    total = sum(i.quantity * i.price for i in invoice.items)
    print(f"Total: {total}")

# After
def print_invoice(invoice):
    print("=== Invoice ===")
    print_line_items(invoice.items)
    print_total(invoice.items)
```

### Inline Method

**Preconditions**: method body is as clear as the method name; not overridden.

### Replace Temp with Query

**Preconditions**: temporary variable holds a computation result used once or twice. Extract computation into its own method.

## Class-Level Refactorings

### Extract Class

**Preconditions**: class has fields/methods forming a cohesive subgroup (SRP violation).

```python
# Before: Person has phone-related fields
class Person:
    def __init__(self, name, area_code, number):
        self.name = name
        self.area_code = area_code
        self.number = number

# After: phone extracted into its own class
class TelephoneNumber:
    def __init__(self, area_code, number):
        self.area_code = area_code
        self.number = number

class Person:
    def __init__(self, name, phone: TelephoneNumber):
        self.name = name
        self.phone = phone
```

### Move Method

**Preconditions**: method uses more features of another class than its own. Move it to the class it uses most, passing needed data as parameters.

### Introduce Parameter Object

**Preconditions**: multiple methods share the same group of parameters.

```python
@dataclass(frozen=True)
class DateRange:
    start: date
    end: date

def amount_invoiced(period: DateRange): ...
def amount_received(period: DateRange): ...
```

## Conditional Refactorings

### Replace Conditional with Polymorphism

**Preconditions**: switch/if-else on type code driving different behavior.

```python
# Before: match on employee.type
# After: Employee ABC with Engineer, Salesperson, Manager subclasses
class Employee(ABC):
    @abstractmethod
    def calculate_pay(self) -> float: ...

class Engineer(Employee):
    def calculate_pay(self) -> float:
        return self.salary
```

## Safe Refactoring Sequences

### Large Class to Smaller Classes

1. Identify cohesive groups of fields/methods. 2. Extract Class (one at a time). 3. Run tests + commit after each extraction. 4. Establish composition. 5. Move callers. 6. Clean up.

### Replace Switch with Strategy

1. Extract each case branch into own method. 2. Create Strategy interface. 3. Create concrete strategies. 4. Replace switch with strategy selection. 5. Delete original switch. 6. Test after each step.

## IDE Refactoring Support Matrix

| Refactoring | IntelliJ | VS Code | PyCharm | Visual Studio |
|------------|----------|---------|---------|---------------|
| Extract Method | Safe | Basic | Safe | Safe |
| Rename | Safe (cross-refs) | Basic | Safe | Safe |
| Move | Safe | Partial | Safe | Safe |
| Extract Interface | Yes | No | Yes | Yes |
| Change Signature | Yes | No | Yes | Yes |

**"Safe"** = IDE verifies preconditions and updates all references.

## References

- Refactoring Catalog: https://refactoring.com/catalog/
- Refactoring Guru: https://refactoring.guru/refactoring/catalog
- Martin Fowler: https://martinfowler.com/tags/refactoring.html
