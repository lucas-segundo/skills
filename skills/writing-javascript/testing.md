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

- Assert what a method does (returned value, state change, side effect), never that a constructor stored a prop or what private fields and internal helpers hold.

  ```js
  // bad
  test('stores the balance', () => {
    expect(new Account({ balance: 100 }).balance).toBe(100);
  });
  // good
  test('withdraw reduces the balance', () => {
    const account = new Account({ balance: 100 });
    account.withdraw(30);

    expect(account.balance).toBe(70);
  });
  ```

- When a test needs many mocks, define them in a `mock` file next to it and import them.
