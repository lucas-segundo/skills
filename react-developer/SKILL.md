---
name: react-developer
description: React frontend conventions. Manual use only.
disable-model-invocation: true
---

# Extending the JavaScript Developer skill
- This skill extends the [JavaScript Developer](../javascript-developer/SKILL.md) skill. Read it first, then read this one.

# React Developer

Write React code that follows best practice first. Where the codebase already has a pattern that doesn't conflict with best practice, stay consistent with it; where it does conflict, follow best practice and flag the deviation rather than copying the flaw.

## Structure

Applies unless the project's CLAUDE.md/AGENTS.md says `project-structure: off` (or equivalent: the user says to skip the skill's structure). When off, do NOT read project-structure.md; follow the project's existing layout. Otherwise, for a new project or a folder-layout question, see [project-structure.md](project-structure.md).

## Rules of thumb

- **Decide how the data is used before fetching.** Check the code, or ask the user if unclear: does the data need client-side interaction (refetch, polling, mutations, filters, pagination), or is it loaded once and static for the page? Interactive data goes through the client data-fetching layer; static data is fetched once on the server when the app supports SSR.

## React best practices

Read [best-practices.md](best-practices.md) before writing or reviewing React code. It covers data fetching with Suspense, components, state, effects, memoization, lists, loading/error, forms.

## Quality

Read [quality.md](quality.md) for linting, formatting, and testing conventions.
