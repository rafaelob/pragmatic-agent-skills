# The encoding fix ladder

Five ways to stop `UnicodeEncodeError: 'charmap' codec can't encode character` on Windows,
ordered by how cheap and how robust each one is. **Apply one.** Stacking all five hides which
layer was actually broken and makes the next failure harder to diagnose.

## Diagnose first: is it stdout, or is it a file?

They are different bugs with different fixes, and the traceback tells you which:

- Traceback ends in a `print(...)` / logging call -> **console encoding**. Use this ladder.
- Traceback ends in `write`, `write_text`, `open(...).write`, `csv.writer` -> **file encoding**.
  The ladder does not apply; the fix is to name `encoding="utf-8"` at the call site, always.
- Traceback ends in `read`, `read_text`, `json.load` -> **input decoding**. Same fix on the read
  side, plus `errors="replace"` if the input is genuinely dirty and you want to survive it.

A process can have all three. Fix them separately.

---

## Rung 1 — `PYTHONIOENCODING=utf-8` in the environment

```powershell
$env:PYTHONIOENCODING = "utf-8"
```
```bash
export PYTHONIOENCODING=utf-8
```

**Covers:** every Python process launched from that shell, including subprocesses, without
touching a single line of code.

**Use when:** you control the session or the harness — an agent shell, a developer machine
default, a CI job's env block.

**Limits:** invisible to anyone who did not set it. A script that only works because of an
ambient environment variable is a script that fails on someone else's machine with no clue why.
Never rely on this for code you commit and hand to others.

---

## Rung 2 — `python -X utf8 script.py`

**Covers:** stdout/stderr **and** the default encoding for `open()` in that process — UTF-8 Mode
changes the filesystem-encoding defaults, not just the console.

**Use when:** you control the command line but not the environment, and you also want file I/O
defaults corrected in one move.

**Limits:** per-invocation; forgotten on the next call. Because it also changes file defaults, a
script that *depends* on it behaves differently when run without it — which is a subtler failure
than crashing. Prefer explicit `encoding=` at every file call regardless.

Equivalent: `PYTHONUTF8=1` as an environment variable.

---

## Rung 3 — `sys.stdout.reconfigure(...)` inside the script

```python
import sys
for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
```

**Covers:** this process's console output, wherever and however it is launched.

**Use when:** the script is committed, shared, or run by a harness you do not control. This is
the correct rung for anything durable — it travels with the file.

**Why the `try/except`:** `reconfigure` exists on `TextIOWrapper`, but `sys.stdout` is not always
one (redirected streams, embedded interpreters, some notebook and test-capture contexts). An
unguarded call turns a printing bug into a startup crash — the fix becoming the failure.

**Why `errors="replace"`:** a diagnostic that survives with a `?` in place of one glyph is worth
more than a diagnostic that dies. Use `errors="strict"` only when correct output is the point.

Do `sys.stderr` too. Tracebacks print there, and a traceback that itself raises
`UnicodeEncodeError` is the worst version of this bug: the real error is destroyed by the
error path.

---

## Rung 4 — `chcp 65001`

```powershell
chcp 65001
```

**Covers:** the console code page for everything run in that window, in any language, not just
Python.

**Use when:** the offending program is not yours to change — a third-party CLI, a compiled tool,
a vendored script.

**Limits:** blunt and session-wide. Some programs read the active code page and change behaviour;
some legacy tools misbehave under 65001. It does not survive a new window. Treat it as a
workaround for foreign binaries, not as your project's answer.

---

## Rung 5 — ASCII-only output

```python
print("step 1 -> step 2")      # not the arrow glyph
print("delta ~= 0.073")        # not the approximation sign
print("-4.49pp")               # ASCII hyphen-minus, not the minus sign
```

**Covers:** everything, everywhere, with zero configuration and zero dependencies.

**Use when:** the output is a throwaway diagnostic. Which is precisely the case that generates
almost all of these crashes: a temporary script printing progress with typographic symbols it
never needed.

**This is the right default for temporary scripts.** The typographic arrow bought nothing and
cost the run. Reserve non-ASCII output for deliverables where the character carries meaning
(names, natural-language text, currency, units), and fix those with rung 3.

**Never** apply this to *data*. Stripping accents from names, addresses, or legal text to avoid a
console crash corrupts the payload to fix the display. Diacritics in data are correctness.

---

## The rule that sits outside the ladder

**Files are always explicit UTF-8, no matter which rung you chose.**

```python
Path(p).read_text(encoding="utf-8")
Path(p).write_text(s, encoding="utf-8")
open(p, "w", encoding="utf-8", newline="")
json.dumps(obj, ensure_ascii=False)
subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
```

Console encoding is a display concern and a crash you can see. File encoding is a data concern
and a corruption you cannot — mojibake written today surfaces months later, after the source is
gone. `ensure_ascii=False` on JSON and an explicit `encoding=` on `subprocess` capture are the
two most commonly forgotten.

---

## Quick reference

| Situation | Rung |
|---|---|
| Agent session default, harness-wide | 1 — `PYTHONIOENCODING` |
| One-off invocation, want file defaults too | 2 — `python -X utf8` |
| Committed script, shared, or CI-embedded | 3 — `reconfigure` in-file |
| Third-party binary you cannot modify | 4 — `chcp 65001` |
| Throwaway diagnostic | 5 — ASCII output |
| Any file read or write, ever | Explicit `encoding="utf-8"` — not optional |
