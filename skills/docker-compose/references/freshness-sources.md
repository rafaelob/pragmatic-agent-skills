# Docker Compose: Verified Authoritative Sources

> Reference for the `docker-compose` skill.

Canonical upstream documentation links for Docker Compose, BuildKit/buildx, and
related tooling. Self-contained: use this list to verify perishable facts
(`develop.watch`, profiles, `deploy.resources`, `security_opt`, cache backends,
WSL2/VirtioFS behavior) against current Docker documentation.

Verified 2026-06-01:

- Compose V2 (plugin) overview: https://docs.docker.com/compose/
- Compose file reference: https://docs.docker.com/reference/compose-file/
- Compose Specification (canonical / upstream schema): https://github.com/compose-spec/compose-spec
- `develop.watch` (file sync + rebuild): https://docs.docker.com/compose/how-tos/file-watch/
- Compose profiles: https://docs.docker.com/compose/how-tos/profiles/
- Docker Desktop WSL2 backend: https://docs.docker.com/desktop/features/wsl/
- Docker Desktop VirtioFS on macOS: https://docs.docker.com/desktop/settings-and-maintenance/settings/#virtiofs
- BuildKit / buildx (multi-platform, cache mounts): https://docs.docker.com/build/buildkit/ and https://docs.docker.com/reference/cli/docker/buildx/
- BuildKit multi-stage builds + cache mounts: https://docs.docker.com/build/building/multi-stage/
- BuildKit cache optimization (`RUN --mount=type=cache`, instruction ordering): https://docs.docker.com/build/cache/optimize/
- CI external build-cache backend (`--cache-to/--cache-from type=gha,mode=max`): https://docs.docker.com/build/cache/backends/gha/
- uv in Docker (official multi-stage pattern, `UV_COMPILE_BYTECODE`, `uv sync --locked`): https://docs.astral.sh/uv/guides/integration/docker/
- VS Code Dev Containers: https://code.visualstudio.com/docs/devcontainers/containers
- debugpy (Python remote debug): https://github.com/microsoft/debugpy
- Delve (Go remote debug): https://github.com/go-delve/delve
- `deploy.resources` (limits/reservations): https://docs.docker.com/reference/compose-file/deploy/#resources
- `security_opt`, `cap_add`, `cap_drop`, `read_only`: https://docs.docker.com/reference/compose-file/services/
- Compose secrets: https://docs.docker.com/reference/compose-file/secrets/
- Healthchecks: https://docs.docker.com/reference/dockerfile/#healthcheck
- `tini` / `init: true` for PID 1 signal handling: https://docs.docker.com/reference/compose-file/services/#init
- Docker Scout (vuln scanning): https://docs.docker.com/scout/ | Trivy: https://trivy.dev/
- Logging drivers + rotation: https://docs.docker.com/engine/logging/drivers/
