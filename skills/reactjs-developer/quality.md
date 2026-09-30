# Quality

- **Test behavior, not markup.** In component tests, assert what the user experiences: loading, empty, or error states showing up, an element appearing or disappearing, a success toast after an action, data being fetched after a click. Do not assert that a component renders a given prop, text literal, class, or style.
- **Keep mocks out of the test file.** If a test needs to mock components, define the mocks in a `mock.tsx` next to it and import them into `test.tsx`, so the test file stays focused on behavior.

```tsx
// Bad: asserts a prop or class is rendered
it('renders the title', () => {
  render(<UserCard title="Ana" />);
  expect(screen.getByText('Ana')).toBeInTheDocument();
});

// Good: loading state, then data
it('shows a spinner while loading, then the users', async () => {
  render(<UserList />);
  expect(screen.getByRole('progressbar')).toBeInTheDocument();
  expect(await screen.findByText('Ana')).toBeInTheDocument();
  expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
});

// Good: action triggers a request and a success toast
it('saves the form and shows a success toast', async () => {
  const user = userEvent.setup();
  render(<ProfileForm />);
  await user.click(screen.getByRole('button', { name: /save/i }));
  expect(await screen.findByText(/saved successfully/i)).toBeInTheDocument();
});
```
