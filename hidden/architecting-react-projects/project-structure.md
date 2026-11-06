# Project Structure

Feature-based layout, the default for a new project. Rules are in the AGENTS.md block in [SKILL.md](SKILL.md).

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

API folders are named after the first path segment of the route, singular: `/exercises`, `/exercises/:id` and `/exercises/:id/finish` all go in `shared/api/exercise/` (`getExercises.ts`, `getExercise.ts`, `finishExercise.ts`). Payload types are exported from the same file as the function.
