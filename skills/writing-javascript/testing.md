# Testing

- Don't re-test behavior that another unit already covers in its own test. Test each rule once, in the unit that owns it. Callers only test their own logic.

  ```js
  // User's constructor throws when name is empty, and User's own unit test covers it.
  test('User throws when name is null', () => {
    expect(() => new User({ name: null })).toThrow();
  });

  // bad: CreateUser only builds a User, so this re-tests User's name validation
  test('CreateUser throws when name is null', async () => {
    await expect(createUser.execute({ name: null })).rejects.toThrow();
  });

  // good: tests what CreateUser itself does
  test('CreateUser saves the user', async () => {
    await createUser.execute({ name: 'Ana' });
    expect(userRepository.save).toHaveBeenCalledTimes(1);
  });
  ```
