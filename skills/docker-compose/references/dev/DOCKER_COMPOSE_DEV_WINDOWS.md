# Docker Compose Dev Workflow on Windows -- Reference

> Freshness disclaimer: verified against Docker Desktop 4.x and Docker Compose V2 as of early 2026. Docker evolves rapidly; always cross-check with the official docs linked below.

## Official documentation

- Docker Desktop WSL2 backend: https://docs.docker.com/desktop/wsl/
- Docker Compose file reference: https://docs.docker.com/compose/compose-file/
- Compose Watch (develop section): https://docs.docker.com/compose/how-tos/file-watch/
- Dev Containers specification: https://containers.dev/implementors/spec/
- VS Code Dev Containers: https://code.visualstudio.com/docs/devcontainers/containers

## WSL2 filesystem performance

Source code location determines I/O performance:

| Location | Path example | Performance | Notes |
|----------|-------------|-------------|-------|
| WSL2 native | `/home/user/project` | Native Linux speed | Recommended for dev |
| Windows via WSL | `/mnt/c/Users/.../project` | 3-10x slower | 9P filesystem bridge |
| Windows native | `C:\Users\...\project` | N/A for containers | Must go through WSL |

Rule: keep source inside the WSL2 distro filesystem for fast file watches and builds.

## Compose Watch configuration

```yaml
services:
  api:
    build: .
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: ./requirements.txt
```

- `sync`: copies changed files into the running container (hot reload).
- `rebuild`: triggers a full rebuild when dependency files change.
- `sync+restart`: syncs files and restarts the service process.

Start with: `docker compose watch` (or `docker compose up --watch`).

## Volume patterns for Windows

```yaml
services:
  web:
    volumes:
      - ./src:/app/src                    # Bind mount: source only
      - node_modules:/app/node_modules    # Named volume: deps
      - build_cache:/app/.next            # Named volume: build output

volumes:
  node_modules:
  build_cache:
```

Named volumes for dependency directories prevent cross-OS filesystem penalties and avoid permission conflicts.

## Line endings (.gitattributes)

```gitattributes
* text=auto eol=lf
*.sh text eol=lf
*.bat text eol=crlf
*.ps1 text eol=crlf
*.png binary
*.jpg binary
```

This ensures shell scripts and config files use LF inside containers regardless of Windows checkout settings.

## Debug port exposure (Compose override)

Starting an override from scratch? `assets/dev/compose.dev.override.yml` in this skill is
a fuller starting point -- bind mount, `LOG_LEVEL=debug`, published port and a health check
-- to copy and edit. It is an example to adapt, never a file to include as-is. The snippet
below is the debugger-attach part on its own.

```yaml
# compose.override.yaml (dev only)
services:
  api:
    command: ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "-m", "uvicorn", "main:app", "--host", "0.0.0.0"]
    ports:
      - "5678:5678"
  web:
    command: ["node", "--inspect=0.0.0.0:9229", "server.js"]
    ports:
      - "9229:9229"
```

## Dev container (devcontainer.json) example

```json
{
  "name": "Project Dev",
  "dockerComposeFile": ["../compose.yaml", "../compose.override.yaml"],
  "service": "api",
  "workspaceFolder": "/app",
  "customizations": {
    "vscode": {
      "extensions": ["ms-python.python", "ms-python.debugpy"]
    }
  },
  "postCreateCommand": "pip install -e '.[dev]'",
  "forwardPorts": [8000, 5678]
}
```

## Common troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Slow hot reload (>5s) | Source on NTFS via /mnt/c | Move source to WSL2 native FS |
| `\r: not found` in shell scripts | Windows CRLF line endings | Add `.gitattributes` with `eol=lf` |
| Permission denied on bind mount | Windows 777 permissions | Use `chmod` in Dockerfile, run as specific UID |
| Container can't reach host DB | Using `localhost` | Use `host.docker.internal` |
| Port already in use | Host port conflict | Change mapping in `.env` or stop conflicting process |
| Node modules mismatch | Bind-mounting node_modules | Use named volume for node_modules |
| `docker` commands hang, no output, no error | Engine/control-plane unresponsive | Recovery ladder below -- do **not** start with `docker system prune -a` |

## Hung engine recovery -- exact commands and official wording

Every quote below was read at the vendor's own documentation on **2026-07-29**. Work down the
ladder and stop at the first rung that brings the engine back; each rung is cheaper to undo than
the next.

### 1. Localise the fault

```powershell
docker version
```

Reports client and server separately. A client that answers while the server hangs tells you
immediately that the engine, not the CLI or one command, is the problem.

### 2. Gather diagnostics BEFORE restarting

A restart destroys the evidence. Docker documents the diagnostics binary at these exact paths
(source: [Docker Desktop troubleshooting](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/)):

```powershell
# All-user install
& "C:\Program Files\Docker\Docker\resources\com.docker.diagnose.exe" gather -upload

# Per-user install
& "$env:LOCALAPPDATA\Programs\DockerDesktop\resources\com.docker.diagnose.exe" gather -upload
```

The Docker Desktop CLI equivalent documented on the same page:

```powershell
docker desktop diagnose
```

### 3. Restart Docker Desktop

The first remedy listed in Docker's own troubleshooting menu, alongside "Reset Kubernetes
cluster", "Clean / Purge data" and "Reset to factory defaults".

### 4. Restart the WSL 2 backend

```powershell
wsl --list --verbose      # check what else is running FIRST -- all of it will die
wsl --shutdown
```

Microsoft documents `wsl --shutdown` as: "Immediately terminates all running distributions and the
WSL 2 lightweight utility virtual machine. This command may be necessary in instances that require
you to restart the WSL 2 virtual machine environment"
([WSL basic commands](https://learn.microsoft.com/en-us/windows/wsl/basic-commands)).

Docker Desktop's WSL 2 backend runs inside that VM, so this restarts the substrate beneath the
engine. Note that Docker's own troubleshooting page does **not** mention this step -- it is
attributed to Microsoft's WSL documentation, not to Docker.

### 5. Check disk pressure

A full disk presents as a hung engine. Check free space on the drive holding the WSL virtual disks.

Microsoft documents the WSL VHD's default maximum size and how to **expand** it
([WSL disk space](https://learn.microsoft.com/en-us/windows/wsl/disk-space)):

```powershell
wsl --manage <distribution name> --resize <size>
```

Reclamation is documented far less well than growth. The mechanism found in official material is a
configuration setting, not a command -- `sparseVhd`, described as "When set to `true`, any newly
created VHD will be set to sparse automatically", listed under the `[experimental]` section of
[.wslconfig](https://learn.microsoft.com/en-us/windows/wsl/wsl-config). It applies to **newly
created** VHDs, so it is a preventative setting rather than a fix for a disk that is already full.
Treat freeing space as a deliberate, planned operation.

### 6. Destructive options -- last, and in Docker's own order

- **Clean / Purge data** -- "This option resets all Docker data without a reset to factory
  defaults." Warning on the same page: "Selecting this option results in the loss of existing
  settings."
- **Reset to factory defaults** -- returns Docker Desktop to "their initial state, the same as when
  Docker Desktop was first installed."

**Back up named volumes before either.** Database data lives in them and a purge takes it.

### Why `docker system prune -a` is the wrong first step

Docker's reference for [`system prune`](https://docs.docker.com/engine/reference/commandline/system_prune/)
states the command removes:

> "all stopped containers", "all networks not used by at least one container", "all anonymous
> volumes not used by at least one container", "all images without at least one container
> associated to them", "all build cache"

With `-a` that means **all unused images, not merely dangling ones**. A hung engine is a
control-plane fault: deleting images does not address it, and the rebuild cost is paid for nothing.
