#!/usr/bin/env python3
"""Read-only kill-slop diff budget checker (Windows-safe).

Never modifies the working tree, index, or git config.

Exit codes:
  0  STATUS: OK (measured a real zero or in-budget diff)
  1  STATUS: OVER_BUDGET, SKIP or EMPTY_SCAN (cannot treat unknown as pass)
  2  usage error
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _git(args: list[str], cwd: Path) -> tuple[int, str]:
    try:
        p = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except FileNotFoundError:
        return 127, "git not available"
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="check_diff.py",
        description="Read-only kill-slop diff budget. Never writes to the repo.",
    )
    ap.add_argument("--max-files", type=int, default=5, help="Soft file budget (default: 5)")
    ap.add_argument("--base", default="HEAD", help="Git ref to diff against (default: HEAD)")
    ap.add_argument(
        "--cwd",
        default=".",
        help="Project being edited (default: current directory)",
    )
    ap.add_argument(
        "--path",
        default=None,
        help="If set, the path must exist and be readable or the scan fails (unknown, not OK)",
    )
    args = ap.parse_args(argv)

    if args.max_files < 0:
        print("--max-files must be a non-negative integer", file=sys.stderr)
        return 2

    cwd = Path(args.cwd).resolve()
    if args.path is not None:
        probe = Path(args.path)
        if not probe.exists():
            print("STATUS: EMPTY_SCAN")
            print(f"reason: --path {probe} does not exist")
            print("A checker that inspected zero items cannot pass.")
            return 1
        if not probe.is_dir() and not probe.is_file():
            print("STATUS: EMPTY_SCAN")
            print(f"reason: --path {probe} is not a readable file or directory")
            return 1

    rc, out = _git(["rev-parse", "--is-inside-work-tree"], cwd)
    if rc == 127:
        print("STATUS: SKIP")
        print("reason: git not available")
        print("A checker that could not scan cannot pass.")
        return 1
    if rc != 0 or "true" not in out.lower():
        print("STATUS: SKIP")
        print("reason: not a git repository")
        print("A checker that could not scan cannot pass.")
        return 1

    rc, _ = _git(["rev-parse", "--verify", args.base], cwd)
    if rc != 0:
        print("STATUS: SKIP")
        print(f"reason: base ref {args.base!r} not found")
        print("A checker that could not scan cannot pass.")
        return 1

    names: set[str] = set()
    for git_args in (
        ["diff", "--name-only", args.base],
        ["ls-files", "--others", "--exclude-standard"],
    ):
        rc, text = _git(git_args, cwd)
        if rc != 0:
            print("STATUS: SKIP")
            print(f"reason: git {' '.join(git_args)} failed")
            print("A checker that could not scan cannot pass.")
            return 1
        for line in text.splitlines():
            line = line.strip()
            if line:
                names.add(line.replace("\\", "/"))

    file_count = len(names)
    untracked = 0
    for f in names:
        rc, _ = _git(["ls-files", "--error-unmatch", "--", f], cwd)
        if rc != 0:
            untracked += 1

    add = 0
    delete = 0
    rc, text = _git(["diff", "--numstat", args.base], cwd)
    if rc != 0:
        print("STATUS: SKIP")
        print(f"reason: git diff --numstat {args.base} failed")
        print("A checker that could not scan cannot pass.")
        return 1
    for line in text.splitlines():
        parts = line.split("\t", 2)
        if len(parts) < 2:
            continue
        a, d = parts[0], parts[1]
        add += 0 if a == "-" else int(a or 0)
        delete += 0 if d == "-" else int(d or 0)

    print("kill-slop diff budget (read-only)")
    print(f"base: {args.base}")
    print(f"scope: working tree vs {args.base}")
    print(f"files_touched: {file_count}")
    print(f"files_untracked: {untracked}")
    print(f"lines_added: {add}")
    print(f"lines_deleted: {delete}")
    print("note: lines_added excludes untracked files")
    print(f"soft_max_files: {args.max_files}")
    print()

    if file_count == 0:
        print("STATUS: OK")
        print(f"No local changes vs {args.base} (measured zero).")
        return 0

    print("files:")
    for f in sorted(names):
        rc, _ = _git(["ls-files", "--error-unmatch", "--", f], cwd)
        kind = "untracked" if rc != 0 else "modified"
        print(f"  - [{kind}] {f}")
    print()

    if file_count > args.max_files:
        print("STATUS: OVER_BUDGET")
        print(
            "Action: shrink the plan — prefer editing existing files; "
            "drop drive-bys; do not add files that can be inlined."
        )
        return 1

    print("STATUS: OK")
    print(
        "Within soft file budget. Still apply kill-slop self-check "
        "(no junk comments, no unrequested deps, no architecture cosplay)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
