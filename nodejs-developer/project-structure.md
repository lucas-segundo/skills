# Project Structure

Hexagonal (ports and adapters) layout for a Node.js/TypeScript backend. Folder names and roles are the convention; framework, ORM, validator and test runner are swappable.

## Tree

```
src/
├── domain/                              # business core, zero outward imports
│   ├── errors.ts                        # DomainError base + NotFoundError, ConflictError, ValidationError
│   └── entities/
│       ├── <entity>.ts                  # class + static factory + immutable transitions
│       └── <entity>.spec.ts             # unit test beside it
│
├── app/                                 # application layer, framework/ORM free
│   ├── pagination.ts                    # PaginationParams, resolvePagination (Paginated<T> only if totals are requested)
│   ├── ports/
│   │   └── <area>/
│   │       └── <verb>-<noun>.ts         # interface <Verb><Noun>Port { execute(...) }
│   └── use-cases/
│       └── <area>/
│           └── <verb>-<noun>/
│               ├── index.ts             # handler class + exported <Name>Dto interface
│               └── test.ts              # mocks ports, no I/O
│
├── infra/                               # implementations of ports
│   └── <persistence>/                   # e.g. prisma/, typeorm/, in-memory/
│       ├── schema | migrations          # storage definition
│       └── adapters/
│           └── <area>/
│               └── <verb>-<noun>.ts     # <Tech><Verb><Noun>Adapter implements port
│
└── main/                                # delivery layer: HTTP + wiring
    ├── app                              # root wiring, registers each area
    ├── index.ts                         # bootstrap (global pipes, filters, listen)
    ├── routes/
    │   └── <area>/
    │       ├── module                   # composition for this area: builds adapters, injects into use cases
    │       ├── controller.ts            # thin: parse, call handler/port, shape response
    │       ├── controller.spec.ts       # controller built directly with mocks
    │       └── dto/
    │           └── <verb>-<noun>.ts     # request validation, conforms to use-case DTO
    └── shared/                          # cross-area helpers
        ├── domain-exception filter      # domain errors -> HTTP status
        ├── pagination DTO
        ├── include helpers              # ?include= allow-list + builder
        └── db client wiring
```

## Dependency direction

```
main ──> app ──> domain
main ──> infra ──> app (ports) ──> domain
```

- `domain` imports nothing outward.
- `app` never imports framework, ORM, or validation library.
- `infra` implements `app/ports`; it is the only place that knows the ORM.
- `main` is the only place that knows the web framework and how dependencies are composed (manual wiring or a DI container).

## Naming

| Thing | Pattern | Example |
| --- | --- | --- |
| File | kebab-case, one operation per file | `complete-set.ts` |
| Entity | domain noun, PascalCase | `WorkoutSession` |
| Port | `<Verb><Noun>Port` | `FindSessionByIdPort` |
| Use case | verb class | `CompleteSet` |
| Use-case input | `<Name>Dto` | `CompleteSetDto` |
| Adapter | `<Tech><Verb><Noun>Adapter` | `PrismaCreateSessionAdapter` |
| Tests | beside source: `<name>.spec.ts`, or `test.ts` in a use-case folder | |

## Layer rules

**Entities** (`domain/entities/<name>.ts`)
- Class with `readonly` constructor params (immutable). Name = domain noun.
- Static factory for creation (`create`, `start`, ...) validates input and generates id + timestamps. The constructor stays dumb, used for rehydration from storage.
- State changes return a new instance, never mutate.
- Derived state as getters.
- Throw domain errors from `domain/errors.ts` with a `code` (see Domain errors below). Message format: `'<Entity> <field> cannot be empty'`.
- Unit test next to it.


```ts
export class WorkoutSession {
  constructor(
    readonly id: string,
    readonly programId: string,
    readonly startedAt: Date,
    readonly endedAt: Date | null,
  ) {}

  static start(programId: string): WorkoutSession {
    if (!programId.trim()) {
      throw new ValidationError('SESSION_PROGRAM_REQUIRED', 'Session programId cannot be empty', { field: 'programId' });
    }
    return new WorkoutSession(crypto.randomUUID(), programId, new Date(), null);
  }

  get isActive(): boolean {
    return this.endedAt === null;
  }

  finish(): WorkoutSession {
    if (!this.isActive) {
      throw new ConflictError('SESSION_ALREADY_FINISHED', 'Session is already finished', { id: this.id });
    }
    return new WorkoutSession(this.id, this.programId, this.startedAt, new Date());
  }
}
```

**Domain errors** (`domain/errors.ts`)
- One abstract `DomainError` base extends `Error`. Generic kinds extend it: `NotFoundError`, `ConflictError`, `ValidationError`. Add a kind only when the boundary must react differently (e.g. `ForbiddenError`); never one class per entity or rule.
- Every error carries a `code`: a stable `UPPER_SNAKE` string that identifies the specific failure for clients (`SESSION_NOT_FOUND`, `SET_ALREADY_RECORDED`). Codes are a public contract: never rename or reuse one, and never make clients parse `message`. Define them as constants in `domain/errors.ts` (or beside the entity that raises them) so each is declared once.
- Every error also carries `meta`: a plain, serializable object with the machine-readable facts behind the message (missing id, conflicting field and value, invalid field). Keep `message` human-readable and stable; put variable data in `meta`, not interpolated only into the message.
- `meta` holds data only (strings, numbers, booleans, plain objects). No entities, ORM rows, or stack traces, so it is safe to log and to return to clients.
- Errors know nothing about HTTP, logging, or i18n. The delivery layer maps kind -> status and may expose `meta` in the response body; clients and tests branch on `code` and read `meta`, never on message text.

```ts
export type ErrorMeta = Record<string, unknown>;

export abstract class DomainError extends Error {
  constructor(
    readonly code: string,
    message: string,
    readonly meta: ErrorMeta = {},
  ) {
    super(message);
    this.name = new.target.name;
  }
}
export class NotFoundError extends DomainError {}
export class ConflictError extends DomainError {}
export class ValidationError extends DomainError {}

throw new NotFoundError('SESSION_NOT_FOUND', 'Session not found', { id });
throw new ConflictError('SET_ALREADY_RECORDED', 'Set already recorded', { exerciseId, setNumber });
throw new ValidationError('SET_NUMBER_INVALID', 'SessionSet setNumber must be a positive integer', { field: 'setNumber', value: setNumber });
```

**Ports** (`app/ports/<area>/<action>.ts`)
- One interface per operation, single method `execute`. Name `<Verb><Noun>Port`. Ports return domain entities, never ORM rows.
- Params: `execute` always takes a single params object (`execute({ session })`, `execute({ page, limit })`), so arguments are named and adding one is not a breaking change. Only exception: find-by-id ports take the id first, then optional params: `execute(id, params?)`.
- Lists return `{ data }` and take `PaginationParams` inside that params object. Do not return a `total` by default: it costs a second `count` query per request. Add it (as a separate port or an opt-in param) only when the user asks for it.
- Optional relations: an `include` param, typed so the return narrows. Only add when a caller needs it.


```ts
// find-by-id: id first, then optional params
export interface FindSessionByIdPort {
  execute(id: string, params?: { include?: { sets?: boolean } }): Promise<WorkoutSession | null>;
}

// everything else: one params object
export interface FindSessionsPort {
  execute(params: PaginationParams): Promise<{ data: WorkoutSession[] }>;
}

export interface UpdateSessionPort {
  execute(params: { session: WorkoutSession }): Promise<void>;
}
```

**Use cases** (`app/use-cases/<area>/<action>/index.ts`)
- Class named by verb, constructor takes ports as `private readonly xPort: XPort`, one `async execute(dto)`.
- Export the input as a plain `<Name>Dto` interface from the same file (no framework or validation decorators).
- Order: load -> guard (throw domain error) -> call entity factory/method -> persist via port -> return entity.
- Business rules live here or in the entity, never in the controller or adapter.


```ts
export interface FinishSessionDto {
  id: string;
}

export class FinishSession {
  constructor(
    private readonly findSessionByIdPort: FindSessionByIdPort,
    private readonly updateSessionPort: UpdateSessionPort,
  ) {}

  async execute({ id }: FinishSessionDto): Promise<WorkoutSession> {
    const session = await this.findSessionByIdPort.execute(id);
    if (!session) throw new NotFoundError('SESSION_NOT_FOUND', 'Session not found', { id });

    const finished = session.finish();
    await this.updateSessionPort.execute({ session: finished });
    return finished;
  }
}
```

**Adapters** (`infra/<persistence>/adapters/<area>/<action>.ts`)
- `<Tech>XAdapter implements XPort`, receives the DB client through the constructor, single `execute`.
- Map rows to entities explicitly. Never leak ORM/driver types out.
- Pagination: offset = `(page - 1) * limit`, limit = `limit`, one page query with explicit ordering. No `count` query unless the user asks for totals (then run it concurrently with the page query).
- Keep adapters stateless. Never store per-call results on adapter fields: adapters are shared singletons, so it is a race.


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

**Controllers / route handlers** (`main/routes/<area>/`)
- Thin: parse input, call a use case, shape response. Validate only what comes from the request: shape, types, required fields, formats, allowed `include` paths, pagination bounds. Business validation (existence, state, uniqueness, invariants) belongs to entities or use cases, never the controller.
- Controllers never throw domain errors and never inspect ports' results to decide business outcomes (no `if (!session) throw NotFound` in a controller).
- Path params merged with body into the use-case DTO explicitly.
- Domain errors are translated to HTTP in one shared place (filter/middleware/error handler): NotFound -> 404, Conflict -> 409, Validation -> 400, and return `{ code, message, meta }` in the response body. Do not scatter status codes.
- Missing single resource on reads: the use case throws `NotFoundError`; the shared error handler answers 404. Reads that need only a lookup still get a small use case for this reason.
- List response envelope: `{ data, page, limit }` using `resolvePagination(query)`. Add `total` only when the user asks for it.
- Relation loading via `?include=a,b`: allow-list per route, sanitize (depth and breadth capped), then map to the port's `include` shape.


```ts
// Framework-neutral shape: adapt to the project's router/controller style.
const SESSION_INCLUDES = new Set(['sets', 'program']);

// request validation only: include paths are checked against an allow-list
async function findById(id: string, query: { include?: string[] }) {
  const paths = sanitizeIncludes(query.include ?? [], SESSION_INCLUDES);
  return findSessionById.execute({ id, include: { sets: paths.includes('sets') } }); // use case throws NotFoundError
}

async function finish(id: string) {
  return finishSession.execute({ id }); // domain errors handled by the shared error handler
}

// shared error handler
function toHttp(error: DomainError) {
  const status = error instanceof NotFoundError ? 404 : error instanceof ConflictError ? 409 : 400;
  return { status, body: { code: error.code, message: error.message, meta: error.meta } };
}
```

**DTOs / request validation** (`main/routes/<area>/dto/<action>.ts`)
- Validate at the boundary with the project's validator (decorators, schemas, whatever exists). Strip unknown fields, coerce query numbers.
- Make the DTO conform to the use-case DTO type so drift fails compile.
- Validate once at the edge; do not re-validate in controllers.


```ts
// Decorator class, schema object, or zod-like parser: use what the project has.
// The point is the contract: the validated type must satisfy the use-case DTO.
const startSessionBody = schema({ programId: string().nonEmpty() });
type StartSessionBody = Infer<typeof startSessionBody>;
const _check: StartSessionDto = {} as StartSessionBody; // drift fails compile
```

**Wiring / composition** (`main/`)
- Use cases and adapters are plain classes with no framework decorators. Only the wiring layer knows how objects are composed.
- Compose by constructor injection: `new UseCase(new Adapter(dbClient))`. Default to manual wiring; if the project already uses a DI container, register each port and handler with its identifier the way the container expects.
- Adapters get the DB client; handlers get their ports. Register each area's wiring in the app root.


```ts
// main/routes/sessions/module (composition root for the area)
const findSessionByIdPort = new PostgresFindSessionByIdAdapter(db);
const updateSessionPort = new PostgresUpdateSessionAdapter(db);
const findSessionById = new FindSessionById(findSessionByIdPort); // throws NotFoundError
const finishSession = new FinishSession(findSessionByIdPort, updateSessionPort);
// hand the use cases to the controller; with a DI container, register the same graph.
```

## Adding a new area

1. `app/ports/<area>/` port per operation.
2. `app/use-cases/<area>/<action>/` handler + test.
3. `infra/<persistence>/adapters/<area>/` adapter per port.
4. `main/routes/<area>/` module, controller, spec, dto.
5. Register the area in `main/app` (and in the container, if the project uses one).
