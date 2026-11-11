---
name: writing-react
description: Applies React frontend coding and testing conventions on top of the JavaScript ones. Use when writing, editing, reviewing, or debugging React code, including components, JSX/TSX, hooks (useState, useEffect, useMemo, useCallback, custom hooks), Suspense, data fetching, forms, or React tests.
---

# React Developer

React is JavaScript: [../writing-javascript/SKILL.md](../writing-javascript/SKILL.md) and its reference files apply too, including its verification step before ending a turn.

- [coding.md](coding.md): read before writing or reviewing React code.

## Planning

Plan with the `planning` skill. Leave classNames and styling out of the plan; the reviewer checks the screen. Keep the plan short and simple: a few bullets per item, no prose. Prioritize:

- API calls: each endpoint, its params (`include`, `filter`, `sort`, `limit`, pagination), and which data hook calls it.
- Page rendering: which screen renders each hook, where the `<Suspense>` and error boundaries sit, and the loading, error and empty states.
