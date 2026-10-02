# Shell equivalents cheat sheet: PowerShell / Git Bash / Python file

Same operation, three vehicles. The **Python file** column is the portable answer whenever
the operation is non-trivial, needs structured data, or must run identically on another OS.

Assume PowerShell 7+ (`pwsh`). Assume the Python column lives in a `.py` file that starts with:

```python
from pathlib import Path
import json, os, subprocess, sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
```

---

## Files and directories

| Operation | PowerShell | Git Bash | Python file |
|---|---|---|---|
| List directory | `Get-ChildItem` / `ls` | `ls -la` | `list(Path(".").iterdir())` |
| List recursively | `Get-ChildItem -Recurse` | `find . -type f` | `Path(".").rglob("*")` |
| Read a file | `Get-Content f` | `cat f` | `Path("f").read_text(encoding="utf-8")` |
| First N lines | `Get-Content f -TotalCount N` | `head -n N f` | `f.read_text(encoding="utf-8").splitlines()[:N]` |
| Last N lines | `Get-Content f -Tail N` | `tail -n N f` | `...splitlines()[-N:]` |
| Write a file | `Set-Content f v -Encoding utf8` | `printf '%s' v > f` | `Path("f").write_text(v, encoding="utf-8")` |
| Append | `Add-Content f v` | `printf '%s' v >> f` | `open("f","a",encoding="utf-8").write(v)` |
| Create empty file | `if (-not (Test-Path f)) { New-Item -ItemType File f }` | `touch f` | `Path("f").touch()` |
| Make dirs (parents) | `New-Item -ItemType Directory -Force p` | `mkdir -p p` | `Path("p").mkdir(parents=True, exist_ok=True)` |
| Delete recursively | `Remove-Item -Recurse -Force p` | `rm -rf p` | `shutil.rmtree("p", ignore_errors=True)` |
| Copy tree | `Copy-Item a b -Recurse` | `cp -r a b` | `shutil.copytree("a","b")` |
| Move / rename | `Move-Item a b` | `mv a b` | `Path("a").rename("b")` |
| Exists? | `Test-Path p` | `[ -e p ]` | `Path("p").exists()` |
| Count lines | `(Get-Content f \| Measure-Object -Line).Lines` | `wc -l < f` | `sum(1 for _ in open("f",encoding="utf-8"))` |
| File size | `(Get-Item f).Length` | `stat -c%s f` | `Path("f").stat().st_size` |
| Symlink | `New-Item -ItemType SymbolicLink -Path l -Target t` | `ln -s t l` | `Path("l").symlink_to("t")` |
| Is a link? | `(Get-Item l).LinkType` | `[ -L l ]` | `Path("l").is_symlink()` |

> `New-Item -Force` on an **existing file truncates it**. Never use it as a `touch` substitute
> without the `Test-Path` guard shown above.

---

## Search

| Operation | PowerShell | Git Bash | Python file |
|---|---|---|---|
| Grep text | `Select-String -Pattern p -Path f` | `grep -n p f` | `re.finditer(p, text)` |
| Grep recursively | `Get-ChildItem -Recurse \| Select-String p` | `grep -rn p .` | walk + `re` |
| Find by name | `Get-ChildItem -Recurse -Filter "*.py"` | `find . -name "*.py"` | `Path(".").rglob("*.py")` |
| Case-insensitive | `Select-String -Pattern p` (default) | `grep -i p f` | `re.I` |

Prefer a dedicated search tool (`rg`, or the agent's own search tool) over all three when
available: it is faster and does not cross a quoting boundary.

---

## Process and environment

| Operation | PowerShell | Git Bash | Python file |
|---|---|---|---|
| Read env var | `$env:NAME` | `$NAME` | `os.environ.get("NAME")` |
| Set env var (session) | `$env:NAME = "v"` | `export NAME=v` | `os.environ["NAME"] = "v"` |
| Prefix one command | `$env:V='x'; cmd` | `V=x cmd` | `subprocess.run(cmd, env={**os.environ,"V":"x"})` |
| Locate executable | `(Get-Command n).Source` | `which n` | `shutil.which("n")` |
| Run and capture | `$o = cmd 2>&1` | `o=$(cmd 2>&1)` | `subprocess.run([...], capture_output=True, text=True, encoding="utf-8")` |
| Exit code | `$LASTEXITCODE` | `$?` | `proc.returncode` |
| Discard stderr | `cmd 2>$null` | `cmd 2>/dev/null` | `stderr=subprocess.DEVNULL` |
| Chain on success | `cmd1 && cmd2` | `cmd1 && cmd2` | `if a.returncode == 0: ...` |
| Sequential regardless | `cmd1; cmd2` | `cmd1; cmd2` | two statements |
| Is PID N alive? | `[bool](Get-CimInstance Win32_Process -Filter "ProcessId = $n")` | `tasklist //FI "PID eq $n" //NH \| grep -q $n` | `OpenProcess` + `WaitForSingleObject` (below) — **never `os.kill(pid, 0)`** |

`subprocess.run` with a **list** argument (not a string, and no `shell=True`) is the only form
with no quoting boundary at all. Prefer it for anything an agent generates.

### `os.kill(pid, 0)` is not a liveness probe on Windows

On POSIX, signal `0` is the null signal: delivery is checked, nothing is sent, and a dead PID
raises `ProcessLookupError`. That is why the idiom exists. **Windows has no null signal**, and
CPython reuses the same two low integers for something else entirely: `signal.CTRL_C_EVENT == 0`
and `signal.CTRL_BREAK_EVENT == 1`, so those values are routed to a console-control event aimed at
a process *group*, and every other value becomes an unconditional `TerminateProcess`.

Measured on CPython 3.13, `sys.platform == "win32"`:

| Call | Target | Caller | Verdict |
|---|---|---|---|
| `os.kill(live_pid, 0)` | survives | survives | returns normally — tells you nothing |
| `os.kill(dead_pid, 0)` | already gone | survives | **returns normally — the probe reports ALIVE for a reaped PID** |
| `os.kill(999999, 0)` | never existed | survives | raises `OSError: [WinError 87]` |
| `os.kill(live_pid, 1)` | observed alive after | **killed the calling interpreter** | `CTRL_BREAK_EVENT` hit the console group |
| `os.kill(live_pid, 15)` | terminated, `returncode == 15` | survives | `TerminateProcess`, exit code = the signal number |

Read rows 2 and 3 together: the idiom raises for a *bogus* PID and stays silent for a *recently
dead* one, so it passes a smoke test and then lies in production. It is a fail-open probe — the
answer is always "alive" in exactly the case you were asking about — and rows 4 and 5 mean a
"probe" can take down the caller or the target.

Two probes that actually answer the question:

```python
import ctypes, ctypes.wintypes as w
SYNCHRONIZE, WAIT_TIMEOUT = 0x00100000, 0x00000102
_k32 = ctypes.WinDLL("kernel32", use_last_error=True)
_k32.OpenProcess.restype = w.HANDLE
_k32.OpenProcess.argtypes = (w.DWORD, w.BOOL, w.DWORD)

def alive(pid: int) -> bool:
    h = _k32.OpenProcess(SYNCHRONIZE, False, pid)   # NULL when the PID is gone
    if not h:
        return False
    try:
        return _k32.WaitForSingleObject(h, 0) == WAIT_TIMEOUT   # still running
    finally:
        _k32.CloseHandle(h)
```

```powershell
# NOT $pid -- see the warning below.
[bool](Get-CimInstance Win32_Process -Filter "ProcessId = $targetPid" -ErrorAction SilentlyContinue)
```

Both were checked against a live child, a reaped child, and a nonexistent PID, and returned
`True/False/False`.

Two things that turn either probe back into a fail-open one:

- **`$PID` is a PowerShell automatic variable holding the CURRENT process id.** Name your variable
  `$pid` and the filter silently reads the shell's own id, so the probe returns `True` forever — a
  green light that cannot turn red, which is the very failure this section exists to prevent.
  Verified: `Get-CimInstance Win32_Process -Filter "ProcessId = $PID"` returns `True` in any live
  session. Use `$targetPid`, or any name that is not an automatic.
- **`tasklist` writes in the console OEM code page**, so decode its output explicitly (`cp850` on
  this host) rather than with `text=True`. Decoding it as UTF-8 raises `UnicodeDecodeError` and
  turns the probe into a crash — the cp1252 family from this skill's main page, arriving through
  the probe you added to be careful.

**PID reuse remains, on every platform.** Windows recycles PIDs aggressively, so "a process with
this PID exists" is never "my process is still running". When it matters, hold the handle (or the
`Popen` object) you got at spawn time, or check identity — start time, image name — alongside the
PID.

---

## Structured data

| Operation | PowerShell | Git Bash | Python file |
|---|---|---|---|
| Parse JSON | `Get-Content f \| ConvertFrom-Json` | `jq . f` | `json.loads(Path("f").read_text(encoding="utf-8"))` |
| Emit JSON | `$o \| ConvertTo-Json -Depth 10` | `jq -n ...` | `json.dumps(o, ensure_ascii=False, indent=2)` |
| Filter rows | `Where-Object { $_.k -eq "v" }` | `jq 'select(.k=="v")'` | list comprehension |
| Select fields | `Select-Object a,b` | `jq '{a,b}'` | dict comprehension |

`ensure_ascii=False` keeps accented characters readable in the output instead of escaping
them to `\uXXXX`. Pair it with an explicit UTF-8 write.

---

## Multi-line strings passed to a native command

A commit message, a PR body, a release note and a board post are **data**. The moment one is
typed inline into a double-quoted argument, a shell parses it, and the two shells damage the same
text in two different ways. Measured, one session, same string in both:

```text
intended   fix(auth): revert the `basename $PWD` regression; $HOME untouched
Git Bash   fix(auth): revert the scratchpad regression; $HOME untouched
PowerShell fix(auth): revert the asename regression; C:\Users\alex untouched
```

Git Bash ran `basename $PWD` as a command substitution and **injected its output** into the
message. PowerShell read the backtick as its escape character, **silently deleted the `b`**, and
expanded `$HOME`. Neither errored. Neither is recoverable by escaping harder, because the two
shells disagree about which character is dangerous.

**So write the message to a file, or hold it in a variable, and hand it over as one argv element.**
The portable form has no shell in it at all:

```python
msg = Path("msg.txt").read_text(encoding="utf-8")
subprocess.run(["git", "commit", "-m", msg], check=True)   # list, no shell=True
```

If the payload really must be inline, quote it so the shell cannot reach inside — and note that
these two forms are not interchangeable, they are each shell's *only* safe spelling:

```powershell
# PowerShell: SINGLE-quoted here-string. $ and backticks stay literal.
# The closing '@ MUST be at column 0 — indentation is a parse error.
git commit -m @'
Subject line.

Body with $variables and `backticks` preserved verbatim.
'@
```

```bash
# Git Bash: QUOTED heredoc. The quotes on 'EOF' are what disable expansion —
# unquoted <<EOF expands $var and backticks inside the body exactly like case A above.
git commit -m "$(cat <<'EOF'
Subject line.

Body with $variables and `backticks` preserved verbatim.
EOF
)"
```

Both forms were verified to round-trip backticks, `$`, apostrophes and accented characters
unchanged, and Git Bash was verified to hand embedded quotes, trailing backslashes and diacritics
to a native `.exe` intact. What the heredoc form still costs you is trailing newlines — command
substitution strips them, always. The argv-list form is the only one with no parsing step at all,
which is why it is the default and these two are the exceptions.

---

## Operations that do NOT translate

| Unix idiom | Why it fails on Windows shells | Do instead |
|---|---|---|
| `2>/dev/null` | Creates a literal file named `null` | `2>$null` (PowerShell), `NUL` (cmd) |
| `chmod` / `chown` | No POSIX permission model | `icacls` only if ACLs are genuinely required |
| `if [ -f x ]` | Not PowerShell syntax — parse error | `if (Test-Path x)` |
| `for x in *` | Not PowerShell syntax — parse error | `foreach ($x in Get-ChildItem)` |
| `` `cmd` `` substitution | Backtick is PowerShell's *escape* character | `$(cmd)` |
| `ln -s` without elevation | Requires admin or Developer Mode | Enable Developer Mode, or use a junction |
| `head` / `tail` / `which` / `wc` | Do not exist as PowerShell cmdlets | See the tables above |
| `sudo` | No equivalent | Launch an elevated shell explicitly |

---

## Choosing quickly

```text
Is it one short command with no tricky quoting?      -> run it directly
Does it need a loop, a conditional, or JSON?         -> write a .py file
Is it Windows host administration?                   -> PowerShell (.ps1 if non-trivial)
Is it heavy log/pipeline I/O?                        -> PowerShell or a .py file, never Git Bash
Does the payload contain both quote styles?          -> write a file; there is no portable inline form
Will you run it more than twice?                     -> write a file
```
