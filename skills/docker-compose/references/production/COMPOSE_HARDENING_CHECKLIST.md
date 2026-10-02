# Docker Compose Production Hardening Checklist -- Reference

> Freshness disclaimer: verified against Docker Compose V2 and Docker Engine 27.x as of early 2026. Always cross-check with the official docs linked below.

## Official documentation

- Docker Compose file reference: https://docs.docker.com/compose/compose-file/
- Dockerfile best practices: https://docs.docker.com/build/building/best-practices/
- Docker security: https://docs.docker.com/engine/security/
- Docker Scout (vulnerability scanning): https://docs.docker.com/scout/
- Multi-stage builds: https://docs.docker.com/build/building/multi-stage/

## Security checklist

### Image security
- [ ] Base images pinned with specific version tags (not `:latest`)
- [ ] Multi-stage builds separating builder from runtime
- [ ] Non-root USER directive in every Dockerfile
- [ ] `.dockerignore` excludes `.git/`, `.env`, `node_modules/`, test files
- [ ] No secrets in build args, env vars, or layers
- [ ] Minimal runtime image (slim/alpine variants or distroless)
- [ ] Vulnerability scan passes with 0 critical findings
- [ ] SBOM / provenance attestations generated where CI supports it

### Runtime security (Compose)

`assets/production/compose.prod.example.yml` in this skill has these directives already
assembled -- pinned image tag, `read_only` root with `tmpfs`, `cap_drop: [ALL]`,
`no-new-privileges`, health check and `deploy.resources.limits`. Copy and adapt it, then
walk the boxes below against the result; validate in the target environment before shipping.

- [ ] `user:` or Dockerfile USER sets non-root identity
- [ ] `read_only: true` with `tmpfs:` for writable paths
- [ ] `cap_drop: [ALL]` with minimal `cap_add:` as needed
- [ ] `security_opt: ["no-new-privileges:true"]`
- [ ] `secrets:` used for sensitive data (not env vars for high-value secrets)
- [ ] No `container_name` set (allows scaling and parallel runs)
- [ ] No `privileged: true` (unless absolutely required and documented)

## Health check patterns

```yaml
services:
  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  redis:
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

  api:
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"]
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 30s
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
```

## Resource limits

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 128M
    restart: unless-stopped
    stop_grace_period: 30s
```

Guidance:
- Set limits on all services to prevent resource starvation.
- Set reservations on critical services to guarantee minimums.
- Adjust `stop_grace_period` based on drain time requirements.

## Network isolation

```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access

services:
  proxy:
    networks: [frontend, backend]
    ports: ["443:443"]
  api:
    networks: [backend]
  postgres:
    networks: [backend]
```

- `internal: true` prevents direct external access to backend services.
- Only the edge proxy is on both networks and exposes ports.

## Logging configuration

```yaml
services:
  api:
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
        tag: "{{.Name}}"
```

- Always set `max-size` and `max-file` to prevent disk exhaustion.
- Use `json-file` driver for local; switch to `fluentd`, `gelf`, or cloud driver for production aggregation.

## Graceful shutdown

- Use exec form for CMD: `CMD ["uvicorn", "main:app"]` (not `CMD uvicorn main:app`).
- Application must handle SIGTERM to drain connections.
- Set `stop_grace_period` to allow drain time before SIGKILL.
- Test: `docker compose stop <service>` should complete within the grace period.

## Secrets management

```yaml
secrets:
  db_password:
    file: ./secrets/db_password.txt  # Local dev
    # Or for Swarm/external: external: true

services:
  api:
    secrets:
      - db_password
    environment:
      DB_PASSWORD_FILE: /run/secrets/db_password
```

- Application reads from `/run/secrets/<name>` at runtime.
- Never commit secret files; add `secrets/` to `.gitignore`.

## Data services

- Use named volumes for persistent state (databases, caches, message brokers).
- Document backup/restore and migration flows for stateful services.
