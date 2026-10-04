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

Do not dump findings in one big comment box, and never edit the source files. Post each finding as an inline review comment on the exact line(s) in the GitHub PR, in a **pending** review (not submitted), so the author resolves each thread.

- Body = `<severity> <problem>. <fix>.` One line, same terse rules as above. Line number is implied by the anchor, drop `L<line>:`.
- Anchor to the line(s) of the offending code: `path`, `line` (and `start_line` for ranges), `side: RIGHT`. Only lines in the PR diff can be commented.
- Leave the review pending. Never submit, approve or request changes; the user submits.
- Chat reply: short summary only — count per severity and the `<file>:L<line>` list. No repeating comment text.
- No PR (local diff, pasted code, no `gh`): fall back to `L<line>: ...` lines in chat.

### Posting

1. Get PR number and head: `gh pr view --json number,headRefOid`.
2. Fetch existing threads first (see below).
3. Pending review already exists for the user → add threads to it with GraphQL `addPullRequestReviewThread` (`pullRequestReviewId`, `path`, `line`, `side`, `body`). Otherwise create one via `gh api repos/{owner}/{repo}/pulls/{n}/reviews` with `comments[]` and **no `event`**, which leaves it pending.

### No duplicates on re-review

Before posting, list existing review threads (GraphQL `pullRequest.reviewThreads`: `isResolved`, `isOutdated`, `path`, `line`, `comments.nodes.body`) plus pending review comments.

- Same problem already on that code (match by path + code + problem, not exact wording or line number) → skip. Do not post a second comment.
- Thread exists and is resolved, code unchanged → skip. Author decided.
- Thread outdated because the code moved and problem persists → skip, mention in summary.
- Existing comment wording or severity stale → edit that comment (`updatePullRequestReviewComment`) instead of adding one.
- Problem now fixed, thread still open → do not post; list it in the summary as "looks fixed" for the author to resolve.

## Auto-Clarity

Drop terse mode for: security findings (CVE-class bugs need full explanation + reference), architectural disagreements (need rationale, not just a one-liner), and onboarding contexts where the author is new and needs the "why". In those cases write a normal paragraph, then resume terse for the rest. The inline comment stays one line and points to the chat explanation.

## Boundaries

Reviews only — does not write the code fix, does not approve/request-changes, does not run linters. Never edits source files; only posts pending inline PR comments. "stop caveman-review" or "normal mode": revert to verbose review style.