---
name: architecting-nodejs-backends
description: Configures a Node.js hexagonal backend's project structure, the lint rules that enforce it, and AGENTS.md so AI agents follow it. Use when the user asks to set up, scaffold, or enforce the structure of a Node.js backend. Manual use only.
disable-model-invocation: true
---

# Node.js Architect

Owns Node backend structure. `writing-javascript` covers code conventions only.

## Steps

Copy this checklist and check off each step:

```
Architect progress:
- [ ] 1. Detect
- [ ] 2. Respect an existing layout
- [ ] 3. Configure lint
- [ ] 4. Write AGENTS.md
- [ ] 5. Verify
```

1. **Detect.** Read `package.json` and the existing `src/`. Note the import alias, framework, ORM, validator and linter (ESLint flat config, `.eslintrc`, Biome).
2. **Respect an existing layout.** If it is sound, adapt the lint rules to it and skip scaffolding. Scaffold folders only for a new project or when asked. Read [project-structure.md](project-structure.md) first; layer details are in [domain.md](domain.md), [app.md](app.md), [infra.md](infra.md), [main.md](main.md).
3. **Configure lint** from [lint.md](lint.md) so structure violations fail `lint`. Extend the existing config, never replace the user's rules. Install only the plugin it names, with the project's package manager.
4. **Write `AGENTS.md`** at the project root using the block below. If one exists, keep the user's content and only add or update `## Project structure`. If the project uses `CLAUDE.md`, make it import `@AGENTS.md`.
5. **Verify.** Run lint. Add one illegal import (e.g. `domain` importing `infra`), confirm lint fails, remove it. If lint passes on the illegal import, fix the config (patterns, alias resolver) and repeat. Report what was configured.

If AGENTS.md/CLAUDE.md says `project-structure: off`, or the user says to skip structure, do nothing.

## AGENTS.md block

Fill `<alias>` with the project's import alias.

```md
## Project structure

Hexagonal layout, enforced by lint. Do not disable or bypass the rules; if one blocks you, the design is wrong, so ask the user.

- Layout: `src/domain` (entities, errors), `src/app` (ports, use cases), `src/infra/<persistence>` (adapters), `src/main` (routes, controllers, DTOs, wiring).
- Dependency direction: `main` -> `app`/`infra` -> `domain`. `domain` imports nothing outward. `app` imports only `domain` and never a framework, ORM or validator. `infra` imports `app/ports` and `domain`, never `main`. Nothing imports `main`.
- Ports live in `app/ports/<area>/`, one folder per entity; adapters mirror them in `infra/<persistence>/<area>/`.
- One operation per file, kebab-case, except the per-entity query and metric ports. Command ports `<Verb><Noun>Port`. Each entity has one `<Entity>QueryPort` with only `findOne` and `findMany`, and one `<Entity>MetricPort` with `get({ filter, metrics, groupBy? })` returning `{ totals, groups? }` (`groups` only when `groupBy` is passed; shared types in `app/ports/metrics.ts`). Adapters `<Tech><Verb><Noun>Adapter`, `<Tech><Entity>QueryAdapter`, `<Tech><Entity>MetricAdapter`.
- Ports are generic data operations: a new read is a filter, sort, include or group key, never a new method or a port named after a use case. Query building shared by an adapter's methods lives in private methods.
- Commands go through a use case; reads are query and metric ports called by the controller.
- Business rules live in entities and use cases, never in controllers or adapters.
- No barrel files. Cross-layer imports use `<alias>`; relative paths only within the same folder.
- New endpoint order: entity, port, use case + test (commands only), adapter, wiring, DTO + controller + test. Run lint and tests before finishing.
```
