---
name: javascript-developer
description: JavaScript and TypeScript conventions and best practices. Use whenever writing, editing, reviewing, or debugging JS/TS code — .js, .ts, .mjs, Node scripts, async/await, modules, functions, error handling, or tests.
---

# JavaScript Developer

Write modern, boring, readable JavaScript. Where the codebase already has a pattern that doesn't conflict with best practice, stay consistent with it; where it does conflict, follow best practice and flag the deviation rather than copying the flaw.

## Rules of thumb

- **No barrel files.** Import from the specific file, not an `index.js` that only re-exports.
- **Small, single-purpose functions.** Named exports over default exports.

## Coding

Read [coding.md](coding.md) before writing or reviewing JavaScript code.

## Testing

Read [testing.md](testing.md) before writing or reviewing tests.

## Verification (final step)

Before finishing any task where you edited files, read [verification.md](verification.md) and run it. The task is done only when it passes.
