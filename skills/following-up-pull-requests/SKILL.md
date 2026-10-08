---
name: following-up-pull-requests
description: Follows up a GitHub pull request's code review comments. Auto-fixes, replies to and resolves the user's own comments after checking they are valid; reports other reviewers' comments in the session for the user to decide. Use when the user asks to follow up, address, or handle review comments on a PR.
---

# Following up pull requests

Copy this checklist and tick it off:

```
- [ ] 1. Identify the PR and the current user
- [ ] 2. Collect unresolved review comments
- [ ] 3. Evaluate each comment against the code
- [ ] 4. Act by author (own: fix, reply, resolve / others: report)
- [ ] 5. Summarize to the user
```

## Tooling

Use whatever tool the environment offers to read and write GitHub data (fetch comments, push commits, post replies, resolve threads). It may be a connector, a CLI, an API, or something else, depending on whether you run locally or in the cloud. This guide describes what to do, not which command to run.

## 1. Identify the PR and the user

- PR: use the number or URL the user gave. Otherwise use the PR for the current branch. If none is found, ask.
- Current user: the authenticated GitHub login. "Own comment" means the comment author equals this login.

## 2. Collect comments

Fetch all **unresolved** review threads (inline code comments, with their replies) plus review summary comments and general PR comments. Skip threads that are resolved or outdated-and-already-addressed. Keep for each: thread id, author, file, line, full reply chain.

Fetch comments grouped by review thread, with whatever identifier the environment needs later to reply to and resolve each thread.

## 3. Evaluate every comment first

Never apply a comment blindly. For each one, read the referenced code and its surroundings, then decide:

- **Valid**: the issue is real and the suggestion is correct.
- **Partly valid**: the concern is real but the suggested fix is wrong or too broad. Plan a better fix.
- **Not valid**: based on a misunderstanding, already handled, or contradicts project conventions.
- **Risky**: the change would break behavior, cause a regression, or touch things outside the PR's scope.

Check for breakage: look at callers, related tests, types and the repo's lint/test scripts. A comment that sounds right can still cause a regression.

## 4. Act by author

### Own comments (author = current user)

- **Valid / partly valid**:
  1. Make the fix.
  2. Run the relevant checks (lint, types, affected tests, using the repo's own scripts). Do not proceed if they fail; fix or treat as risky.
  3. Commit with a message that references the comment, and push.
  4. Reply on the thread saying what was changed (short, plain words, mention the commit).
  5. Mark the thread as resolved.
- **Not valid / risky**: do **not** change the code, reply, or resolve. Leave the thread untouched and report it to the user with the reason, since even their own comment may be outdated or wrong.

### Other people's comments

Never change code, reply, or resolve. Report them in the session so the user decides.

For each one give:

- Author, file and line, link to the thread
- What they ask, in one sentence
- Your assessment: valid / partly valid / not valid / risky, with the reason (and any regression risk)
- Suggested action (apply, apply differently, push back) and a draft reply if pushing back

Then wait for the user's decision. Only act on those comments after the user says so, and then follow the same fix, check, commit, reply, resolve flow.

## 5. Summarize

End with a short report:

- Own comments: fixed and resolved (list), left open with reason (list)
- Other comments: awaiting the user's decision (list with your assessment)
- Checks run and their result
