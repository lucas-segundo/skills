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

Run [verification.md](verification.md) before finishing. It applies only if the project has a linter or test runner; when one runs, the task is done only when it passes.
