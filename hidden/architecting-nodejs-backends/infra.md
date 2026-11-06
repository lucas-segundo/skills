# Infra Layer

`src/infra/` implements the ports declared in `app/ports`. It is the only layer that knows the ORM, query builder, or driver. Swapping persistence means swapping this folder.

## Folders

Adapters mirror the port folders: `infra/<tech>/<area>/`, one folder per entity, same file name as the port.

```
infra/<tech>/
├── metrics.ts                     # toMetricsResult: rows -> { totals, groups? }
└── sessions/
    ├── update-session.ts          # <Tech>UpdateSessionAdapter
    ├── session-query.ts           # <Tech>SessionQueryAdapter
    ├── session-metric.ts          # <Tech>SessionMetricAdapter
    └── session-where.ts           # filter -> where clause, shared by query and metric adapters
```

## Adapters

- One per port, `implements` that port. Names: `<Tech><Verb><Noun>Adapter` for commands (`PrismaUpdateSessionAdapter`), `<Tech><Entity>QueryAdapter` and `<Tech><Entity>MetricAdapter` for reads.
- Receives the DB client through the constructor.
- Maps rows explicitly. Never leaks ORM or driver types out. Always build domain entities or the port's declared shape; included relations are attached under their name.
- Stateless. Adapters are shared singletons: never store per-call results on adapter fields, it is a race.

## Query adapters

- `findOne` and `findMany` share their query building in private methods (`selection(include)`, joins, sort mapping). Never copy it between the two methods.
- The filter -> where clause lives in one place. When only the query adapter uses it, a private method; when the metric adapter needs it too, a helper beside them (`<entity>-where.ts`). Both adapters then filter the same way, so a list and its count always agree.
- Join a relation only when it is included, filtered on, or sorted on.
- Paging: `offset` and `limit` passed straight through, explicit `orderBy` from `sort` plus the primary key as tie-breaker.

```ts
export class PostgresSessionQueryAdapter implements SessionQueryPort {
  constructor(private readonly db: DbClient) {}

  async findOne<I extends SessionInclude = object>({ filter, include }: { filter: SessionFilter; include?: I }) {
    const [row] = await this.baseQuery(filter, include).limit(1);

    return row ? this.toSession<I>(row) : null;
  }

  async findMany<I extends SessionInclude = object>({ filter, include, sort = [], offset, limit }: FindManyQuery<I>) {
    const rows = await this.baseQuery(filter, include)
      .orderBy(...sort.map(({ field, direction }) => [sortColumns[field], direction]), sessions.id)
      .offset(offset)
      .limit(limit);

    return rows.map((row) => this.toSession<I>(row));
  }

  private baseQuery(filter: SessionFilter, include?: SessionInclude) {
    return this.db.select(this.selection(include)).from(sessions).where(sessionWhere(filter));
  }

  private selection(include?: SessionInclude) { /* entity columns, plus relation columns when included */ }

  private toSession<I extends SessionInclude>(row: SessionRow): SessionWith<I> { /* row -> entity */ }
}
```

## Metric adapters

- One `get`, one aggregate query: `count()` (and other metrics) over the shared where clause, `GROUP BY` the group key column when `groupBy` is passed.
- Build the result with the shared `toMetricsResult(groupBy, rows)` helper (`infra/<tech>/metrics.ts`): `totals` is the sum of the rows, `groups` is added only when grouped. Test it once, not per adapter.
- Short-circuit filters that can match nothing (an empty `ids: []`) without hitting the database.

```ts
const groupColumns = { programId: sessions.programId };

export class PostgresSessionMetricAdapter implements SessionMetricPort {
  constructor(private readonly db: DbClient) {}

  async get<G extends SessionGroupBy | undefined = undefined, M extends Metric = Metric>({
    filter,
    groupBy,
  }: MetricsQuery<SessionFilter, G, M>): Promise<MetricsResult<G, M>> {
    if (filter.ids?.length === 0) return toMetricsResult(groupBy, []);

    const key = groupBy ? groupColumns[groupBy] : undefined;
    const query = this.db
      .select(key ? { key, count: count() } : { count: count() })
      .from(sessions)
      .where(sessionWhere(filter));
    if (key) query.groupBy(key);

    return toMetricsResult(groupBy, await query);
  }
}
```
