---
name: pr-code-review
description: >
  Ultra-compressed code review comments. Cuts noise from PR feedback while preserving
  the actionable signal. Each comment is one line: location, problem, fix. Use when user
  says "review this PR", "code review", "review the diff", "/review", or invokes
  /pr-code-review. Auto-triggers when reviewing pull requests.
---

One line per finding: problem, fix. Terse is the format, not the bar: every finding is verified against the code before it is posted.

## Rules

**Severity prefix:**
- `🔴 bug:` — broken behavior, will cause incident
- `🟡 risk:` — works but fragile (race, missing null check, swallowed error)
- `🔵 nit:` — style, naming, micro-optim. Author can ignore
- `❓ ask:` — unresolved after reading the code; needs author answer

**Drop:** hedging, praise per comment, restating what the line does, "consider refactoring" without a concrete fix.

**Keep:** symbol names in backticks, the *why* when the fix isn't obvious, the evidence when the cause is outside the diff: `(see useFoo.ts:18)`.

## Questions

Answer a question from the code first: answered → a finding or nothing. Use `❓ ask:` only when the answer is outside the repo (backend, product decision): `❓ ask: <question>? <what to fix if the answer is bad>.` It is an inline comment like any finding, never chat, and doesn't count toward the nit budget.

## Context first

Before reading the diff, read the PR body, any plan or spec it links or adds (e.g. `sdlc/**/plan.md`, `docs/changes/**`), and `AGENTS.md` / `CLAUDE.md`. Don't flag:
- decisions the PR or plan states as deliberate
- items the PR already lists as known limitations or pending manual checks
- missing tests when the repo has no test runner (one line in the summary at most)

## Check against spec.md

Find the change's `spec.md` (`docs/changes/*/spec.md`, or the one the PR body links or adds). Match by PR title, branch name or slug. Do not guess between several candidates: pick the one the PR references, else treat as not found.

- **Found:** compare the diff with its requirements (`R1`...). For each requirement the code does not meet, or only partly meets, post an inline finding on the closest diff line: `🔴 bug: R<n> "<requirement>" not met. <what is missing>.` Check that the feature as a whole reaches the spec's goal, not only that each line is correct. Requirements met need no comment. If the spec's status is not `accepted`, say so in the summary.
- **Not found:** warn in the review body (and the chat summary): `⚠️ No spec.md found for this change. Could not verify the code reaches its goal.` Still review the code on its own merits.

## Before posting: verify

The diff is where you start, not all you read. For every candidate finding:
1. Open the code it depends on: callers, callees, hooks, query keys, types. Grep the symbol.
2. Write the failure path: concrete input or state → steps → wrong result. Can't write one from the repo → drop it, unless it hinges on something outside the repo (then `❓ ask`).
3. Bar per severity: `🔴 bug` needs a path reachable from real use today. `🟡 risk` needs a realistic trigger, not "if the cache were stale" or "if someone typed this URL".
4. Weigh the fix: when it costs more code than the failure it prevents, drop it.

Budget: at most 3 `🔵 nit` per review. Pick the ones a teammate would actually fix.

## Examples

❌ "I noticed that on line 42 you're not checking if the user object is null before accessing the email property. This could potentially cause a crash if the user is not found in the database. You might want to add a null check here."

✅ `L42: 🔴 bug: user can be null after .find(). Add guard before .email.`

❌ "It looks like this function is doing a lot of things and might benefit from being broken up into smaller functions for readability."

✅ `L88-140: 🔵 nit: 50-line fn does 4 things. Extract validate/normalize/persist.`

❌ "Have you considered what happens if the API returns a 429? I think we should probably handle that case."

✅ `L23: 🟡 risk: no retry on 429. Wrap in withBackoff(3).`

❌ `L63: does useFinishSession invalidate the useSession cache? If not, button hangs.` (answerable: read `useFinishSession`, then post a finding or nothing)

✅ `L31: ❓ ask: does the backend dedupe retried `POST /pay`? If not, add idempotency key.` (answer not in repo; anchored inline)

✅ `L63: 🔴 bug: useFinishSession invalidates ["session", id] but useSession keys ["sessions", id] (see useSession.ts:9). Button hangs on "Finishing…". Match the key.`

## Comment on the PR line

Post each finding as an inline thread in one pending review, then submit it. Use whatever inline-comment tool is available (a dedicated inline-comment tool, GitHub MCP pending-review tools, `gh api`); if one fails, try another.

- Body = `<severity> <problem>. <fix>.` One line.
- Anchor: `path`, `line` (`startLine` for ranges), `side: RIGHT`. Only lines in the PR diff.
- Spec warning (no `spec.md`) goes in the review body, never as an inline thread.
- Chat reply: count per severity and the `<file>:L<line>` list only. No comment text, no preamble.
- No PR (local diff, pasted code, no `gh`): `<file>:L<line>: <severity> <problem>. <fix>.` lines in chat.

### Posting

- Submit as `REQUEST_CHANGES` when the tool supports reviews, body empty or one line ("2 🔴, 1 🟡"), plus the spec warning when it applies. Never approve.
- Nothing new to post → no empty review. Delete a pending review you created with no comments.
- Inline posting impossible with every available tool → post the one-line findings as one PR comment and say in the summary why inline failed.

Known pitfall: REST `POST /pulls/{n}/reviews` with `comments[]` often 422s on lines outside the diff. Check that the anchor is a diff line.

### No duplicates on re-review

First list the existing review threads (resolved and outdated state, path, line, comment bodies) plus your pending comments.

- Same problem on same code (match path + code + problem, not wording or line) → skip.
- Resolved, code unchanged → skip.
- Outdated, problem persists → skip, mention in summary.
- Stale wording or severity → edit your existing comment.
- Fixed, thread still open → don't post; list as "looks fixed" in summary.

## Auto-Clarity

Drop terse mode for security findings (explanation + reference), architectural disagreements (rationale) and authors new to the codebase (the "why"). Write a normal paragraph in that inline comment, then resume terse for the rest.

## Boundaries

Reviews only: never edits source files, writes the fix, approves or runs linters.