# React Best Practices

Examples use TanStack Query and `react-error-boundary`; adapt them to the project's own libraries.

## Data fetching (client side)

Use the project's data-fetching library, never ad-hoc `useEffect` + `useState` fetching. Data hooks must adopt React Suspense (the suspense variant of the library's read hook, no manual `isLoading` branching); the screen wraps the data component in `<Suspense>` with a fallback and an error boundary.

```tsx
// Bad
const [user, setUser] = useState<User>();
const [loading, setLoading] = useState(true);
useEffect(() => {
  const load = async () => {
    try {
      setUser(await getUser(id));
    } finally {
      setLoading(false);
    }
  };
  load();
}, [id]);
if (loading) return <Spinner />;

// Good: screen first, then the component it renders, then the hook it uses
export const UserScreen = ({ id }: { id: string }) => (
  <ErrorBoundary fallback={<ErrorState />}>
    <Suspense fallback={<Spinner />}>
      <UserCard id={id} />
    </Suspense>
  </ErrorBoundary>
);

const UserCard = ({ id }: { id: string }) => {
  const { data: user } = useUser(id);
  return <h2>{user.name}</h2>;
};

export const useUser = (id: string) =>
  useSuspenseQuery({ queryKey: ['user', id], queryFn: () => getUser(id) });
```

## Data fetching (server side, SSR)

Call the API function directly on the server (server components, loaders), with no hook. Handle loading and errors with the framework's mechanisms (streaming `<Suspense>` boundaries, error boundaries).

```tsx
// Use framework's loading.tsx / error.tsx handle the states
const UserPage = async ({ params }: { params: { id: string } }) => {
  const user = await getUser(params.id);
  return <h2>{user.name}</h2>;
};

// default export only because the framework requires it for pages
export default UserPage;
```

## Params over fixed config

Service functions and hooks take options as params, never hardcode fixed config (query-string `include`, `filter`, `sort`, `limit`, etc.) inside. Each caller decides what it needs; the service only forwards it. Defaults are fine only when every caller truly wants them.

```tsx
// Bad: every caller is stuck with the same include/filter
const getUser = (id: string) =>
  api.get(`/users/${id}`, { params: { include: 'posts', status: 'active' } });

// Good: caller passes what it needs
export const useUser = (id: string, params?: GetUserParams) =>
  useSuspenseQuery({
    queryKey: ['user', id, params],
    queryFn: () => getUser(id, params),
  });

const getUser = (id: string, params?: GetUserParams) =>
  api.get(`/users/${id}`, { params });
```

Include `params` in the `queryKey` so different params cache separately.

Never pass params as a delimited string (`"exercises,sessions"`); that leaks the query-string format into callers. Take an array or object and let the service serialize it.

```tsx
// Bad
useUser(id, 'exercises,sessions');

// Good
useUser(id, { include: ['exercises', 'sessions'] });

// service serializes
const getUser = (id: string, { include, ...rest }: GetUserParams = {}) =>
  api.get(`/users/${id}`, { params: { ...rest, include: include?.join(',') } });
```

## Avoid fetching large data

Never fetch a large collection in one go. Prefer pagination (or infinite scroll) when the API supports it, and pass page/limit/cursor as params. If the API has no pagination, tell the user and leave a `TODO` in the code next to the call.

```tsx
// Good: API paginates, caller controls the page
export const useUsers = (params: { page: number; limit: number }) =>
  useSuspenseQuery({
    queryKey: ['users', params],
    queryFn: () => getUsers(params),
  });

// API has no pagination: fetch all, flag it, and tell the user
// TODO: no pagination in GET /users, fetches everything. Paginate when the API supports it.
const getUsers = () => api.get('/users');
```

## Components

Small, single-purpose, function components. Extract when JSX gets nested or a piece is reused. Keep screens as composition.

```tsx
// Good: the screen reads like an outline
export const OrderScreen = ({ id }: { id: string }) => (
  <>
    <OrderHeader id={id} />
    <OrderItems id={id} />
    <OrderActions id={id} />
  </>
);
```

## Order code top-down

Order code top-down, like a pyramid: the component that renders the others goes at the top, then the components it renders, then the hooks and helpers they use. Readers should see the usage first and scroll down for details.

```tsx
// Good: screen, then its pieces, then the hook
export const OrderScreen = ({ id }: { id: string }) => (
  <>
    <OrderHeader id={id} />
    <OrderItems id={id} />
  </>
);

const OrderHeader = ({ id }: { id: string }) => {
  const { data: order } = useOrder(id);
  return <h2>{order.name}</h2>;
};

const OrderItems = ({ id }: { id: string }) => {/* ... */};

export const useOrder = (id: string) => useSuspenseQuery(/* ... */);
```

## Mapped items

Never inline a big JSX body (handlers, hooks calls, derived values) inside `.map`. Extract a component that receives the item as a prop and derives the rest itself. The parent keeps only the sort/filter and the map.

```tsx
// Bad: logic and layout buried in the map callback
{items.map((item) => {
  const full = countFor(item.id) >= item.target;
  return (
    <View key={item.id}>
      {/* ...lots of JSX, handlers, styles... */}
    </View>
  );
})}

// Good: the map only composes
{items.map((item) => (
  <ItemRow key={item.id} item={item} logged={countFor(item.id)} />
))}

const ItemRow = ({ item, logged }: ItemRowProps) => {
  const full = logged >= item.target;
  return <View>{/* ... */}</View>;
};
```

Per-row hooks (e.g. a mutation) inside the row component scope state like `isPending` to that row. Pass the hook result from the parent only if rows must share it.

## Effects

Avoid them when possible. Use one only for synchronizing with external systems. If an action can be done in a callback (event handler), do it there; if it can be a computed value, derive it during render. Neither is an effect. Always clean up subscriptions/timers.

```tsx
// Bad: reacting to state to run an action
useEffect(() => {
  if (submitted) showToast('Saved');
}, [submitted]);

// Good: do it in the handler that caused it
const handleSubmit = () => {
  save();
  showToast('Saved');
};

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
