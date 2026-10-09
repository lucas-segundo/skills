# Intent template

Keep every heading. Write "None" rather than deleting a section.

```md
# Intent: <title>

Author: <name>. Date: <YYYY-MM-DD>. Status: draft.

## Problem
<What hurts today, for whom, and what it costs. Facts and numbers where known.>

## Proposed outcome
<What is true when this is done, in the user's terms. How success is measured.>

## Affected users and systems
<People, teams, systems, APIs.>

## Constraints
<Security, privacy, compliance, deadlines, budget, required or forbidden tech.>

## Out of scope
<What this change will not do.>

## Open questions
<Unknowns to answer in the spec. One per bullet.>
```

## Example

```md
# Intent: claims status self-service

Author: J. Ortiz. Date: 2026-06-02. Status: draft.

## Problem
Customers phone the contact center to ask where their claim is.
Handlers spend roughly a third of call time on status-only queries.

## Proposed outcome
Customers see claim status, next step and expected date in the portal.
Success: status-only calls drop by half within a quarter.

## Affected users and systems
Customers, claims handlers, portal team, claims-core API.

## Constraints
No new PII in the portal session. Existing authentication only.

## Out of scope
Editing or appealing a claim from the portal.

## Open questions
- Do third-party loss adjusters need access too?
```
