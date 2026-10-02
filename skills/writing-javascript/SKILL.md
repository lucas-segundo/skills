---
name: writing-javascript
description: Applies JavaScript and TypeScript coding, testing and verification conventions. Use when writing, editing, reviewing, or debugging JS/TS code (.js, .ts, .mjs, Node scripts), including async/await, modules, functions, error handling, or tests.
---

# JavaScript Developer

Write modern, boring, readable JavaScript. Where the codebase already has a pattern that doesn't conflict with best practice, stay consistent with it; where it does conflict, follow best practice and flag the deviation rather than copying the flaw.

## Rules of thumb

- **No barrel files.** Import from the specific file, not an `index.js` that only re-exports.
- **Small, single-purpose functions.** Named exports over default exports.

## Reference files

- **Coding**: read [coding.md](coding.md) before writing or reviewing JS/TS code.
- **Testing**: read [testing.md](testing.md) before writing or reviewing tests.

## Verification (final step)

**Hard rule:** do not end the turn after editing JS/TS files until this step has run.

- **Scope:** only the JS/TS files created or edited in this prompt, including files changed by codemods or `--fix`. Never the whole project, a folder or a suite.
- **Lint and tests:** prefer `npm run lint:ai -- <files>` and `npm run test:ai -- --findRelatedTests <files>` when `package.json` has them. Otherwise `eslint <files>` and `jest --findRelatedTests <files>`.
- **Type check:** in a TS project, also run `npx tsc --noEmit` (it can't be scoped to files). Run it once, as the last step, after lint and tests pass. Fix only errors in the files edited this prompt; mention errors in other files but don't fix them.
- **Report:** pass only if the files were linted and tests actually ran. Name the files linted and tested, say which have no related tests, and state the `tsc` result and whether any errors belong to the edited files. On failure, fix the cause and rerun.
- **Whole-project runs** (full jest run, a whole folder) only if the user asks.

Full detail in [verification.md](verification.md); read it if anything above is unclear.
