# Plan template

Keep every heading. Write "None" rather than deleting a section.

```md
# Plan: <title>

From: intent.md (<date>), spec.md (<date>). Author: <name>. Date: <YYYY-MM-DD>. Status: draft.

## Files that change
- <path> (new | changed | deleted): <why>

## Order of work
1. <Step>. Covers: R1, R2. Done when: <check>.

## Risks
- <What could break, the riskiest step, and the mitigation.>

## Alternatives not taken
- <Option>: <why rejected>.

## Proof
- <test file>: <what it asserts>. Covers: R1.
- Commands: <how to run tests and lint>.
```

## Example

```md
# Plan: claims status self-service

From: intent.md (2026-06-02), spec.md (2026-06-03). Author: A. Lee. Date: 2026-06-04. Status: draft.

## Files that change
- portal/src/claims/StatusPanel.tsx (new): status panel.
- claims-api/routes/status.py (changed): status endpoint.
- claims-api/tests/test_status.py (new): endpoint tests.

## Order of work
1. Add the status endpoint behind existing auth. Covers: R1, R4. Done when: tests pass.
2. Build the panel against the endpoint. Covers: R2.
3. Wire the panel into the portal nav. Covers: R3.

## Risks
- claims-core rate-limits at 50 rps; the panel caches responses for 60s.

## Alternatives not taken
- Polling claims-core from the browser: exposes the internal API.

## Proof
- test_status.py: covers the four claim states and unauthenticated access. Covers: R1, R4.
- Screenshot matches the approved mock. Covers: R2.
- Commands: `pytest claims-api`, `npm test --prefix portal`.
```
