---
name: caveman-review
description: >
  Ultra-compressed code review comments. Cuts noise from PR feedback while preserving
  the actionable signal. Each comment is one line: location, problem, fix. Use when user
  says "review this PR", "code review", "review the diff", "/review", or invokes
  /caveman-review. Auto-triggers when reviewing pull requests.
---

Write code review comments terse and actionable. One line per finding. Location, problem, fix. No throat-clearing. Post findings as inline PR line comments (see "Comment on the PR line"), not in a big comment block.

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

## Comment on the PR line

Never edit source files. Post each finding as an inline thread in one pending review, then submit it. No big comment block.

- Body = `<severity> <problem>. <fix>.` One line, no `L<line>:`.
- Anchor: `path`, `line` (`startLine` for ranges), `side: RIGHT`. Only lines in the PR diff.
- Chat reply: count per severity and the `<file>:L<line>` list only. No comment text, no preamble.
- No PR (local diff, pasted code, no `gh`): `L<line>: ...` lines in chat.

### Posting

Use `gh api graphql` only, not REST `reviews` with `comments[]` (422).

1. `gh pr view --json number,headRefOid`.
2. Fetch existing threads (see below).
3. Reuse the user's pending review, else `addPullRequestReview` (`pullRequestId`, no `event`).
4. Per finding: `addPullRequestReviewThread` (`pullRequestReviewId`, `path`, `line`, `side`, `body`).
5. `submitPullRequestReview` with `event: REQUEST_CHANGES`, body empty or one line ("2 🔴, 1 🟡"). Never approve.
6. Nothing new to post → no empty review. Delete a pending review you created with no comments.

### No duplicates on re-review

List `pullRequest.reviewThreads` (`isResolved`, `isOutdated`, `path`, `line`, `comments.nodes.body`) plus pending comments.

- Same problem on same code (match path + code + problem, not wording or line) → skip.
- Resolved, code unchanged → skip.
- Outdated, problem persists → skip, mention in summary.
- Stale wording or severity → `updatePullRequestReviewComment`.
- Fixed, thread still open → don't post; list as "looks fixed" in summary.

## Auto-Clarity

Drop terse mode for: security findings (CVE-class bugs need full explanation + reference), architectural disagreements (need rationale, not just a one-liner), and onboarding contexts where the author is new and needs the "why". In those cases write a normal paragraph, then resume terse for the rest. The inline comment stays one line and points to the chat explanation.

## Boundaries

Reviews only — does not write the code fix, does not approve, does not run linters. Never edits source files; only posts and submits inline PR comments as a `REQUEST_CHANGES` review. "stop caveman-review" or "normal mode": revert to verbose review style.