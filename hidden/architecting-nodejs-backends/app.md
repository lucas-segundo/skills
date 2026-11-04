# App Layer

`src/app/` is the application layer. It orchestrates business operations: it defines what the system needs from the outside (ports) and the use cases that combine ports with domain entities. It is framework and ORM free. It may import `domain` only.

## Port folders

Ports live in `app/ports/<area>/`, one folder per entity (`sessions/`, `memberships/`). A port belongs to the entity it reads or writes, not to the use case or feature that first needed it: `CreateMembershipPort` goes in `memberships/` even if only `CreateOrganization` uses it.

| Port | File | Interface |
| --- | --- | --- |
| Command (one per mutation) | `<area>/<verb>-<noun>.ts` | `<Verb><Noun>Port` |
| Query (one per entity) | `<area>/<entity>-query.ts` | `<Entity>QueryPort` with `findOne`, `findMany` |
| Metric (one per entity) | `<area>/<entity>-metric.ts` | `<Entity>MetricPort` with `get` |
| Shared metric types | `metrics.ts` | `Metric`, `MetricsQuery`, `MetricsResult` |

Ports are generic data operations. They never encode a use-case rule in their name or behaviour (no `FindRecentSessionsPort`, `ReplaceSetsPort`): "recent" is a filter or sort the caller passes, "replace" is a use case composing generic ports.

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

Every read of rows (list, detail) goes through the entity's one query port. It has no use case of its own: the controller calls it directly.

- One interface per entity, `<Entity>QueryPort`, with exactly two methods: `findOne` and `findMany`. No `findById`, `findByEmail`, `count` or other per-question methods: a new question is a new filter field, not a new method. Aggregates go in the metric port.
- Both take a single query object. `filter` is the entity's `<Entity>Filter` type (all fields optional, combined with AND). `findMany` adds `sort`, `offset` and `limit`.
- `findOne` returns `null` when nothing matches. The controller maps `null` to the framework's not-found response (no use case to throw `NotFoundError`).
- `findMany` returns a plain array. No `total`: totals come from the metric port, called only when the caller needs them.
- Sort is an array of `{ field, direction }`, with `field` a union of allowed names (relation fields dotted: `'program.name'`). The adapter adds a unique tie-breaker so paging is stable.
- Read-only, no side effects. Mutations belong to command ports.
- No separate read-model types: the port returns the entity. Optional relations use an `include` param, typed so the result only has the relation when it was asked for (`SessionWith<I>`). If the entity already declares the relation, return the entity.
- A command use case may still inject a query port to load what it needs (see `FinishSession`). The guard stays in that use case.
- Guards, state checks and decisions never live in a query port or its controller call: they belong to a command use case.

```ts
import type { WorkoutSession } from 'src/domain/entities/workout-session';
import type { Program } from 'src/domain/entities/program';

export type SessionFilter = {
  ids?: string[];
  programId?: string;
  active?: boolean;
};

export type SessionInclude = { program?: boolean };

export type SessionWith<I extends SessionInclude> = WorkoutSession &
  (I extends { program: true } ? { program: Program } : object);

export type SessionSort = {
  field: 'startedAt' | 'program.name';
  direction: 'asc' | 'desc';
};

export interface SessionQueryPort {
  findOne<I extends SessionInclude = object>(query: {
    filter: SessionFilter;
    include?: I;
  }): Promise<SessionWith<I> | null>;

  findMany<I extends SessionInclude = object>(query: {
    filter: SessionFilter;
    include?: I;
    sort?: SessionSort[];
    offset?: number;
    limit?: number;
  }): Promise<SessionWith<I>[]>;
}
```

## Metric ports

Aggregates (counts, and later sums or averages) go through the entity's one metric port, never the query port. Like query ports, they have no use case.

- One interface per entity, `<Entity>MetricPort`, with one method `get`. It reuses the query port's `<Entity>Filter`, so a list and its total always agree.
- `get` takes `{ filter, metrics, groupBy? }`: `metrics` names the aggregates to compute (only `'count'` until a caller needs more), `groupBy` is one of the entity's allowed group keys.
- It returns `{ totals }`, plus `groups` only when `groupBy` is passed. Each group carries its `key` and the same metrics as `totals`. The result type enforces this, so callers never check for `groups` they did not ask for.
- The shared types live once in `app/ports/metrics.ts`; each metric port only declares its `<Entity>GroupBy` union.

```ts
// app/ports/metrics.ts
export type Metric = 'count';

export type MetricValues<M extends Metric> = { [K in M]: number };

export type MetricsGroup<G extends string, M extends Metric> = MetricValues<M> & {
  key: { [K in G]: string };
};

export type MetricsQuery<F, G extends string | undefined, M extends Metric> = {
  filter: F;
  metrics: M[];
  groupBy?: G;
};

/** Totals over the whole filter, plus one entry per group when grouped. */
export type MetricsResult<G extends string | undefined, M extends Metric> = {
  totals: MetricValues<M>;
} & ([G] extends [string] ? { groups: MetricsGroup<G, M>[] } : object);
```

```ts
// app/ports/sessions/session-metric.ts
export type SessionGroupBy = 'programId';

export interface SessionMetricPort {
  get<G extends SessionGroupBy | undefined = undefined, M extends Metric = Metric>(
    query: MetricsQuery<SessionFilter, G, M>,
  ): Promise<MetricsResult<G, M>>;
}

// totals only:  { totals: { count: 12 } }
await sessionMetricPort.get({ filter: { active: true }, metrics: ['count'] });
// grouped:      { totals: { count: 12 }, groups: [{ key: { programId: 'p1' }, count: 7 }, ...] }
await sessionMetricPort.get({ filter: {}, metrics: ['count'], groupBy: 'programId' });
```

## Use cases

- Class named by verb (`FinishSession`). Constructor takes ports as `private readonly xPort: XPort`. One `async execute(dto)`.
- Export the input as a plain `<Name>Dto` interface from the same file. No framework or validation decorators.
- Flow: load, guard (throw domain error), call entity factory/method, persist via port, return entity.
- Business rules live here or in the entity, never in the controller or adapter.
- Only commands get use cases. Reads are query and metric ports with no use case, see above.
- Test in `test.ts` beside `index.ts`: mock ports, no I/O.

```ts
export interface FinishSessionDto {
  id: string;
}

export class FinishSession {
  constructor(
    private readonly sessionQueryPort: SessionQueryPort,
    private readonly updateSessionPort: UpdateSessionPort,
  ) {}

  async execute({ id }: FinishSessionDto): Promise<WorkoutSession> {
    const session = await this.sessionQueryPort.findOne({ filter: { ids: [id] } });
    if (!session) throw new NotFoundError('SESSION_NOT_FOUND', 'Session not found', { id });

    const finished = session.finish();
    await this.updateSessionPort.execute({ session: finished });
    return finished;
  }
}
```
