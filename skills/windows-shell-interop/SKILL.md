---
name: windows-shell-interop
description: "Use for UnicodeEncodeError, console mojibake (cp1252), PowerShell 5.1 vs 7, or a path/quoting trap across PowerShell, Git Bash, cmd and Windows paths. Not a Linux-only script. Compose volumes -> docker-compose."
license: Apache-2.0
metadata:
  author: coding-agent
  version: 1.6.0
  category: infrastructure
  subcategory: developer-environment
  vendor: universal
  lifecycle: active
  coding_agent: true
  audience: developer
  output_format: markdown
  modality: text
  tags:
  - windows
  - shell
  - powershell
  - git-bash
  - cmd
  - encoding
  - utf-8
  - cp1252
  - unicodeencodeerror
  - quoting
  - escaping
  - here-string
  - exit-code
  - ntfs
  - junction
  - symlink
  - long-path
  - cross-platform
  - developer-environment
---

# Resolve the execution boundary first

Identify the interpreter, working directory, filesystem and process domain: PowerShell, cmd, Git Bash, WSL or container. Do not pass a Windows path to a Linux tool as though it were a Linux path. Shared visibility of files is not shared process, credential, lock or dependency state.

Prefer native Windows tooling over WSL. Where a project's own scripts still run in WSL, one command name can resolve to two programs: inside WSL, `pwsh` is the distro's Linux PowerShell and `pwsh.exe` is Windows PowerShell 7 through interop. On Windows itself, PowerShell 7 may be a Microsoft Store install reached only through an alias in `%LOCALAPPDATA%\Microsoft\WindowsApps`, with no `C:\Program Files\PowerShell\7` — probe with `Get-Command pwsh`, never a guessed install path. A Windows script that drives Windows tools runs as `pwsh.exe -NoProfile -File <script>` with a Windows-style `-File` path (`wslpath -w` from a Linux absolute path). A Windows SDK executed by a Linux interpreter over a `/mnt/*` path reads through 9P: measured minutes per call, not a universal SLA — do not run it that way for anything latency-sensitive.

Prefer native file operations or direct argv. For complicated shell logic, use an owned script with an explicit target rather than nested quoting. Keep file encoding explicit where needed and inspect pipe/console behavior instead of assuming one encoding for every Windows process: a Python script run bare on Windows inherits the console's code page (often cp1252), so `UnicodeEncodeError` and mojibake on non-ASCII output are console-encoding symptoms, not a broken string — run it as `python -X utf8 script.py` instead of `python script.py`.

Preserve the actual child exit code before formatting output. Catch only an expected condition that has a valid recovery; file absence and access denied are different. Do not use empty catch blocks, trailing successful commands or shell pipelines to conceal failure.

## Traps measured on this kind of host
- Git Bash (MSYS) rewrites an argument that starts with `/` into a Windows path: `tasklist /FI ...` and a value like `/root/x` arrive as `C:/Program Files/Git/...`, and the command fails or writes the wrong value quietly. Run Windows tools from PowerShell, or prefix that one command with `MSYS_NO_PATHCONV=1`, and read the result back.
- Stopping a shell (a tool timeout, a task stop, `timeout N` in Git Bash) does not stop the processes it started: a dev server keeps its port. Record the PID of what you launched, confirm it is still yours (same process start time), stop its tree (`taskkill /PID <pid> /T /F`), then confirm the port is free (`Get-NetTCPConnection -LocalPort <n>`). Never kill by port or name alone: that process may belong to someone else.
- Text with backslash escapes or non-ASCII goes into a file through the runtime's file-writing tool, not a heredoc or `echo`: the shell layer may rewrite both.

Read `references/encoding_fix_ladder.md` when a `UnicodeEncodeError` or mojibake needs the cheapest robust fix, ordered by cost; read `references/shell_equivalents_cheatsheet.md` when the same operation needs an equivalent PowerShell, Git Bash and Python-file spelling.

## Test the relevant portability contract
Reproduce the actual command with the path or encoding that failed. For reusable interop code, include the applicable spaces, Unicode, failure exit and path-domain negative case. Do not build an exhaustive cross-product of all shells for a one-time read command. Do not claim Windows behavior from a Linux-only test.

Preserve reparse points and unknown ownership; keep Windows and Linux dependency environments separate. No new daemon, global shell configuration or dependency installation merely to complete a local task. Remove only owned temporary artifacts and stop when the failing boundary works or its precise unsupported condition is reported.
