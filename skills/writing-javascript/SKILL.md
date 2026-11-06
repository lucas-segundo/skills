---
name: writing-javascript
description: Applies JavaScript and TypeScript coding, testing and verification conventions. Use when writing, editing, reviewing, or debugging JS/TS code (.js, .ts, .mjs, Node scripts), including async/await, modules, functions, error handling, or tests.
---

# JavaScript Developer

Follow the codebase's existing pattern unless it conflicts with these rules or best practice; then follow them and flag the deviation.

- No code comments (inline, block or JSDoc) unless the user asks for them. Leave existing comments as they are.
- Never write `TODO` in code. If work would be left unfinished, or needs something outside the task (a missing endpoint, field or API), warn the user and ask whether to finish it another way.

## Reference files

- [coding.md](coding.md): read before writing or reviewing JS/TS.
- [testing.md](testing.md): read before writing or reviewing tests.
- [verification.md](verification.md): read before ending any turn that edited JS/TS. Lint, related tests and `tsc` must have run on the edited files; do not end the turn first.
