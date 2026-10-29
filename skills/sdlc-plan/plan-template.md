# Plan template

Delete any section or collapsed block you have nothing to add to.

```md
# Plan: <title>

From: <intent.md (<date>), spec.md (<date>), or "direct request">. Author: <name>. Date: <YYYY-MM-DD>. Status: not executed | executed.

## Files that change
List every touched file, ranked by risk, riskiest first. Risky means: migrations, changed fetching or data-access logic, breaking changes (public API, schema, contracts), auth, config. Low-risk files (tests, copy, styling) go in the collapsed block.
- <path> (new | changed | deleted) — high | medium: <why it is risky>

<details>
<summary>Minor or no risk (<count> files)</summary>

- <path> (new | changed | deleted) — minor | none: <what changes>
</details>

## Order of work
1. <Step>. Covers: R1, R2. Done when: <check>.

## Risks
List every risk, ranked riskiest first, using the same notion of risky as above. Minor risks go in the collapsed block.
- <What could break, the riskiest step, and the mitigation.>

<details>
<summary>Minor risks (<count>)</summary>

- <What could break and the mitigation.>
</details>

## Alternatives not taken
- <Option>: <why rejected>.

## Proof
<details>
<summary>Tests and commands</summary>

- <test file>: <what it asserts>. Covers: R1.
- Commands: <how to run tests and lint>.
</details>
```

## Example

```md
# Plan: claims status self-service

From: intent.md (2026-06-02), spec.md (2026-06-03). Author: A. Lee. Date: 2026-06-04. Status: executed.

## Files that change
- claims-api/routes/status.py (changed) — high: new fetch path to claims-core, rate-limited upstream.
- portal/nav/config.ts (changed) — medium: nav entry gated by feature flag.

<details>
<summary>Minor or no risk (3 files)</summary>

- portal/components/StatusPanel.tsx (new) — minor: new presentational panel.
- claims-api/tests/test_status.py (new) — none: tests.
- portal/copy/en.json (changed) — none: panel labels.
</details>

## Order of work
1. Add the status endpoint behind existing auth. Covers: R1, R4. Done when: tests pass.
2. Build the panel against the endpoint. Covers: R2.
3. Wire the panel into the portal nav. Covers: R3.

## Risks
- claims-core rate-limits at 50 rps; the panel caches responses for 60s.

<details>
<summary>Minor risks (1)</summary>

- Cached status can be up to 60s stale; the panel shows "last updated" time.
</details>

## Alternatives not taken
- Polling claims-core from the browser: exposes the internal API.

## Proof
<details>
<summary>Tests and commands</summary>

- test_status.py: covers the four claim states and unauthenticated access. Covers: R1, R4.
- Screenshot matches the approved mock. Covers: R2.
- Commands: `pytest claims-api`, `npm test --prefix portal`.
</details>
```
