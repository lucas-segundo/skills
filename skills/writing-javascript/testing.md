# Testing

- Test each rule once, in the unit that owns it. Callers test only their own logic.

  ```js
  // bad: CreateUser only builds a User; User's own test covers name validation
  test('CreateUser throws when name is null', async () => {
    await expect(createUser.execute({ name: null })).rejects.toThrow();
  });
  // good
  test('CreateUser saves the user', async () => {
    await createUser.execute({ name: 'Ana' });
    expect(userRepository.save).toHaveBeenCalledTimes(1);
  });
  ```

- **Test behavior, not implementation.** Assert what the caller experiences when it runs a method: the returned value, the state change, the side effect (a saved record, a request made). Do not assert that a constructor stored a prop, or inspect private fields and internal helpers.
- **Keep mocks out of the test file.** If a test needs many mocks, define them in a `mock` file next to it and import them, so the test file stays focused on behavior.

```js
// Bad: asserts the constructor stored its prop
test('stores the balance', () => {
  const account = new Account({ balance: 100 });
  expect(account.balance).toBe(100);
});

// Good: the method does what it promises
test('withdraw reduces the balance', () => {
  const account = new Account({ balance: 100 });
  account.withdraw(30);
  expect(account.balance).toBe(70);
});

// Good: the method rejects invalid input
test('withdraw throws when funds are insufficient', () => {
  const account = new Account({ balance: 20 });
  expect(() => account.withdraw(30)).toThrow();
});
```
