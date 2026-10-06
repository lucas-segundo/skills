# Coding

- Use `Map`/`Set` for keyed lookups and dedupe, not objects/arrays scanned repeatedly.

  ```js
  // bad: O(n) scan per lookup, O(n²) dedupe
  const user = users.find((u) => u.id === id);
  const unique = ids.filter((id, i) => ids.indexOf(id) === i);
  // good
  const usersById = new Map(users.map((u) => [u.id, u]));
  const user = usersById.get(id);
  const unique = [...new Set(ids)];
  ```

- Naming: `camelCase` values/functions, `PascalCase` classes, `UPPER_SNAKE` true constants; booleans read as `isX`/`hasX`; functions are verbs.

  ```js
  const MAX_RETRIES = 3;
  class UserService {}
  const isActive = user.status === 'active';
  const fetchUser = (id) => {};
  ```

- Don't create a top-of-file constant (title, label, className, style object, options array, config) that is used once and not exported. Inline it where it is used. Hoist only when it is reused or exported.

  ```js
  // bad: used once, not exported, just adds indirection
  const TIMEOUT_MS = 5000;
  const defaultHeaders = { Accept: 'application/json' };
  export const fetchUser = (id) =>
    fetch(`/users/${id}`, { headers: defaultHeaders, signal: AbortSignal.timeout(TIMEOUT_MS) });
  // good
  export const fetchUser = (id) =>
    fetch(`/users/${id}`, {
      headers: { Accept: 'application/json' },
      signal: AbortSignal.timeout(5000),
    });
  ```

- Prefer arrow functions over `function` declarations and expressions.

  ```js
  // bad
  function add(a, b) {
    return a + b;
  }
  items.map(function (item) {
    return item.id;
  });
  // good
  const add = (a, b) => a + b;
  items.map((item) => item.id);
  ```

- Don't use the `void` operator in front of a call (`void fn()`). Handle the promise instead: `await` it or return it.

  ```js
  // bad: hides a floating promise, rejection goes unhandled
  void saveUser(user);
  // good
  await saveUser(user);
  ```

- Avoid `.then` and `.catch`. Use `async`/`await` with `try`/`catch`.

  ```js
  // bad
  fetchUser(id)
    .then((user) => render(user))
    .catch((err) => logError(err));
  // good
  try {
    const user = await fetchUser(id);
    render(user);
  } catch (err) {
    logError(err);
  }
  ```

- Order code top-down, like a pyramid: the function/class that calls the others goes at the top, then the things it calls, and so on. Readers should see the usage first and scroll down for details. In classes, put public methods before the private methods they use.

  ```js
  // bad: helpers first, usage buried at the bottom
  const parse = (raw) => {};
  const validate = (data) => {};
  export const importUser = (raw) => validate(parse(raw));
  
  // good: entry point first, then its helpers in call order
  export const importUser = (raw) => validate(parse(raw));
  const parse = (raw) => {};
  const validate = (data) => {};
  ```

- Avoid re-exports. Don't import a symbol just to export it again, and don't use `export ... from`. Each symbol has one source of export; consumers import it from where it's defined.

  ```js
  // bad: two places export DEFAULT_DRAFT
  import {
    DEFAULT_DRAFT,
    getScopeDetails,
    type DraftOption,
  } from './draft';

  export { DEFAULT_DRAFT };

  // good: import only what this file uses
  import { getScopeDetails, type DraftOption } from './draft';
  // consumers of DEFAULT_DRAFT import it from './draft'
  ```

- Never create a type or interface identical to another. Use the original directly instead of aliasing it.

  ```ts
  // bad: alias adds a second name for the same shape
  export type RetentionCaseSolutionResponse = RetentionCaseSolutionBase;
  // good: use RetentionCaseSolutionBase directly
  ```
