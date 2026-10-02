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
│   ├── pagination.ts                    # Pagination, resolvePagination (Paginated<T> only if totals are requested)
│   ├── ports/
│   │   └── <area>/
│   │       └── <verb>-<noun>.ts         # interface <Verb><Noun>Port { execute(...) }
│   └── use-cases/
│       └── <area>/
│           └── <verb>-<noun>/
│               ├── index.ts             # use-case class + exported <Name>Dto interface
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
    │       ├── controller.ts            # thin: parse, call use case/query port, shape response
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
- Cross-layer imports use the project's absolute alias; relative paths only within the same folder. No barrel files.

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

## Layers

Each layer has its own file with role, rules and examples:

- [domain.md](domain.md): entities and domain errors.
- [app.md](app.md): ports and use cases.
- [infra.md](infra.md): adapters.
- [main.md](main.md): controllers, DTOs, error mapping and wiring.

## Adding an endpoint (checklist)

1. Entity change/factory + unit test if the domain needs it.
2. Port in `app/ports/<area>/`.
3. Use case + test. Skip for pure read (query) ports: the controller calls the port directly.
4. Adapter (and schema/migration if storage changes).
5. Register in the composition root / DI container.
6. DTO, controller/route handler, wiring.
7. Controller tests. Update API docs (OpenAPI etc.) if the route is documented.
8. Run the project's test and lint scripts.
