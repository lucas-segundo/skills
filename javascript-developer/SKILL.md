---
name: javascript-developer
description: JavaScript and TypeScript conventions and best practices. Use whenever writing, editing, reviewing, or debugging JS/TS code — .js, .ts, .mjs, Node scripts, async/await, modules, functions, error handling, or tests.
---

# JavaScript Developer

Write modern, boring, readable JavaScript. Where the codebase already has a pattern that doesn't conflict with best practice, stay consistent with it; where it does conflict, follow best practice and flag the deviation rather than copying the flaw.

## Rules of thumb

- **No barrel files.** Import from the specific file, not an `index.js` that only re-exports.
- **Small, single-purpose functions.** Named exports over default exports.

## JavaScript best practices

Read [best-practices.md](best-practices.md) before writing or reviewing JavaScript code.

## Quality

Read [quality.md](quality.md) for naming, comments, secrets, linting, and testing conventions.
