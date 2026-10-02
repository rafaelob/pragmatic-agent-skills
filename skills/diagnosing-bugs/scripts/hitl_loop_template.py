#!/usr/bin/env python3
"""Human-in-the-loop reproduction loop (Loop 10 -- last resort).

Adapted from mattpocock/skills (MIT), `diagnosing-bugs/scripts/hitl-loop.template.sh`.
Ported from bash to Python because this catalog distributes to Windows as well as
POSIX, and `input()` behaves identically on cmd, PowerShell, and any POSIX shell,
whereas the bash original needs Git Bash to run on Windows at all.

Copy this file, edit the steps in `run()`, and run it. The agent runs the script;
the human follows the prompts in their terminal.

Usage:
    python hitl_loop_template.py

Two helpers:
    step("<instruction>")          -> show instruction, wait for Enter
    capture("<question>")          -> show question, return the typed response

**Capture observations, never credentials.** Whatever `capture()` collects is
exposed twice: the terminal echoes it unmasked as the human types it, and the
final summary prints it as `KEY=VALUE` -- which is the copy the agent reads, and
the copy that survives in scrollback and in whatever transcript the block is
pasted into. So leave signing in to the human as a `step`: a `step` collects no
value, so there is nothing to echo, print, or paste.

As a backstop, the summary passes every value through `redact()` before printing
it (see `_SECRET_PATTERNS`). That filter is a net under the rule above, never a
substitute for it -- it only catches secrets it can recognise.
"""

import argparse
import re
import sys

REDACTED = "<REDACTED>"

# Narrow, label-anchored patterns. They fire on text that is a credential by
# construction, not on anything that merely looks random: a commit SHA, a UUID,
# a request id or a stack frame must survive, because that is what the agent
# diagnoses from. Labelled values are only redacted from 12 characters up, so
# "token: expired" and "token: malformed" stay readable.
_SECRET_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    # Authorization header -- the scheme is kept, since the wrong scheme is a
    # real bug cause; the credential after it never is.
    (
        re.compile(
            r"(?i)(?<![A-Za-z0-9])((?:[A-Za-z0-9]+[_-])*(?:proxy-)?authorization"
            r"[\"']?\s*[:=]\s*[\"']?)((?:bearer|basic|token|digest)\s+)?[^\s\"',;}\]]+"
        ),
        rf"\1\2{REDACTED}",
    ),
    # key=value / key: value for credential-named keys, quoted (JSON) or bare,
    # with or without a prefix (`APP_TOKEN`, `DB_PASSWORD`, `MY_APP_API_KEY`).
    (
        re.compile(
            r"(?i)(?<![A-Za-z0-9])((?:[A-Za-z0-9]+[_-])*"
            r"(?:api[-_]?key|apikey|access[-_]?token|refresh[-_]?token|"
            r"client[-_]?secret|private[-_]?key|passphrase|password|secret|token)"
            r"[\"']?\s*[:=]\s*)[\"']?[^\s\"',;}\]]{12,}"
        ),
        rf"\1{REDACTED}",
    ),
    # Credentials inside a URL -- connection strings show up in stack traces.
    (re.compile(r"(?i)\b([a-z][a-z0-9+.\-]*://)[^\s/:@]+:[^\s/@]+@"), rf"\1{REDACTED}@"),
    # Token shapes that carry no label at all.
    (re.compile(r"\beyJ[A-Za-z0-9_-]{6,}\.[A-Za-z0-9_-]{6,}\.[A-Za-z0-9_-]*"), REDACTED),
    (re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"), REDACTED),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"), REDACTED),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"), REDACTED),
    (
        re.compile(r"(?s)-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----"),
        REDACTED,
    ),
)


def redact(value: str) -> str:
    """Replace secret-shaped substrings with `<REDACTED>`, keeping the rest intact.

    The observation still reaches the agent -- only the credential inside it is
    swapped out. Widen `_SECRET_PATTERNS` for a credential format this bug
    happens to involve; do not widen it into a reason to capture secrets.
    """
    for pattern, replacement in _SECRET_PATTERNS:
        value = pattern.sub(replacement, value)
    return value


def step(instruction: str) -> None:
    """Show an instruction and block until the human presses Enter.

    Collects nothing, so nothing is echoed or printed. Anything secret --
    signing in, entering a token, unlocking a vault -- belongs here.
    """
    print(f"\n>>> {instruction}")
    input("    [Enter when done] ")


def capture(question: str) -> str:
    """Ask a question and return the human's answer.

    The answer is echoed unmasked as it is typed and printed again in the final
    summary, so ask for an **observation** -- an error message, a status, what
    appeared on screen. Never ask for a password, token, or any other
    credential: use `step` for those.
    """
    print(f"\n>>> {question}")
    return input("    > ").strip()


def run() -> dict[str, str]:
    """Edit this function. Return whatever the agent needs back as KEY=VALUE."""
    step(
        "Reproduce the setup described by the user "
        "(open the app, sign in, load the fixture, run the flow)."
    )

    observed = capture(
        "Describe exactly what happened "
        "(error message, wrong output, or 'matches expectation'):"
    )

    return {"OBSERVED": observed}


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Human-in-the-loop reproduction loop (Loop 10 -- last resort). "
            "Copy this file, edit the steps in run(), then run it: the agent "
            "runs the script and the human follows the prompts in their "
            "terminal. Takes no arguments; run with no flags to start."
        ),
    )
    return parser.parse_args(argv)


def main() -> int:
    _parse_args()
    try:
        captured = run()
    except (EOFError, KeyboardInterrupt):
        # Non-interactive stdin or an aborted run: say so instead of emitting a
        # half-empty KEY=VALUE block the agent would read as real observations.
        print("\n\nAborted before capturing anything -- no results to report.")
        return 1

    masked: list[str] = []
    print("\n--- Captured ---")
    for key, value in captured.items():
        safe = redact(value)
        if safe != value:
            masked.append(key)
        print(f"{key}={safe}")

    if masked:
        # Distinguish a mask this script applied from a literal the human typed:
        # otherwise the agent cannot tell a hidden value from an absent one.
        print(
            f"\n# {REDACTED} above was written by this script, not typed by the human "
            f"({', '.join(masked)}). If it swallowed something the diagnosis needs, "
            "describe that part in words instead of pasting it."
        )

    print("\nPaste the block above back to the agent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
