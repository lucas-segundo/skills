# Quality

- **Test behavior, not markup.** In component tests, assert what the user experiences: loading, empty, or error states showing up, an element appearing or disappearing, a success toast after an action, data being fetched after a click. Do not assert that a component renders a given prop, text literal, class, or style.
- **Keep mocks out of the test file.** If a test needs to mock components, define the mocks in a `mock.tsx` next to it and import them into `test.tsx`, so the test file stays focused on behavior.

```tsx
// Bad: only checks that a prop or style is rendered
it('renders the title', () => {
  render(<UserCard title="Ana" />);
  expect(screen.getByText('Ana')).toBeInTheDocument();
});
it('has the active class', () => {
  render(<Tab active />);
  expect(screen.getByRole('tab')).toHaveClass('active');
});

// Good: loading state, then data
it('shows a spinner while loading, then the users', async () => {
  render(<UserList />);
  expect(screen.getByRole('progressbar')).toBeInTheDocument();
  expect(await screen.findByText('Ana')).toBeInTheDocument();
  expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
});

// Good: empty state
it('shows the empty state when there are no users', async () => {
  server.use(http.get('/users', () => HttpResponse.json([])));
  render(<UserList />);
  expect(await screen.findByText(/no users/i)).toBeInTheDocument();
});

// Good: action triggers a request and a success toast
it('saves the form and shows a success toast', async () => {
  const user = userEvent.setup();
  render(<ProfileForm />);
  await user.click(screen.getByRole('button', { name: /save/i }));
  expect(await screen.findByText(/saved successfully/i)).toBeInTheDocument();
});

// Good: click loads more data
it('loads more users after clicking "Load more"', async () => {
  const user = userEvent.setup();
  render(<UserList />);
  await user.click(await screen.findByRole('button', { name: /load more/i }));
  expect(await screen.findByText('Bruno')).toBeInTheDocument();
});
```
