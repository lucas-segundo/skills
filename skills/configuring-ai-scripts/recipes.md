# Recipes

Verified with Biome 2.5, Jest 30.5 and Vitest 5.0.

## Biome

`lint:ai`: `biome check --reporter=concise --max-diagnostics=none`. Add `--write` for *Fix first*.

- Prints one line per problem, then `Checked N files`. `--max-diagnostics=none` lifts the default cap of 20 problems.
- In check-only mode, a format problem has no line number. Fix it with `biome check --write <file>`.
- No `concise` in `biome check --help` (older Biome): no script.

## ESLint

No script. ESLint has no built-in compact formatter, and its default output already lists only problems.

## Jest ≥ 30.3

| Script | Command |
|---|---|
| `test:ai` | `jest --reporters=agent --ci` |
| `test:ai:coverage` | `jest --reporters=agent --coverage --coverageReporters=text-summary --ci` |

- `agent` prints only failing files (including suites that fail to load), then the totals.
- `--ci` fails on a missing snapshot instead of writing it. It must come last: `--reporters` swallows a file passed after it.
- No gaps table: `skipFull` needs a config file.
- Older Jest: no script. Suggest upgrading, since `--reporters=summary` hides failure details when there are 20 suites or fewer.

## Vitest

`test:ai`: `vitest run --reporter=agent` (≥ 4.1) or `vitest run --reporter=dot` (older).

For `test:ai:coverage`, append to `test:ai`:
- Summary: `--coverage.enabled --coverage.reporter=text-summary`
- Gaps table: `--coverage.enabled --coverage.reporter=text --coverage.skipFull`

Notes:
- Add `--update=none` if `vitest --help` lists `none` for `--update`. It fails on a missing snapshot instead of writing it.
- Coverage needs `@vitest/coverage-v8` (or `-istanbul`) at the same major version as Vitest. Ask before installing.
