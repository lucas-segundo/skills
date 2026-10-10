# Intent template

Keep every heading except Open questions. Write "None" rather than deleting a section. Business language only: no code, file names, APIs or technology.

```md
# Intent: <title>

Author: <name>. Date: <YYYY-MM-DD>. Status: draft.

## Problem
<What hurts today, for whom, and what it costs. Facts and numbers where known.>

## Proposed outcome
<What is true when this is done, in the user's terms. How success is measured.>

## Affected users and teams
<People, teams, customers, partners, business processes.>

## Constraints
<Privacy, compliance, deadlines, budget, policies, contracts.>

## Out of scope
<What this change will not do.>

## Open questions
<Only if any remain: questions the AI asked that the user could not answer, or questions the user asked that the AI could not answer. One per bullet. Otherwise omit this section.>
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

## Affected users and teams
Customers, claims handlers, contact center, portal team.

## Constraints
Customers see no personal data beyond what the portal already shows.
Customers use their current portal login; no new sign-up.

## Out of scope
Editing or appealing a claim from the portal.

## Open questions
- Do third-party loss adjusters need access too?
```
