---
name: writing-javascript
description: Applies JavaScript and TypeScript coding, testing and verification conventions. Use when writing, editing, reviewing, or debugging JS/TS code (.js, .ts, .mjs, Node scripts), including async/await, modules, functions, error handling, or tests.
---

# JavaScript Developer

Write modern, boring, readable JavaScript. Follow the codebase's existing pattern unless it conflicts with best practice; then follow best practice and flag the deviation.

- No barrel files: import from the specific file.
- Small, single-purpose functions. Named exports over default.

## Reference files

- [coding.md](coding.md): read before writing or reviewing JS/TS.
- [testing.md](testing.md): read before writing or reviewing tests.
- [verification.md](verification.md): read before ending any turn that edited JS/TS. Lint, related tests and `tsc` must have run on the edited files; do not end the turn first.
