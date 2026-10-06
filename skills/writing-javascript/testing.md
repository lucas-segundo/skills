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
