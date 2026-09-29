# Project Structure

Feature-based layout. Each feature owns its types, hooks and screens; code used by more than one feature lives in `shared`. If the project already has a sound layout, follow it; use this as the default when starting one.

```
src/
├── app/                      # Routes only: thin files that point at a screen/page
├── features/
│   └── <feature>/
│       ├── types.ts          # Interfaces mirroring backend entities
│       ├── hooks/
│       │   ├── keys.ts       # Query/cache keys (client-side data only)
│       │   └── use<Thing>.ts # Client-side data hooks
│       ├── components/       # Components used only by this feature
│       └── screen/
│           └── <Name>Screen.tsx  # Screen/page: composes components and data
├── shared/
│   ├── api/
│   │   ├── config.ts         # Shared HTTP client
│   │   └── <route-first-segment>/<verbNoun>.ts  # One function per API call
│   ├── components/           # Reusable UI (error boundary, buttons, inputs)
│   └── hooks/                # Reusable hooks
└── theme/                    # Design tokens (colors, spacing) and theme hook
```

## Rules

- **Screens compose.** No inline fetching or business logic; pull data from hooks (client) or call the API function on the server (SSR).
- **API functions live in `shared/api`**, one per call, so any feature can reuse them. Payload types are exported from the same file.
- **API folders are named after the first path segment of the route**, singular. `/exercises`, `/exercises/:id` and `/exercises/:id/finish` all go in `shared/api/exercise/` (e.g. `getExercises.ts`, `getExercise.ts`, `finishExercise.ts`).
- **Promote to `shared` on second use.** Keep code inside its feature until another feature needs it.
- **Features never import each other.** Shared code goes to `shared`.
- **No barrel files.** Import from the specific file.
- **Import with the project's alias**, not deep relative paths.

Lint enforcement: see [lint.md](lint.md).
