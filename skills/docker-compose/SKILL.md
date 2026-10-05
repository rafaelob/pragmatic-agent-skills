---
name: docker-compose
description: "Use when a change must run against the repo's own Compose project (service won't start, ports, volumes). Reuse `docker compose -p <project>`. Test selection -> layered-testing-executor."
license: Apache-2.0
metadata:
  author: coding-agent
  version: 2.4.2
  category: infrastructure
  subcategory: cloud-ops
  vendor: universal
  lifecycle: active
  coding_agent: true
  tags:
  - docker
  - compose
  - dev
  - workflow
  - production
  - hardening
  - security
  audience: developer
  output_format: markdown
  modality: text
---

# Use the project's existing Compose workflow

## Reuse, don't recreate
1. **One Compose project per repo.** Everything the agent needs — dependencies, test runners, one-off tools — runs inside the repo's own `compose.yaml`/`docker-compose.yml` and project name. Never a loose `docker run`, never a second `-p <name>`, never a parallel compose file for the same stack, unless the repo already declares it as an override that the base file merges.
2. **Look before you create.** Run `docker compose ps` (and `docker compose ps -a` for stopped containers).
   - A running service is reused with `docker compose exec <service> <cmd>`.
   - A stopped one is restarted with `docker compose start <service>`.
   - Only a missing service is started, with `docker compose up -d <service>`, without `--force-recreate`, and `--build` only when the image inputs changed.
   - Recreate only a service you own whose inputs (image, build context, config) changed, with `docker compose up -d --build <service>`, keeping its volumes; never recreate or duplicate a service that is merely running, nor one another writer owns.
3. **One-offs:** use `docker compose run --rm <service> <cmd>` in the SAME project, so nothing is left behind. For a long test step, give the command its own deadline (for example `timeout <s> pytest …`) shorter than any outer lock wall, so the container dies with it.
4. **A tool the stack lacks** becomes a service in the repo's compose (with a profile such as `profiles: [tools]` when it should not start by default), never an ad-hoc `docker run`.
5. **Cleanup:** stop and remove only what you created (`run --rm` does it for one-offs). Never `docker compose down -v` or `docker system prune` on a shared stack. Check `docker system df` before adding images or volumes.

Read the canonical Compose files, wrappers, project identity, profiles, env-file order and runner. Files may live outside the root; absence of a root file does not prove no Compose workflow exists.

## Verify the code actually running
Check the image, mount or watch synchronization relevant to the test. A green run on an old copied source tree is not evidence for the new diff. Health checks demonstrate their readiness contract, not that a feature works. For configuration edits, validate the effective selected configuration without exposing secrets. Reuse valid results instead of launching a parallel stack per reviewer.

Honor machine resource admission and locks. Orphan removal is not taking the whole stack down, and none of this implies a Docker install, daemon change or global prune.

Start from `assets/docker-compose.base.yml` when the project has no stack yet. A setting outside the stack (env var, port, flag) keeps one versioned home with what, why and rollback recorded; when the failure is the Windows shell around Docker, use `windows-shell-interop`.

## Reference files
Read `references/buildkit-multistage-cache.md` when hardening a Dockerfile with multi-stage builds and BuildKit cache mounts. Read `references/dev/DOCKER_COMPOSE_DEV_WINDOWS.md` when the dev loop runs through Docker Desktop's WSL2 backend on Windows. Read `references/production/COMPOSE_HARDENING_CHECKLIST.md` before shipping a production Compose stack. Read `references/freshness-sources.md` when a Compose, BuildKit or base-image fact in this skill needs a current primary source.
