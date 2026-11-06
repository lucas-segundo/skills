# Coding

- Use `Map`/`Set` for keyed lookups and dedupe, not repeated scans of arrays/objects.

  ```js
  const usersById = new Map(users.map((user) => [user.id, user]));
  const unique = [...new Set(ids)];
  ```

- Name variables and parameters descriptively; no single-letter names (`q` for `query`, `u` for `user`, `e` for `error`).

  ```js
  // bad
  const find = (q) => items.filter((i) => i.name.includes(q));
  // good
  const find = (query) => items.filter((item) => item.name.includes(query));
  ```

- Inline a constant (title, className, options, config) used once and not exported. Hoist only when reused or exported.

  ```js
  // bad
  const TIMEOUT_MS = 5000;
  export const fetchUser = (id) => fetch(`/users/${id}`, { signal: AbortSignal.timeout(TIMEOUT_MS) });
  // good
  export const fetchUser = (id) => fetch(`/users/${id}`, { signal: AbortSignal.timeout(5000) });
  ```

- Leave one blank line above the final `return` of a block that follows other statements. Guard clauses (`if (...) return`) stay grouped with the statements before them, and a `return` alone in its block needs none.

  ```js
  // bad
  const syncUser = async (identity) => {
    const existing = await findUser(identity.externalId);

    if (!existing) return createUser(identity);

    if (existing.hasIdentity(identity)) return existing;
    return updateUser(existing.id, identity);
  };
  // good
  const syncUser = async (identity) => {
    const existing = await findUser(identity.externalId);
    if (!existing) return createUser(identity);
    if (existing.hasIdentity(identity)) return existing;

    return updateUser(existing.id, identity);
  };
  ```

- Write conditions without `!` when you can. If both branches return, test the positive case first. Keep `!` for guard clauses that throw or exit early before the main logic.

  ```js
  // bad
  if (!lastSave) {
    return { title: 'Discard this event?', save: 'Save draft and leave' };
  }

  return { title: 'Discard changes?', save: 'Save and leave' };
  // good
  if (lastSave) {
    return { title: 'Discard changes?', save: 'Save and leave' };
  }

  return { title: 'Discard this event?', save: 'Save draft and leave' };
  ```

- Split a function body that does several steps (load the actor, fetch the main data, fetch extras, shape the output) into blocks, one blank line between each. Statements of the same step stay together, and a guard clause stays with the statement it checks.

  ```js
  // bad
  const listOrders = async (filters) => {
    const user = await requireUser();
    const orders = await findOrders({ ...filters, userId: user.id });
    const total = await countOrders({ ...filters, userId: user.id });
    const ids = orders.map(({ id }) => id);
    const totals = await sumOrderItems(ids);
    const items = orders.map((order) => ({ ...order, total: totals[order.id] }));

    return { items, total };
  };
  // good
  const listOrders = async (filters) => {
    const user = await requireUser();

    const orders = await findOrders({ ...filters, userId: user.id });
    const total = await countOrders({ ...filters, userId: user.id });

    const ids = orders.map(({ id }) => id);
    const totals = await sumOrderItems(ids);

    const items = orders.map((order) => ({ ...order, total: totals[order.id] }));

    return { items, total };
  };
  ```

- Follow SOLID, applied to modules and functions as well as classes:
  - Single responsibility: one reason to change per function, module or class. Split one that mixes concerns (fetching, business rules, formatting, I/O).
  - Open/closed: add a case by adding data or a new implementation, not by editing a growing `switch`/`if` chain.
  - Liskov substitution: an implementation of a shared contract accepts the same inputs, returns the same shape and throws the same errors as the others.
  - Interface segregation: take only what you use. Accept `{ id, email }` instead of a whole `user`; keep interfaces small.
  - Dependency inversion: pass dependencies (clients, repositories, clocks) in as parameters instead of importing concrete ones deep inside business logic.

  Do not add an abstraction, interface or injection point with only one implementation and no test need for it.

  ```js
  // bad
  const notify = async (user, channel) => {
    if (channel === 'email') return sendEmail(user.email, 'Welcome');
    if (channel === 'sms') return sendSms(user.phone, 'Welcome');
  };
  // good
  const notifiers = {
    email: ({ email }) => sendEmail(email, 'Welcome'),
    sms: ({ phone }) => sendSms(phone, 'Welcome'),
  };
  const notify = (user, channel) => notifiers[channel](user);
  ```

- Arrow functions over `function` declarations and expressions.
- `async`/`await` with `try`/`catch`, not `.then`/`.catch`.
- Await or return every promise; no `void fn()`.
- No `await` inside a loop. Prefer one batch call (`createMany`, `insert ... values (...), (...)`, a bulk endpoint); add one to the port or repository if missing. Without a batch API, run independent tasks together with `Promise.all`, within the limit below. Keep a sequential loop only when each step needs the previous result.

  ```js
  // bad
  await this.unitOfWorkPort.run(async () => {
    await this.createEventPort.execute({ event });
    for (const guestList of guestLists) {
      await this.createGuestListPort.execute({ guestList });
    }
  });
  // good
  await this.unitOfWorkPort.run(async () => {
    await this.createEventPort.execute({ event });
    await this.createGuestListsPort.execute({ guestLists });
  });
  ```

- No unbounded `Promise.all` over tasks that each hold a limited resource (pool connection, tunnel, socket, rate-limited API). N tasks at once can exhaust the limit in one call: 10 queries on a 10-connection pool leave none for anyone else. Run them sequentially or with a concurrency cap.

  ```js
  // bad
  const [user, orders, invoices] = await Promise.all([
    db.query('SELECT * FROM users WHERE id = $1', [userId]),
    db.query('SELECT * FROM orders WHERE user_id = $1', [userId]),
    db.query('SELECT * FROM invoices WHERE user_id = $1', [userId]),
  ]);
  // good
  const user = await db.query('SELECT * FROM users WHERE id = $1', [userId]);
  const orders = await db.query('SELECT * FROM orders WHERE user_id = $1', [userId]);
  const invoices = await db.query('SELECT * FROM invoices WHERE user_id = $1', [userId]);
  ```
- Never handle an error with only `console.log`/`console.warn`/`console.error`. A `catch` must act on the failure: undo partial work, show the user an error, redirect them to recover (for example, back to sign-in), retry, or rethrow. If the caller or framework already handles thrown errors, drop the `try`/`catch` and let the error propagate.

  ```js
  // bad
  try { await syncUser(user); } catch (error) { console.error('Sync failed', error); }
  // good: the auth callback fails and sends the user back to sign in
  handleCallbackRoute({ onSuccess: ({ user }) => syncUser(user), errorRedirectUrl: '/' });
  // good
  try { await saveUser(values); } catch (error) { toast.error(error.message); }
  ```

- Order top-down: callers first, then what they call. Public class methods before private ones.

  ```js
  export const importUser = (raw) => validate(parse(raw));
  const parse = (raw) => {};
  const validate = (data) => {};
  ```

- No re-exports (`export ... from`, or import-then-export). Consumers import from the defining file.
- No type or interface that duplicates another. Use the original.
- Never write `TODO` in code. If work would be left unfinished, warn the user in the response and ask for confirmation on whether to finish it.
