# Spec template

Keep every heading. Write "None" rather than deleting a section.

```md
# Spec: <title>

From: intent.md (<intent date>). Author: <name>. Date: <YYYY-MM-DD>. Status: draft.
Policy skills applied: <skill names, or None>.

## Summary
<Two or three sentences: what will be built and why, in plain words.>

## Requirements
### Functional
- R1. <Testable statement of behavior.>
### Non-functional
- R<n>. <Performance, security, accessibility, privacy, limits.>

## Design
### Approach
<How the change fits the existing system: components, responsibilities, flow.>
### Data and interfaces
<Data models, API contracts, events, UI states. Only what changes.>
### Alternatives considered
<Options rejected and why.>

## Out of scope
<Carried from the intent, plus anything decided here.>

## Open questions
- <Question from the intent> → Answered: <decision> | Carried: <why still open, who decides>

## Flagged concerns
- <Concern>. Policy: <skill or "intent">. Impact: <what goes wrong>. Proposed resolution: <option>. Owner: <who decides>.
```
