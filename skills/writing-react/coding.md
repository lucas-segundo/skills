# Coding

Examples use TanStack Query and `react-error-boundary`; adapt them to the project's own libraries.

## Data fetching (client side)

Use the project's data-fetching library, never ad-hoc `useEffect` + `useState` fetching. Data hooks must adopt React Suspense (the suspense variant of the library's read hook, no manual `isLoading` branching); the screen wraps the data component in `<Suspense>` with a fallback and an error boundary.

```tsx
// Screen first, then the component it renders, then the hook it uses
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

Call the API function directly in server components/loaders, no hook. Use the framework's loading/error mechanisms (streaming `<Suspense>`, `loading.tsx`, `error.tsx`). Default export only where the framework requires it.

## Params over fixed config

Service functions and hooks take options as params (`include`, `filter`, `sort`, `limit`); never hardcode them inside. Include `params` in the `queryKey`. Never pass delimited strings (`"a,b"`); take an array/object and let the service serialize.

```tsx
export const useUser = (id: string, params?: GetUserParams) =>
  useSuspenseQuery({ queryKey: ['user', id, params], queryFn: () => getUser(id, params) });

useUser(id, { include: ['exercises', 'sessions'] }); // not 'exercises,sessions'

const getUser = (id: string, { include, ...rest }: GetUserParams = {}) =>
  api.get(`/users/${id}`, { params: { ...rest, include: include?.join(',') } });
```

## Avoid fetching large data

Never fetch a large collection in one go. Paginate (or infinite scroll) when the API supports it, passing page/limit/cursor as params. If it doesn't, tell the user and leave a `TODO` next to the call.

```tsx
// TODO: no pagination in GET /users, fetches everything. Paginate when the API supports it.
const getUsers = () => api.get('/users');
```

## Backend gaps

Never code the backend. If the frontend needs something it lacks (endpoint, field, behavior), warn the user and leave a `TODO(backend)` next to the call, naming the backend if it is in the workspace.

```tsx
// TODO(backend: orders-api): GET /orders has no `status` filter, filtering client side for now.
const getOrders = () => api.get('/orders');
```

## Backend errors

Never show a backend error as-is. The service maps every error code to a plain-language message (what went wrong, what to do next) and throws an `Error` with it; the UI displays `error.message`. Unknown codes get a generic friendly message, never the raw backend text. If the backend returns no code, warn the user and leave a `TODO(backend)`.

```tsx
const userErrorMessages: Record<string, string> = {
  EMAIL_TAKEN: 'This email is already registered. Try logging in instead.',
  SESSION_EXPIRED: 'Your session ended. Please log in again.',
};

const updateUser = async (id: string, values: UserValues) => {
  try {
    return await api.put(`/users/${id}`, values);
  } catch (e) {
    const code = (e as ApiError).response?.data?.code;
    throw new Error(userErrorMessages[code] ?? 'Something went wrong. Please try again.');
  }
};
```

## Components

Small, single-purpose function components. Extract when JSX nests or a piece is reused. Screens are composition only.

## Avoid large prop lists

Don't build components with many props (rule of thumb: more than ~5), especially value/`onChange` pairs per field. Group related data into one object prop plus a single change handler, or use another strategy: context, composition (`children`/slots), or a form library.

```tsx
// Bad: one value prop and one handler per field
<AllowanceFields
  hasInstallmentAllowance={draft.hasInstallmentAllowance}
  installmentAllowanceAmount={draft.installmentAllowanceAmount}
  annualDiscountAmount={draft.annualDiscountAmount}
  financeObservation={draft.financeObservation}
  onHasInstallmentAllowanceChange={(hasInstallmentAllowance) => updateDraft({ hasInstallmentAllowance })}
  onInstallmentAllowanceAmountChange={(installmentAllowanceAmount) => updateDraft({ installmentAllowanceAmount })}
  onAnnualDiscountAmountChange={(annualDiscountAmount) => updateDraft({ annualDiscountAmount })}
  onFinanceObservationChange={(financeObservation) => updateDraft({ financeObservation })}
/>

// Good: one object, one patch handler
<AllowanceFields value={draft} onChange={updateDraft} />

const AllowanceFields = ({ value, onChange }: { value: Draft; onChange: (patch: Partial<Draft>) => void }) => (
  <input
    value={value.financeObservation}
    onChange={(e) => onChange({ financeObservation: e.target.value })}
  />
);
```

## Lazy-mount hidden components

Components that start hidden (modal, drawer, popover, tab) stay out of the initial bundle. Load them with the framework's lazy strategy if it has one (e.g. `next/dynamic` in Next.js), else `React.lazy`. Mount it only once first needed (`&&` inside `<Suspense>`), then keep it mounted and toggle an `open` prop so exit animations play. One state: `undefined` = never shown, then `true`/`false`.

```tsx
const EditDialog = lazy(() => import('./EditDialog'));

const [open, setOpen] = useState<boolean>();

<button onClick={() => setOpen(true)}>Edit</button>
{open !== undefined && (
  <Suspense fallback={null}>
    <EditDialog open={open} onClose={() => setOpen(false)} />
  </Suspense>
)}
```

With `next/dynamic`, use `dynamic(() => import('./EditDialog'))` and its `loading` option instead of `<Suspense>`. Named export: `lazy(() => import('./EditDialog').then((m) => ({ default: m.EditDialog })))`.

## No ternary chains for conditional rendering

Don't chain ternaries to pick render branches (error/loading/empty/data). Extract a component with early returns.

```tsx
const UnitsList = ({ isError, isLoading, isEmpty, items }: UnitsListProps) => {
  if (isError) return <ErrorMsg />;
  if (isLoading) return <Skeleton />;
  if (isEmpty) return <EmptyMsg />;
  return <List items={items} />;
};
```

## Mapped items

Never inline a big JSX body (handlers, hooks, derived values) in `.map`. Extract a row component that takes the item and derives the rest; the parent keeps only sort/filter and the map. Per-row hooks (e.g. a mutation) scope state like `isPending` to that row.

```tsx
{items.map((item) => <ItemRow key={item.id} item={item} logged={countFor(item.id)} />)}
```

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

No `useMemo`/`useCallback`/`memo` by default. Add only for a measured re-render or a required stable reference (memoized list rows, dependency arrays).

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
