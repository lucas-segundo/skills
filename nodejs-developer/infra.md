# Infra Layer

`src/infra/` implements the ports declared in `app/ports`. It is the only layer that knows the ORM, query builder, or driver. Swapping persistence means swapping this folder.

## Contents

```
infra/
└── <persistence>/                   # e.g. prisma/, typeorm/, in-memory/
    ├── schema | migrations          # storage definition
    └── adapters/
        └── <area>/
            └── <verb>-<noun>.ts     # <Tech><Verb><Noun>Adapter implements port
```

## Adapters

- Name `<Tech><Verb><Noun>Adapter` (`PrismaCreateSessionAdapter`), one per port, `implements` that port.
- Receives the DB client through the constructor. Single `execute` method.
- Maps rows explicitly. Never leaks ORM or driver types out. Command and entity-returning ports build domain entities; query ports may return the plain `<Name>Query` shape, or an entity plus computed fields via `Object.assign(new Entity(...), { extra })`.
- Query aggregates (counts, sums) are computed from included rows or in the query. Keep it simple, no business rules.
- Pagination: offset = `(page - 1) * limit`, limit = `limit`, one page query with explicit ordering. No `count` query unless the user asks for totals (then run it concurrently with the page query).
- Stateless. Adapters are shared singletons: never store per-call results on adapter fields, it is a race.
- Contains no business rules. Guards and invariants belong to entities and use cases.

```ts
// `db` is whatever client the project uses (ORM, query builder, driver).
export class PostgresFindSessionsAdapter implements FindSessionsPort {
  constructor(private readonly db: DbClient) {}

  async execute({ page, limit }: PaginationParams) {
    const rows = await this.db.sessions.findMany({
      offset: (page - 1) * limit,
      limit,
      orderBy: { startedAt: 'desc' },
    });
    return {
      data: rows.map((r) => new WorkoutSession(r.id, r.programId, r.startedAt, r.endedAt)),
    };
  }
}
```

## Rules

- Imports `app/ports` and `domain` (to build entities). Never `main`.
- Schema and migrations live beside the adapters that use them.
- Only `main` wires adapters into use cases; use cases never import from here.
