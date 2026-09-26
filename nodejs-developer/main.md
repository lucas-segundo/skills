# Main Layer

`src/main/` is the delivery layer: HTTP plus wiring. It is the only place that knows the web framework and how dependencies are composed (manual wiring or a DI container).

## Contents

```
main/
├── app                          # root wiring, registers each area
├── index.ts                     # bootstrap (global pipes, filters, listen)
├── routes/
│   └── <area>/
│       ├── module               # composition: builds adapters, injects into use cases
│       ├── controller.ts        # thin: parse, call use case, shape response
│       ├── controller.spec.ts   # controller built directly with mocks
│       └── dto/
│           └── <verb>-<noun>.ts # request validation, conforms to use-case DTO
└── shared/                      # cross-area helpers
    ├── domain-exception filter  # domain errors -> HTTP status
    ├── pagination DTO
    ├── include helpers          # ?include= allow-list + builder
    └── db client wiring
```

## Controllers

- Thin: parse input, call a use case, shape the response.
- Validate only what comes from the request: shape, types, required fields, formats, allowed `include` paths, pagination bounds.
- Business validation (existence, state, uniqueness, invariants) belongs to entities or use cases. Controllers never throw domain errors and never inspect port results to decide business outcomes.
- Query ports (read-only, see `app.md`) are called directly by the controller, no use case. `null` from a find-by-id becomes the framework's not-found response.
- Path params are merged with the body into the use-case DTO explicitly.
- List envelope: `{ data, page, limit }` using `resolvePagination(query)`. Add `total` only when the user asks.
- `?include=a,b`: allow-list per route, sanitize (depth and breadth capped), map to the port's `include` shape.

```ts
const SESSION_INCLUDES = new Set(['sets', 'program']);

const findById = async (id: string, query: { include?: string[] }) => {
  const paths = sanitizeIncludes(query.include ?? [], SESSION_INCLUDES);
  return findSessionById.execute({ id, include: { sets: paths.includes('sets') } });
};
```

## Error handling

Domain errors are translated to HTTP in one shared place (filter, middleware, or error handler). Do not scatter status codes.

- `NotFoundError` -> 404, `ConflictError` -> 409, `ValidationError` -> 400.
- Body: `{ code, message, meta }`.

```ts
const toHttp = (error: DomainError) => {
  const status = error instanceof NotFoundError ? 404 : error instanceof ConflictError ? 409 : 400;
  return { status, body: { code: error.code, message: error.message, meta: error.meta } };
};
```

## DTOs / request validation

- DTOs belong to use cases only. The controller does not define DTOs; it validates the request input and maps it to the use-case DTO.
- Input source: GET reads query params; every other method (POST, PUT, PATCH, DELETE) reads the body.
- Validate at the boundary with the project's validator (decorators, schemas, whatever exists). Strip unknown fields, coerce query numbers.
- Make the request schema conform to the use-case DTO type so drift fails compile.
- Validate once at the edge; do not re-validate in controllers.

```ts
// POST -> body
const startSessionBody = schema({ programId: string().nonEmpty() });
type StartSessionBody = Infer<typeof startSessionBody>;
const _check: StartSessionDto = {} as StartSessionBody; // drift fails compile

// GET -> query
const listSessionsQuery = schema({ page: number().int().min(1) });
```

## Wiring / composition

- Use cases and adapters are plain classes with no framework decorators. Only this layer composes them.
- Constructor injection: `new UseCase(new Adapter(dbClient))`. Default to manual wiring; if the project already uses a DI container, register each port and handler the way the container expects.
- Adapters get the DB client; use cases get their ports. Register each area in the app root.

```ts
// main/routes/sessions/module (composition root for the area)
const findSessionByIdPort = new PostgresFindSessionByIdAdapter(db);
const updateSessionPort = new PostgresUpdateSessionAdapter(db);
const findSessionById = new FindSessionById(findSessionByIdPort);
const finishSession = new FinishSession(findSessionByIdPort, updateSessionPort);
```

## Rules

- May import every other layer. Nothing imports `main`.
- Holds no business rules.
