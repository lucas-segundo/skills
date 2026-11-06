# Coding

Examples use TanStack Query and `react-error-boundary`; adapt them to the project's own libraries.

## Data fetching

Use the project's data-fetching library, never ad-hoc `useEffect` + `useState` fetching. Data hooks use the library's suspense variant, with no manual `isLoading` branching; the screen wraps the data component in `<Suspense>` and an error boundary. Server components and loaders call the API function directly.

```tsx
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
```

Service functions and hooks take options as params (`include`, `filter`, `sort`, `limit`), never hardcoded inside, and include them in the `queryKey`. Take arrays/objects, never delimited strings (`"a,b"`); the service serializes.

```tsx
export const useUser = (id: string, params?: GetUserParams) =>
  useSuspenseQuery({ queryKey: ['user', id, params], queryFn: () => getUser(id, params) });

useUser(id, { include: ['exercises', 'sessions'] });

const getUser = (id: string, { include, ...rest }: GetUserParams = {}) =>
  api.get(`/users/${id}`, { params: { ...rest, include: include?.join(',') } });
```

## Let the backend do the work

- Never fetch a large collection in one go. Paginate (or infinite scroll), passing page/limit/cursor as params.
- Don't filter, search or sort fetched data on the client; pass the criteria as params. Filtering a partial page misses matches beyond it.

  ```tsx
  // bad: misses matches beyond the first 10
  const { data: sessions } = useSessions({ limit: 10 });
  const inProgress = sessions.data.some((session) => session.programId === programId && session.status === 'in_progress');
  // good
  const { data: sessions } = useSessions({ programId, status: 'in_progress', limit: 1 });
  const inProgress = sessions.data.length > 0;
  ```

- Never code the backend.

When the backend can't do one of these (no pagination, no filter, a missing endpoint or field, errors without a code), warn the user, naming the backend if it is in the workspace, and ask whether to work around it on the frontend. Don't work around it silently.

## Backend errors

Never show a backend error as-is. The service maps every error code to a plain-language message (what went wrong, what to do next) and throws an `Error` with it; the UI displays `error.message`. Unknown codes get a generic friendly message.

```tsx
const userErrorMessages: Record<string, string> = {
  EMAIL_TAKEN: 'This email is already registered. Try logging in instead.',
  SESSION_EXPIRED: 'Your session ended. Please log in again.',
};

const updateUser = async (id: string, values: UserValues) => {
  try {
    return await api.put(`/users/${id}`, values);
  } catch (error) {
    const code = (error as ApiError).response?.data?.code;
    throw new Error(userErrorMessages[code] ?? 'Something went wrong. Please try again.');
  }
};
```

## Components

- Extract a component when JSX nests or a piece is reused. Screens are composition only.
- No more than ~5 props, and no value/`onChange` pair per field. Group related data into one object prop with one patch handler, or use context, composition (`children`/slots) or a form library.

  ```tsx
  // bad
  <AllowanceFields
    annualDiscountAmount={draft.annualDiscountAmount}
    financeObservation={draft.financeObservation}
    onAnnualDiscountAmountChange={(annualDiscountAmount) => updateDraft({ annualDiscountAmount })}
    onFinanceObservationChange={(financeObservation) => updateDraft({ financeObservation })}
  />
  // good
  <AllowanceFields value={draft} onChange={updateDraft} />
  ```

- Don't chain ternaries to pick render branches (error/loading/empty/data). Extract a component with early returns.

  ```tsx
  const UnitsList = ({ isError, isLoading, isEmpty, items }: UnitsListProps) => {
    if (isError) return <ErrorMsg />;
    if (isLoading) return <Skeleton />;
    if (isEmpty) return <EmptyMsg />;

    return <List items={items} />;
  };
  ```

- Never inline a big JSX body (handlers, hooks, derived values) in `.map`. Extract a row component that takes the item and derives the rest; the parent keeps only sort/filter and the map. Per-row hooks scope state like `isPending` to that row.

## Lazy-mount hidden components

Components that start hidden (modal, drawer, popover, tab) stay out of the initial bundle. Load them with the framework's lazy strategy if it has one (`next/dynamic` and its `loading` option in Next.js), else `React.lazy`. Mount only once first needed, then keep mounted and toggle an `open` prop so exit animations play. One state: `undefined` = never shown, then `true`/`false`.

```tsx
const EditDialog = lazy(() => import('./EditDialog').then((module) => ({ default: module.EditDialog })));

const [open, setOpen] = useState<boolean>();

<button onClick={() => setOpen(true)}>Edit</button>
{typeof open === 'boolean' && (
  <Suspense fallback={null}>
    <EditDialog open={open} onClose={() => setOpen(false)} />
  </Suspense>
)}
```

## Effects

Use an effect only to sync with an external system. Run actions in the event handler that caused them and derive computed values during render.

## Forms and mutations

Disable submit while pending with a loading state. Unless the project already has a pattern, ask the user how it should look (spinner on the button, inline indicator). Show the error and invalidate the affected queries on success.
