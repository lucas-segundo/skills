# Coding

## Style

- Arrow functions over `function` declarations and expressions.
- Named exports over default. No barrel files or re-exports (`export ... from`, or import-then-export); consumers import from the defining file.
- No type or interface that duplicates another. Use the original.
- Name variables and parameters descriptively; no single-letter names, including `e` for an error or event and `i` for an item.

  ```js
  // bad
  const find = (q) => items.filter((i) => i.name.includes(q));
  // good
  const find = (query) => items.filter((item) => item.name.includes(query));
  ```

- Inline a constant (title, className, options, config) used once and not exported. Hoist only when reused or exported. Lookup tables read by a key (`notifiers[channel]`, `messages[code]`) keep their name.

  ```js
  // bad
  const TIMEOUT_MS = 5000;
  export const fetchUser = (id) => fetch(`/users/${id}`, { signal: AbortSignal.timeout(TIMEOUT_MS) });
  // good
  export const fetchUser = (id) => fetch(`/users/${id}`, { signal: AbortSignal.timeout(5000) });
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

- Order top-down: callers first, then what they call. Public class methods before private ones.

## Blank lines

Split a function body into blocks, one per step (load the actor, fetch the main data, fetch extras, shape the output), with one blank line between them. Statements of the same step stay together, and a guard clause (`if (...) return`) stays with the statement it checks. Leave one blank line above the final `return` when other statements precede it; a `return` alone in its block needs none.

```js
// bad
const listOrders = async (filters) => {
  const user = await requireUser();

  if (!user) return [];

  const orders = await findOrders({ ...filters, userId: user.id });
  const ids = orders.map(({ id }) => id);
  const totals = await sumOrderItems(ids);
  return orders.map((order) => ({ ...order, total: totals[order.id] }));
};
// good
const listOrders = async (filters) => {
  const user = await requireUser();
  if (!user) return [];

  const orders = await findOrders({ ...filters, userId: user.id });

  const ids = orders.map(({ id }) => id);
  const totals = await sumOrderItems(ids);

  return orders.map((order) => ({ ...order, total: totals[order.id] }));
};
```

## Design

- Add a case by adding data or a new implementation, not by growing a `switch`/`if` chain.

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

- Take only what you use: accept `{ id, email }` instead of a whole `user`.
- Pass dependencies (clients, repositories, clocks) in as parameters instead of importing concrete ones deep inside business logic. Do not add an abstraction, interface or injection point with only one implementation and no test need for it.

## Async

- `async`/`await` with `try`/`catch`, not `.then`/`.catch`. Await or return every promise; no `void fn()`.
- No `await` inside a loop. Prefer one batch call (`createMany`, `insert ... values (...), (...)`, a bulk endpoint), adding one to the port or repository if missing. Without a batch API, run independent tasks with `Promise.all`, within the limit below. Keep a sequential loop only when each step needs the previous result.

  ```js
  // bad
  for (const guestList of guestLists) {
    await this.createGuestListPort.execute({ guestList });
  }
  // good
  await this.createGuestListsPort.execute({ guestLists });
  ```

- No unbounded `Promise.all` over tasks that each hold a limited resource (pool connection, tunnel, socket, rate-limited API): 10 queries on a 10-connection pool leave none for anyone else. Run them sequentially or with a concurrency cap.

## Errors

Never handle an error with only `console.log`/`console.warn`/`console.error`. A `catch` must act on the failure: undo partial work, show the user an error, redirect them to recover (for example, back to sign-in), retry, or rethrow. If the caller or framework already handles thrown errors, drop the `try`/`catch` and let the error propagate.

```js
// bad
try { await syncUser(user); } catch (error) { console.error('Sync failed', error); }
// good
try { await saveUser(values); } catch (error) { toast.error(error.message); }
```
