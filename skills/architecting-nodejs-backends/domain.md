# Domain Layer

`src/domain/` is the business core. It holds the entities and the errors that describe what the business allows. It imports nothing outward: no `app`, `infra`, `main`, framework, ORM, or validation library.

## Entities

- Class with `readonly` constructor params (immutable). Name is the domain noun, PascalCase (`WorkoutSession`).
- A static factory (`create`, `start`, ...) validates input and generates id and timestamps. The constructor stays dumb: it is used to rehydrate from storage.
- State changes return a new instance, never mutate.
- Derived state is exposed as getters.
- Invariants are enforced here by throwing domain errors. Message format: `'<Entity> <field> cannot be empty'`.
- Unit test lives next to the entity.

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

## Domain errors

- One abstract `DomainError` extends `Error`. Generic kinds extend it: `NotFoundError`, `ConflictError`, `ValidationError`. Add a kind only when the boundary must react differently (e.g. `ForbiddenError`). Never one class per entity or rule.
- Every error carries a `code`: a stable `UPPER_SNAKE` string identifying the failure for clients (`SESSION_NOT_FOUND`). Codes are a public contract: never rename or reuse one. Declare each once, as a constant in `errors.ts` or beside the entity that raises it.
- Every error carries `meta`: a plain, serializable object with the facts behind the message (missing id, conflicting field and value). Keep `message` human-readable and stable; put variable data in `meta`.
- `meta` holds data only. No entities, ORM rows, or stack traces.
- Errors know nothing about HTTP, logging, or i18n. The delivery layer (`main`) maps kind to status.

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
```
