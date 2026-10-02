---
name: writing-react
description: Applies React frontend coding and testing conventions on top of the JavaScript ones. Use when writing, editing, reviewing, or debugging React code, including components, JSX/TSX, hooks (useState, useEffect, useMemo, useCallback, custom hooks), Suspense, data fetching, forms, or React tests.
---

# React Developer

Write React code that follows best practice first. Where the codebase already has a pattern that doesn't conflict with best practice, stay consistent with it; where it does conflict, follow best practice and flag the deviation rather than copying the flaw.

React code is also JavaScript, so the `writing-javascript` conventions apply too. Read its files directly:

- [../writing-javascript/coding.md](../writing-javascript/coding.md): general JS/TS coding rules.
- [../writing-javascript/testing.md](../writing-javascript/testing.md): general testing rules.

## Reference files

- **Coding**: read [coding.md](coding.md) before writing or reviewing React code.
- **Testing**: read [testing.md](testing.md) before writing or reviewing component tests.

## Planning

In plan mode, do not describe classNames or styling details in the plan. The reviewer checks the screen to verify styling.

## Verification (final step)

**Hard rule:** do not end the turn after editing JS/TS files until this step has run.

- **Scope:** only the JS/TS files created or edited in this prompt, including files changed by codemods or `--fix`. Never the whole project, a folder or a suite.
- **Lint and tests:** prefer `npm run lint:ai -- <files>` and `npm run test:ai -- --findRelatedTests <files>` when `package.json` has them. Otherwise `eslint <files>` and `jest --findRelatedTests <files>`.
- **Type check:** in a TS project, also run `npx tsc --noEmit` (it can't be scoped to files). Run it once, as the last step, after lint and tests pass. Fix only errors in the files edited this prompt; mention errors in other files but don't fix them.
- **Report:** pass only if the files were linted and tests actually ran. Name the files linted and tested, say which have no related tests, and state the `tsc` result and whether any errors belong to the edited files. On failure, fix the cause and rerun.
- **Whole-project runs** (full jest run, a whole folder) only if the user asks.

Full detail in [../writing-javascript/verification.md](../writing-javascript/verification.md); read it if anything above is unclear.
