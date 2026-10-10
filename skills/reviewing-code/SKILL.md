---
name: reviewing-code
description: >
  Ultra-compressed code review comments. Cuts noise from PR feedback while preserving
  the actionable signal. Each comment is one line: location, problem, fix. Use when user
  says "review this PR", "code review", "review the diff", "/review", or invokes
  /reviewing-code. Auto-triggers when reviewing pull requests.
---

Write code review comments terse and actionable. One line per finding. Location, problem, fix. No throat-clearing. Terse is the format, not the bar: every finding is verified against the code before it is posted (see "Before posting: verify"). Post findings as inline PR line comments (see "Comment on the PR line"), not in a big comment block.

## Rules

**Format:** `L<line>: <problem>. <fix>.` — or `<file>:L<line>: ...` when reviewing multi-file diffs.

**Severity prefix (optional, when mixed):**
- `🔴 bug:` — broken behavior, will cause incident
- `🟡 risk:` — works but fragile (race, missing null check, swallowed error)
- `🔵 nit:` — style, naming, micro-optim. Author can ignore

**Drop:**
- "I noticed that...", "It seems like...", "You might want to consider..."
- "This is just a suggestion but..." — use `nit:` instead
- "Great work!", "Looks good overall but..." — say it once at the top, not per comment
- Restating what the line does — the reviewer can read the diff
- Hedging ("perhaps", "maybe", "I think") — if unsure, verify; still unsure → drop it
- Questions — every comment is a finding with a fix. Read the code to answer it yourself

**Keep:**
- Exact line numbers
- Exact symbol/function/variable names in backticks
- Concrete fix, not "consider refactoring this"
- The *why* if the fix isn't obvious from the problem statement
- The evidence when the cause is outside the diff: `(see useFoo.ts:18)`

## Context first

Before reading the diff, read the PR body, any plan or spec it links or adds (e.g. `sdlc/**/plan.md`, `docs/changes/**`), and `AGENTS.md` / `CLAUDE.md`. Don't flag:
- decisions the PR or plan states as deliberate
- items the PR already lists as known limitations or pending manual checks
- missing tests when the repo has no test runner (one line in the summary at most)

## Before posting: verify

The diff is where you start, not all you read. For every candidate finding:
1. Open the code it depends on: callers, callees, hooks, query keys, types. Grep the symbol.
2. Write the failure path: concrete input or state → steps → wrong result. Can't write one → drop it. Don't post it as a question.
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

❌ `L63: does useFinishSession invalidate the useSession cache? If not, button hangs.` (no questions: read `useFinishSession`, then post a finding or nothing)

✅ `L63: 🔴 bug: useFinishSession invalidates ["session", id] but useSession keys ["sessions", id] (see useSession.ts:9). Button hangs on "Finishing…". Match the key.`

## Comment on the PR line

Never edit source files. Post each finding as an inline thread in one pending review, then submit it. No big comment block.

- Body = `<severity> <problem>. <fix>.` One line, no `L<line>:`.
- Anchor: `path`, `line` (`startLine` for ranges), `side: RIGHT`. Only lines in the PR diff.
- Chat reply: count per severity and the `<file>:L<line>` list only. No comment text, no preamble.
- No PR (local diff, pasted code, no `gh`): `L<line>: ...` lines in chat.

### Posting

Use whatever inline-comment tool works in this environment: a dedicated inline-comment tool (e.g. `mcp__github_inline_comment__create_inline_comment` in the Claude GitHub Action), GitHub MCP pending-review tools, or `gh api` (REST or GraphQL). Pick the one that is available and allowed. If it fails, try another before giving up.

Outcome, whatever the tool:
- Each finding is its own inline thread on its diff line, ideally grouped in one review.
- Submit as `REQUEST_CHANGES` when the tool supports reviews, body empty or one line ("2 🔴, 1 🟡"). Never approve.
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

Drop terse mode for: security findings (CVE-class bugs need full explanation + reference), architectural disagreements (need rationale, not just a one-liner), and onboarding contexts where the author is new and needs the "why". In those cases write a normal paragraph, then resume terse for the rest. The inline comment stays one line and points to the chat explanation.

## Boundaries

Reviews only — does not write the code fix, does not approve, does not run linters. Never edits source files; only posts inline PR comments (as a `REQUEST_CHANGES` review when possible). "stop reviewing-code" or "normal mode": revert to verbose review style.