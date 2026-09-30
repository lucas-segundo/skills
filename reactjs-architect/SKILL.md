---
name: react-architect
description: Configures a React frontend's project structure, the lint rules that enforce it, and AGENTS.md so AI agents follow it. Manual use only.
disable-model-invocation: true
---

# React Architect

Owns React project structure. `react-developer` covers code conventions only.

## Steps

1. **Detect.** Read `package.json` and the existing `src/`. Note the import alias and the linter (ESLint flat config, `.eslintrc`, Biome).
2. **Respect an existing layout.** If it is sound, adapt the lint rules to it and skip scaffolding. Scaffold folders only for a new project or when asked. Layout: [project-structure.md](project-structure.md).
3. **Configure lint** from [lint.md](lint.md) so structure violations fail `lint`. Extend the existing config, never replace the user's rules. Install only the plugin it names, with the project's package manager.
4. **Write `AGENTS.md`** at the project root using the block below. If one exists, keep the user's content and only add or update `## Project structure`. If the project uses `CLAUDE.md`, make it import `@AGENTS.md`.
5. **Verify.** Run lint. Add one illegal import, confirm lint fails, remove it. Report what was configured.

If AGENTS.md/CLAUDE.md says `project-structure: off`, or the user says to skip structure, do nothing.

## AGENTS.md block

Fill `<alias>` with the project's import alias.

```md
## Project structure

These rules are enforced by lint. Do not disable or bypass them; if a rule blocks you, the design is wrong, so ask the user.

- Layout: `src/app` (routes only), `src/features/<feature>` (types, hooks, components, screen), `src/shared` (api, components, hooks), `src/theme`.
- `app` may import `features` and `shared`. `features` may import `shared` and `theme`, never another feature. `shared` imports only `shared` and `theme`.
- Screens compose components and hooks; no inline fetching or business logic.
- One API function per file in `shared/api/<route-first-segment-singular>/`.
- Move code to `shared` when a second feature needs it, not before.
- No barrel files. Import from the specific file using `<alias>`, never deep relative paths across folders.
- Before finishing, run lint and fix every boundary error.
```
