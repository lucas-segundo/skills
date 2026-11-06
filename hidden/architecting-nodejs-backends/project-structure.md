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
│   ├── ports/
│   │   ├── metrics.ts                   # shared Metric, MetricsQuery, MetricsResult ({ totals, groups? })
│   │   └── <area>/                      # one folder per entity
│   │       ├── <verb>-<noun>.ts         # command: interface <Verb><Noun>Port { execute(...) }
│   │       ├── <entity>-query.ts        # interface <Entity>QueryPort { findOne, findMany }
│   │       └── <entity>-metric.ts       # interface <Entity>MetricPort { get }
│   └── use-cases/
│       └── <area>/
│           └── <verb>-<noun>/
│               ├── index.ts             # use-case class + exported <Name>Dto interface
│               └── test.ts              # mocks ports, no I/O
│
├── infra/                               # implementations of ports
│   └── <persistence>/                   # e.g. prisma/, drizzle/, in-memory/
│       ├── schema | migrations          # storage definition
│       ├── metrics.ts                   # toMetricsResult helper shared by metric adapters
│       └── <area>/                      # mirrors app/ports/<area>
│           ├── <verb>-<noun>.ts         # <Tech><Verb><Noun>Adapter implements command port
│           ├── <entity>-query.ts        # <Tech><Entity>QueryAdapter
│           ├── <entity>-metric.ts       # <Tech><Entity>MetricAdapter
│           └── <entity>-where.ts        # filter -> where, only when query and metric adapters share it
│
└── main/                                # delivery layer: HTTP + wiring
    ├── app                              # root wiring, registers each area
    ├── index.ts                         # bootstrap (global pipes, filters, listen)
    ├── routes/
    │   └── <area>/
    │       ├── module                   # composition for this area: builds adapters, injects into use cases
    │       ├── controller.ts            # thin: parse, call use case/query port, shape response
    │       ├── controller.spec.ts       # controller built directly with mocks
    │       └── dto/
    │           └── <verb>-<noun>.ts     # request validation, conforms to use-case DTO
    └── shared/                          # cross-area helpers
        ├── domain-exception filter      # domain errors -> HTTP status
        ├── pagination DTO + resolvePagination (page/limit -> offset/limit)
        ├── include helpers              # ?include= allow-list + builder
        └── db client wiring
```

Dependency direction and naming are in the AGENTS.md block in [SKILL.md](SKILL.md); per-layer rules in the layer files.

## Adding an endpoint (checklist)

1. Entity change/factory + unit test if the domain needs it.
2. Port in `app/ports/<area>/` (the entity's folder). For a read, add a filter field, sort field, include or group key to the entity's query or metric port before adding anything new.
3. Use case + test. Skip for reads: the controller calls the query or metric port directly.
4. Adapter (and schema/migration if storage changes).
5. Register in the composition root / DI container.
6. DTO, controller/route handler, wiring.
7. Controller tests. Update API docs (OpenAPI etc.) if the route is documented.
8. Run the project's test and lint scripts.
