# Loop Taxonomy — Reproduction Setup Guide

Full setup guidance for each of the 10 feedback loop types from the `diagnosing-bugs` skill. Read when choosing or constructing the reproduction's pass/fail signal.

---

## Loop 1 — Failing test

**Best when**: the bug has a known entry point (function, API handler, domain rule) reachable via automated test.

**Setup pattern (Python/uv)**:

```python
# tests/test_regression_<ticket>.py
import pytest
from myapp.module import buggy_function

def test_regression_<ticket>():
    """Regression: <describe the symptom>."""
    result = buggy_function(fixture_input)
    assert result == expected_value  # previously failing assertion
```

```bash
uv run pytest tests/test_regression_<ticket>.py -x -v
```

**Tighten**: use `pytest -x --tb=short` to fail fast; pin any randomness with `random.seed(42)`.

---

## Loop 2 — HTTP script / curl

**Best when**: the bug surfaces via an HTTP API and the server can be started locally.

```bash
# Start dev server
uv run uvicorn myapp.main:app --port 8000

# Reproduce the bug
curl -s -X POST http://localhost:8000/endpoint \
  -H 'Content-Type: application/json' \
  -d '{"field": "value"}' | python -m json.tool

# Or use httpx for richer assertions
uv run python scripts/repro_curl.py
```

**Tighten**: capture the exact response body and status code; diff against a known-good baseline:

```bash
curl -s ... > /tmp/actual.json
diff /tmp/expected.json /tmp/actual.json
```

---

## Loop 3 — CLI invocation with fixture

**Best when**: the bug manifests in a CLI tool or a script that transforms input to output.

```bash
# Save fixture
cat > /tmp/fixture.json << 'EOF'
{"key": "value"}
EOF

# Run and diff
uv run python -m myapp.cli process /tmp/fixture.json > /tmp/actual.txt
diff /tmp/expected.txt /tmp/actual.txt
echo "Exit: $?"
```

**Tighten**: lock the fixture to the minimal input found during symptom reduction; assert on specific lines, not whole-file diff.

---

## Loop 4 — Headless browser (Playwright)

**Best when**: the bug only manifests through a UI interaction (click, form submit, page navigation).

```python
# scripts/repro_ui.py
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:3000/path")
    page.fill("#input", "value")
    page.click("button[type=submit]")
    # Assert on the symptom
    assert page.locator(".error-message").is_visible(), "Expected error not shown"
    browser.close()
```

```bash
uv run python scripts/repro_ui.py
```

**Tighten**: use `page.wait_for_selector` not `time.sleep`; save a page capture to a temp file on assertion failure (Playwright's page-level capture call).

---

## Loop 5 — Replay a captured trace

**Best when**: the bug requires a real external payload (webhook, API callback, event) that is hard to synthesise.

```bash
# Capture once (e.g., from logs or a HAR export)
cat real_event.json

# Replay through the handler in isolation
uv run python scripts/replay_event.py real_event.json
```

```python
# scripts/replay_event.py
import json, sys
from myapp.handlers import handle_event

payload = json.load(open(sys.argv[1]))
result = handle_event(payload)
assert result["status"] == "ok", f"Unexpected: {result}"
```

**Tighten**: strip all irrelevant fields from `real_event.json` until the failure still triggers (minimise).

---

## Loop 6 — Throwaway harness

**Best when**: the bug requires multiple components but not the whole system.

```python
# scripts/harness_<ticket>.py
"""Minimal harness: service A + mock for B."""
from unittest.mock import MagicMock
from myapp.service_a import ServiceA

mock_b = MagicMock()
mock_b.fetch.return_value = {"data": "stub"}

service = ServiceA(dependency_b=mock_b)
result = service.process("trigger-input")
assert result["field"] == "expected", f"Got: {result}"
```

```bash
uv run python scripts/harness_<ticket>.py
```

**Tighten**: remove one mock/dep at a time and check the loop still goes red — keep only what is load-bearing.

---

## Loop 7 — Property / fuzz loop

**Best when**: the bug is "sometimes wrong output" with no obvious trigger.

```python
# scripts/fuzz_<ticket>.py
import random
from myapp.module import function_under_test

random.seed(42)  # reproducibility
failures = []
for i in range(1000):
    inp = random.choices(...)
    result = function_under_test(inp)
    if not invariant_holds(result):
        failures.append((inp, result))

assert not failures, f"Found {len(failures)} failures: {failures[:3]}"
```

```bash
uv run python scripts/fuzz_<ticket>.py
```

**Tighten**: once you find a failing input, minimise it (reduce length, simplify values) until the smallest trigger is known — then pivot to Loop 1 with that fixture.

---

## Loop 8 — Bisection harness

**Best when**: the bug appeared between two known commits (or dataset versions, or config states).

`git bisect` rewrites the worktree. Run it only on an already-authorized isolated checkout (disposable clone or worktree), never on the live tree. Adjacent bisect of two revisions uses the same isolated checkout — not `git show` of a single file on HEAD.

```bash
# Isolated checkout already at an authorized path (clone or worktree). Live tree stays put.
git -C /path/to/isolated-checkout bisect start
git -C /path/to/isolated-checkout bisect bad HEAD
git -C /path/to/isolated-checkout bisect good <last-known-good-sha>
git -C /path/to/isolated-checkout bisect run uv run pytest tests/test_regression_<ticket>.py -x -q
```

The script must exit 0 for "good" and non-zero for "bad". `git bisect run` walks commits until it finds the first bad one. Do not `git stash`, `git checkout --`, or `git restore` the live tree to make that walk.

**Tighten**: ensure the test is self-contained (no external state mutation) so it can run cleanly at any commit of that isolated checkout.

---

## Loop 9 — Differential loop

**Best when**: the bug is "version A returns X but version B returns Y" — regression between configs, deploys, or library versions.

```bash
# Interpreter/config differential (same tree, two runtimes)
uv run --python 3.11 python scripts/repro_fixture.py > /tmp/old.txt
uv run --python 3.12 python scripts/repro_fixture.py > /tmp/new.txt
diff /tmp/old.txt /tmp/new.txt
```

`git show <tag>:<path>` is only for a self-contained fixture or byte inspection. If the fixture imports product code, both sides still load the CURRENT tree's modules (or the tmp file loses the relative import) and the diff hides the regression.

```bash
# Byte inspection of a self-contained fixture (no product imports)
git show v1.2.0:scripts/repro_fixture.py > /tmp/repro_old.py
diff /tmp/repro_old.py scripts/repro_fixture.py
```

For behavior between two product revisions, run each revision in an already-existing isolated checkout that has that revision's code AND dependencies. No new framework, no checkout of the live tree, no auto-install.

```bash
uv run --directory /path/to/checkout-v1.2.0 python scripts/repro_fixture.py > /tmp/old.txt
uv run --directory /path/to/checkout-HEAD python scripts/repro_fixture.py > /tmp/new.txt
diff /tmp/old.txt /tmp/new.txt
```

Falsifier: a change only in the imported product module appears different on the two sides, while the live tree is unchanged.

Do not `git stash`, `git checkout`, or `git restore` the live working tree to compare versions.

**Tighten**: diff only the field that encodes the symptom — not full serialization — to avoid noise.

---

## Loop 10 — HITL script (last resort)

**Best when**: no automated path exists; a human must click or observe in a live environment.

Drive the human with the two-helper template at `scripts/hitl_loop_template.py` (skill root) instead of ad hoc `echo`/`read` — `step()` shows an instruction and waits for Enter, `capture()` asks a question and returns the answer, and the end of the run prints every captured value as `KEY=VALUE` for the agent to parse. Edit `run()` and nothing else:

```python
def run() -> dict[str, str]:
    step("Open http://localhost:3000/path and sign in.")
    errored = capture("Click 'Submit'. Did it throw an error? (y/n)")
    error_msg = capture("Paste the exact error message (or 'none'):")
    return {"ERRORED": errored, "ERROR_MSG": error_msg}
```

```bash
python -X utf8 scripts/hitl_loop_template.py
```

It exits non-zero and captures nothing on EOF or a non-interactive stdin, so an agent that runs it unattended gets a clear abort rather than a block of empty answers that reads like real observations.

**Capture observations, never credentials.** Every captured value is exposed twice — echoed unmasked as the human types it, then printed again in the closing `KEY=VALUE` block, which is the copy you read and the copy that survives in their scrollback. A sign-in belongs in a `step`, as in the example above: a `step` collects nothing, so there is nothing to echo, print, or paste. As a backstop the closing block is redacted on the way out (auth headers, credential-named keys, common token shapes, URL credentials, PEM blocks) and says so when it fires, so a mask is never mistaken for what the human actually typed.

**Tighten**: capture timestamped output; after the human provides a repro, move toward Loop 4 (Playwright) to automate it.

---

## Choosing the right loop

| Symptom type | Start with |
|---|---|
| Function / domain rule broken | Loop 1 (failing test) |
| API endpoint returning wrong data | Loop 2 (curl / HTTP script) |
| CLI tool wrong output | Loop 3 (CLI + diff) |
| UI interaction broken | Loop 4 (Playwright) |
| Webhook / external event broken | Loop 5 (replay trace) |
| Multi-component interaction | Loop 6 (throwaway harness) |
| "Sometimes wrong" output | Loop 7 (fuzz loop) |
| Regression between commits | Loop 8 (bisection) |
| Regression between versions/configs | Loop 9 (differential) |
| No automated path possible | Loop 10 (HITL script) |

**Always prefer the loop highest on the list** (most automated, most deterministic). Descend only when a higher loop is genuinely unavailable.
