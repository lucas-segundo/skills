# App Layer

`src/app/` is the application layer. It orchestrates business operations: it defines what the system needs from the outside (ports) and the use cases that combine ports with domain entities. It is framework and ORM free. It may import `domain` only.

## Contents

```
app/
├── pagination.ts                # PaginationParams, resolvePagination
├── ports/
│   └── <area>/
│       └── <verb>-<noun>.ts     # interface <Verb><Noun>Port { execute(...) }
└── use-cases/
    └── <area>/
        └── <verb>-<noun>/
            ├── index.ts         # handler class + exported <Name>Dto interface
            └── test.ts          # mocks ports, no I/O
```

## Ports

- One interface per operation, single method `execute`. Name `<Verb><Noun>Port` (`FindSessionByIdPort`).
- Ports return domain entities, never ORM rows.
- `execute` takes a single params object (`execute({ session })`), so arguments are named and adding one is not a breaking change. Exception: find-by-id ports take the id first, then optional params: `execute(id, params?)`.
- Lists return `{ data }` and take `PaginationParams` in the params object. No `total` by default: it costs a second `count` query. Add it only when the user asks.
- Optional relations use an `include` param, typed so the return narrows. Add only when a caller needs it.

```ts
export interface FindSessionByIdPort {
  execute(id: string, params?: { include?: { sets?: boolean } }): Promise<WorkoutSession | null>;
}

export interface FindSessionsPort {
  execute(params: PaginationParams): Promise<{ data: WorkoutSession[] }>;
}

export interface UpdateSessionPort {
  execute(params: { session: WorkoutSession }): Promise<void>;
}
```

## Use cases

- Class named by verb (`FinishSession`). Constructor takes ports as `private readonly xPort: XPort`. One `async execute(dto)`.
- Export the input as a plain `<Name>Dto` interface from the same file. No framework or validation decorators.
- Flow: load, guard (throw domain error), call entity factory/method, persist via port, return entity.
- Business rules live here or in the entity, never in the controller or adapter.
- Reads that only look something up still get a small use case, so a missing resource throws `NotFoundError` here.
- Test in `test.ts` beside `index.ts`: mock ports, no I/O.

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

## Rules

- Imports only `domain`. Never a framework, ORM, or validation library.
- Depends on ports (interfaces), never on adapters.
- Naming: kebab-case files, one operation per file.
