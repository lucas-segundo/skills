# Plan template

The plan is a header, then one section per step **in the order the work is done**. Each step carries its own change, risks and proof, so an agent can execute one step before starting the next. Errors between steps are expected; the final check verifies everything at the end. Only what spans several steps goes after them.

```md
# Plan: <title>

Source: <ticket or link, or "task description">
Writing skills: <skills the executing agent loads before writing code, or "None">
Order: <where the order comes from: "AGENTS.md: <quoted rule>", or "default: <short reason>">

## Goals
- R1: <goal>
- R2: <goal>

## Step 1: <short name>
Requirements: <R ids this step serves>
Depends on: <earlier steps, or "none">

Change:
<what this step does, in a sentence or two; no line-by-line detail>
<optional sketch: signatures and shape of the code, bodies elided with `...`>

Risks:
- <what could break> → <how this step reduces it>

Proof:
- <test file>: <what it asserts>

## Step 2: <short name>
...

## Across steps
Risks: <risks that span several steps, or "None">
Rejected approaches: <approach → why not>
Final check: `<typecheck, lint and test commands covering every changed file and proof test, run once after the last step>`
```

## Example

```md
# Plan: claims status self-service

Source: CLM-412
Writing skills: writing-react, writing-javascript
Order: AGENTS.md: "API changes land before the UI that uses them"

## Goals
- R1: Customers see their claim status in the portal.
- R2: Only the claim owner can read its status.
- R3: The panel recovers when the API fails.

## Step 1: Status endpoint
Requirements: R1, R2
Depends on: none

Change:
GET /claims/{id}/status behind the existing auth decorator, cached 30 s.

    @router.get("/claims/{claim_id}/status")
    @requires_auth
    @cache(ttl=30)
    def claim_status(claim_id: str) -> StatusOut: ...

Risks:
- claims-core rate-limits at 50 rps → 30 s cache per claim.

Proof:
- test_status.py: the four claim states map to the right label (R1); unauthenticated call gets 401 (R2).

## Step 2: Status panel
Requirements: R1, R3
Depends on: Step 1

Change:
Panel fetches the step 1 endpoint and renders state, date and next action.

    function StatusPanel({ claimId }: Props) {
      const { data, error, retry } = useClaimStatus(claimId);
      if (error) return <RetryNotice onRetry={retry} />;
      ...
    }

Risks:
- Slow endpoint leaves an empty panel → skeleton while loading, retry on error.

Proof:
- StatusPanel.test.tsx: renders each state; shows retry on a 500 (R3).

## Step 3: Portal nav
Requirements: R1
Depends on: Step 2

Change:
Add "Claim status" to the claims menu, linking to the panel.

Risks:
- None beyond the shared nav snapshot → update that snapshot in this step.

Proof:
- routes.test.tsx: the new entry is present for signed-in users.

## Across steps
Risks: None.
Rejected approaches: polling claims-core from the browser → exposes the internal API and multiplies its load.
Final check: `pytest claims-api/tests/test_status.py && npx vitest run portal/src/claims portal/src/nav && npm run lint && npm run typecheck`
```
