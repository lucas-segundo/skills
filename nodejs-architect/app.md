# App Layer

`src/app/` is the application layer. It orchestrates business operations: it defines what the system needs from the outside (ports) and the use cases that combine ports with domain entities. It is framework and ORM free. It may import `domain` only.

## Command ports

A command port mutates data (create/update/delete). It is always used inside a use case, never called from a controller.

- One interface per operation, single method `execute`. Name `<Verb><Noun>Port` (`UpdateSessionPort`).
- Take domain entities, never ORM rows. Reading data is a query port, see Query ports.
- `execute` takes a single params object (`execute({ session })`), so arguments are named and adding one is not a breaking change.

```ts
export interface UpdateSessionPort {
  execute(params: { session: WorkoutSession }): Promise<void>;
}
```

## Query ports

Every port that finds or fetches data is a query port (list, detail, report). It has no use case of its own: the controller calls it directly.

- Read-only, no side effects. Mutations belong to command ports.
- No separate read-model types: the port returns the entity. Extra data is requested through `include` and the adapter attaches it to the returned object (`Object.assign`).
  - The port's return type declares each included relation as optional: `Entity & { relation?: Relation }` (or `Partial<{ ... }>`). No `Omit`, no generics.
  - If the entity already declares the relation, leave the return type as the entity.
- Find-by-id returns `null` when missing. The controller maps `null` to the framework's not-found response (no use case to throw `NotFoundError`).
- One interface per operation, single method `execute`. Name `<Verb><Noun>Port` (`FindSessionByIdPort`).
- Find-by-id takes the id first, then optional params: `execute(id, params?)`. Other queries take a single params object.
- Lists return `{ data }` and take `Pagination` as a `pagination` prop in the params object (`{ pagination }`). No `total` by default: it costs a second `count` query. Add it only when the user asks.
- Optional relations use an `include` param (`params?: { include?: { exercises?: boolean } }`). Add only when a caller needs it.
- A command use case may still inject a query port to load what it needs (see `FinishSession`). The guard stays in that use case.
- Guards, state checks and decisions never live in a query port or its controller call: they belong to a command use case.

```ts
import { Program } from 'src/domain/entities/program';
import { ProgramExercise } from 'src/domain/entities/program-exercise';

export interface FindProgramByIdPort {
  execute(
    id: string,
    params?: { include?: { exercises?: boolean } },
  ): Promise<(Program & { exercises?: ProgramExercise[] }) | null>;
}
```

## Use cases

- Class named by verb (`FinishSession`). Constructor takes ports as `private readonly xPort: XPort`. One `async execute(dto)`.
- Export the input as a plain `<Name>Dto` interface from the same file. No framework or validation decorators.
- Flow: load, guard (throw domain error), call entity factory/method, persist via port, return entity.
- Business rules live here or in the entity, never in the controller or adapter.
- Only commands get use cases. Reads are query ports with no use case, see Query ports.
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
