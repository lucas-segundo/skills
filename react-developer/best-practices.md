# React Best Practices

Examples use TanStack Query and `react-error-boundary`; adapt them to the project's own libraries.

## Data fetching (client side)

Use the project's data-fetching library, never ad-hoc `useEffect` + `useState` fetching. Data hooks must adopt React Suspense (the suspense variant of the library's read hook, no manual `isLoading` branching); the screen wraps the data component in `<Suspense>` with a fallback and an error boundary.

```tsx
// Bad
const [user, setUser] = useState<User>();
const [loading, setLoading] = useState(true);
useEffect(() => {
  getUser(id).then(setUser).finally(() => setLoading(false));
}, [id]);
if (loading) return <Spinner />;

// Good
export function useUser(id: string) {
  return useSuspenseQuery({ queryKey: ['user', id], queryFn: () => getUser(id) });
}

function UserCard({ id }: { id: string }) {
  const { data: user } = useUser(id);
  return <h2>{user.name}</h2>;
}

export function UserScreen({ id }: { id: string }) {
  return (
    <ErrorBoundary fallback={<ErrorState />}>
      <Suspense fallback={<Spinner />}>
        <UserCard id={id} />
      </Suspense>
    </ErrorBoundary>
  );
}
```

## Data fetching (server side, SSR)

Call the API function directly on the server (server components, loaders), with no hook. Handle loading and errors with the framework's mechanisms (streaming `<Suspense>` boundaries, error boundaries).

```tsx
// Use framework's loading.tsx / error.tsx handle the states
export default async function UserPage({ params }: { params: { id: string } }) {
  const user = await getUser(params.id);
  return <h2>{user.name}</h2>;
}
```

## Components

Small, single-purpose, function components. Extract when JSX gets nested or a piece is reused. Keep screens as composition.

```tsx
// Good: the screen reads like an outline
export function OrderScreen({ id }: { id: string }) {
  return (
    <>
      <OrderHeader id={id} />
      <OrderItems id={id} />
      <OrderActions id={id} />
    </>
  );
}
```

## Effects

Avoid them when possible. Use one only for synchronizing with external systems. If an action can be done in a callback (event handler), do it there; if it can be a computed value, derive it during render. Neither is an effect. Always clean up subscriptions/timers.

```tsx
// Bad: reacting to state to run an action
useEffect(() => {
  if (submitted) showToast('Saved');
}, [submitted]);

// Good: do it in the handler that caused it
function handleSubmit() {
  save();
  showToast('Saved');
}

// Good: a real external sync, with cleanup
useEffect(() => {
  const id = setInterval(tick, 1000);
  return () => clearInterval(id);
}, []);
```

## Memoization

Don't add `useMemo`/`useCallback`/`memo` by default. Add them where a measured re-render or a stable-reference requirement (e.g. list item renderers, dependency arrays) justifies it.

```tsx
// Bad: memoizing cheap work
const label = useMemo(() => `Hi ${name}`, [name]);

// Good: stable callback passed to a memoized list item
const handleSelect = useCallback((id: string) => setSelected(id), []);
<MemoizedRow onSelect={handleSelect} />;
```

## Forms/mutations

Disable submit while pending and show a loading state (ask the user how it should look, e.g. spinner on the button or inline indicator, unless the project already has a pattern), surface errors, refresh the affected data on success.

```tsx
const queryClient = useQueryClient();
const { mutate, isPending, error } = useMutation({
  mutationFn: updateUser,
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['user', id] }),
});

<form onSubmit={(e) => { e.preventDefault(); mutate(values); }}>
  {error && <FormError message={error.message} />}
  <button type="submit" disabled={isPending}>
    {isPending ? <Spinner /> : 'Save'}
  </button>
</form>;
```
