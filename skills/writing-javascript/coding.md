# Coding

- Use `Map`/`Set` for keyed lookups and dedupe, not repeated scans of arrays/objects.

  ```js
  const usersById = new Map(users.map((u) => [u.id, u]));
  const unique = [...new Set(ids)];
  ```

- Inline a constant (title, className, options, config) used once and not exported. Hoist only when reused or exported.

  ```js
  // bad
  const TIMEOUT_MS = 5000;
  export const fetchUser = (id) => fetch(`/users/${id}`, { signal: AbortSignal.timeout(TIMEOUT_MS) });
  // good
  export const fetchUser = (id) => fetch(`/users/${id}`, { signal: AbortSignal.timeout(5000) });
  ```

- Arrow functions over `function` declarations and expressions.
- `async`/`await` with `try`/`catch`, not `.then`/`.catch`.
- Await or return every promise; no `void fn()`.
- A `catch` acts on the failure (undo partial work, show the user an error, retry, rethrow). Logging alone loses it; if logging is the only option, tell the user.

  ```js
  // bad
  try { await SplashScreen.hideAsync(); } catch (error) { console.warn(error); }
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
