# BuildKit Multi-Stage Builds & Cache Mounts

> Reference for the `docker-compose` skill.

Deep dive for hardening Dockerfiles with multi-stage builds and BuildKit cache
mounts (production hardening track, Step 2). Self-contained: covers the
multi-stage pattern, a full Python example, per-ecosystem `RUN --mount=type=cache`
mounts, and external CI cache backends.

## Multi-stage build pattern

- Use multi-stage builds: builder stage for compilation/dependencies, minimal runtime stage.
- Pin base images with specific tags or digests (never `:latest`).
- Create a non-root user and switch to it before CMD/ENTRYPOINT.
- Install only runtime dependencies in the final stage.
- Use `COPY --from=builder` to bring only built artifacts.
- Add strict `.dockerignore`: exclude `.git/`, `node_modules/`, `.env`, `*.md`, test files.
- Set `HEALTHCHECK` in the Dockerfile as a fallback (Compose-level takes precedence).

```dockerfile
# Example: Python multi-stage (BuildKit cache mount on the pip download cache)
FROM python:<current-stable>-slim AS builder  # Pin to specific version; verify latest stable
WORKDIR /app
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --prefix=/install -r requirements.txt

FROM python:<current-stable>-slim  # Pin to specific version; verify latest stable
RUN groupadd -r app && useradd -r -g app -d /app -s /sbin/nologin app
WORKDIR /app
COPY --from=builder /install /usr/local
COPY --chown=app:app . .
USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## BuildKit build-cache (highest-value build-time/cost lever)

BuildKit is the default builder; use `RUN --mount=type=cache,...` to persist
package-manager caches across builds so repeated local and CI builds skip
re-downloads. Order instructions least-to-most-changing and copy manifests
before source so the dependency layer stays cached when only application code
changes.

Cache mounts per ecosystem:

- **pip**: `--mount=type=cache,target=/root/.cache/pip` (drop `--no-cache-dir`).
- **uv**: `--mount=type=cache,target=/root/.cache/uv` (see `assets/Dockerfile.python`).
- **apt**: `--mount=type=cache,target=/var/cache/apt,sharing=locked` (and keep `rm -rf /var/lib/apt/lists` out so the cache survives; do not set `--no-cache`).
- **Go**: `--mount=type=cache,target=/go/pkg/mod --mount=type=cache,target=/root/.cache/go-build`.
- **npm/pnpm**: `--mount=type=cache,target=/root/.npm` (npm) or the pnpm store path (see `assets/Dockerfile.node`).

## External cache backend for CI

These cache mounts are local to the builder. For CI, also wire an **external
cache backend** so cache survives ephemeral runners:
`docker buildx build --cache-to type=gha,mode=max --cache-from type=gha`
(GitHub Actions) or `type=registry,ref=<registry>/<image>:buildcache,mode=max`.

External cache backends require a non-default BuildKit driver
(`docker buildx create --use`); with `docker/build-push-action`, set
`cache-from: type=gha` and `cache-to: type=gha,mode=max`.
See https://docs.docker.com/build/cache/backends/gha/.

## Authoritative sources

- BuildKit / buildx (multi-platform, cache mounts): https://docs.docker.com/build/buildkit/ and https://docs.docker.com/reference/cli/docker/buildx/
- Multi-stage builds + cache mounts: https://docs.docker.com/build/building/multi-stage/
- Cache optimization (`RUN --mount=type=cache`, instruction ordering): https://docs.docker.com/build/cache/optimize/
- CI external build-cache backend (`--cache-to/--cache-from type=gha,mode=max`): https://docs.docker.com/build/cache/backends/gha/
- uv in Docker (official multi-stage pattern, `UV_COMPILE_BYTECODE`, `uv sync --locked`): https://docs.astral.sh/uv/guides/integration/docker/
