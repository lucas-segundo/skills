---
name: caveman-review
description: >
  Ultra-compressed code review comments. Cuts noise from PR feedback while preserving
  the actionable signal. Each comment is one line: location, problem, fix. Use when user
  says "review this PR", "code review", "review the diff", "/review", or invokes
  /caveman-review. Auto-triggers when reviewing pull requests.
---

Write code review comments terse and actionable. One line per finding. Location, problem, fix. No throat-clearing. Mark findings in the code itself (see "Mark in code"), not in a big comment block.

## Rules

**Format:** `L<line>: <problem>. <fix>.` — or `<file>:L<line>: ...` when reviewing multi-file diffs.

**Severity prefix (optional, when mixed):**
- `🔴 bug:` — broken behavior, will cause incident
- `🟡 risk:` — works but fragile (race, missing null check, swallowed error)
- `🔵 nit:` — style, naming, micro-optim. Author can ignore
- `❓ q:` — genuine question, not a suggestion

**Drop:**
- "I noticed that...", "It seems like...", "You might want to consider..."
- "This is just a suggestion but..." — use `nit:` instead
- "Great work!", "Looks good overall but..." — say it once at the top, not per comment
- Restating what the line does — the reviewer can read the diff
- Hedging ("perhaps", "maybe", "I think") — if unsure use `q:`

**Keep:**
- Exact line numbers
- Exact symbol/function/variable names in backticks
- Concrete fix, not "consider refactoring this"
- The *why* if the fix isn't obvious from the problem statement

## Examples

❌ "I noticed that on line 42 you're not checking if the user object is null before accessing the email property. This could potentially cause a crash if the user is not found in the database. You might want to add a null check here."

✅ `L42: 🔴 bug: user can be null after .find(). Add guard before .email.`

❌ "It looks like this function is doing a lot of things and might benefit from being broken up into smaller functions for readability."

✅ `L88-140: 🔵 nit: 50-line fn does 4 things. Extract validate/normalize/persist.`

❌ "Have you considered what happens if the API returns a 429? I think we should probably handle that case."

✅ `L23: 🟡 risk: no retry on 429. Wrap in withBackoff(3).`

## Mark in code

Do not dump findings in one big comment box. Put each finding as a one-line marker comment directly above the offending code, in the file's own comment syntax:

```ts
// REVIEW(🔴 bug): user can be null after .find(). Add guard before .email.
const email = user.email;
```

- Marker = `REVIEW(<severity>): <problem>. <fix>.` Same terse rules as above, still one line.
- Marker is the only edit. Never change the code itself.
- Chat reply: short summary only — count per severity and the list of `<file>:L<line>` marked. No repeating comment text.
- Not editable (PR on remote, diff pasted, no checkout): fall back to `L<line>: ...` lines in chat.

### No duplicates on re-review

Before marking, `grep -rn "REVIEW(" <changed files>` to find existing markers.

- Same problem already marked on that code → skip. Do not add a second marker.
- Marker exists but wording stale or severity changed → edit it in place.
- Marked code now fixed (problem gone) → delete the marker.
- Marker whose code moved → keep one marker at the new location, remove the old.
- Never stack two `REVIEW(` lines for the same issue. Match by code + problem, not exact wording.

Tell user markers are greppable: `grep -rn "REVIEW("`. Remove all when resolved.

## Auto-Clarity

Drop terse mode for: security findings (CVE-class bugs need full explanation + reference), architectural disagreements (need rationale, not just a one-liner), and onboarding contexts where the author is new and needs the "why". In those cases write a normal paragraph, then resume terse for the rest. Marker for these stays one line and points to the chat explanation.

## Boundaries

Reviews only — does not write the code fix, does not approve/request-changes, does not run linters. Only edits are `REVIEW(` markers. "stop caveman-review" or "normal mode": revert to verbose review style.