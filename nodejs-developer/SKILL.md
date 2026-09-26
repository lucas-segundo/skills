---
name: nodejs-developer
description: Node.js hexagonal backend conventions. Manual use only.
disable-model-invocation: true
---

# Extending the JavaScript Developer skill
- This skill extends the [JavaScript Developer](../javascript-developer/SKILL.md) skill. Read it first, then read this one.

# Node Backend Developer

Hexagonal layout, library-agnostic. The architecture is the convention; the framework, ORM, validator and test runner are swappable details. Before writing code, detect what the project uses (package.json, existing files) and follow it. Where the codebase pattern conflicts with best practice, follow best practice and flag the deviation.

## Layout (`src/`)

Applies unless the project's CLAUDE.md/AGENTS.md says `project-structure: off` (or equivalent: the user says to skip the skill's structure). When off, do NOT read project-structure.md, ignore the dependency-direction paragraph and the endpoint checklist below, and follow the project's existing layout; other conventions still apply. Otherwise:

Read [project-structure.md](project-structure.md) before writing or reviewing code. It has the folder tree, naming table, per-layer rules (entities, ports, use cases, adapters, controllers, DTOs, wiring), and how to add a new area.

Dependency direction: `main` -> `app`/`infra` -> `domain`. `domain` imports nothing outward. `app` never imports the framework, ORM, or validation library. Cross-layer imports use the project's absolute alias; relative paths only within the same folder. No barrel files.

## Adding an endpoint (checklist)

1. Entity change/factory + unit test if the domain needs it.
2. Port in `app/ports/<area>/`.
3. Use case + test. Skip for pure read (query) ports: the controller calls the port directly.
4. Adapter (and schema/migration if storage changes).
5. Register in the composition root / DI container.
6. DTO, controller/route handler, wiring.
7. Controller tests. Update API docs (OpenAPI etc.) if the route is documented.
8. Run the project's test and lint scripts.
