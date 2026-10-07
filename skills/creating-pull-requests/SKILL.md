---
name: creating-pull-requests
description: Creates GitHub pull requests with the gh CLI, filling the repo's PR template with a plain-language summary of the changes. Handles both plain branches and gh stack stacked PRs. Use when the user asks to open, create, or raise a pull request or PR.
---

# Creating pull requests

Copy this checklist and tick it off:

```
- [ ] 1. Find the PR template (stop if missing)
- [ ] 2. Check if the branch is in a stack
- [ ] 3. Follow the matching guide (summarize, fill template, create PR)
```

## Tooling

Use only `gh` for all GitHub operations. If `gh` is not available (`command -v gh` fails), use the GitHub connector or another available tool instead.

## 1. Find the template

Look for the template in these locations, in order:

- `.github/pull_request_template.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `pull_request_template.md` or `PULL_REQUEST_TEMPLATE.md` (repo root or `docs/`)
- `.github/PULL_REQUEST_TEMPLATE/*.md` (several templates: pick the one that best fits the changes, and ask the user if unclear)

**If no template exists, stop.** Do not create the PR and do not invent a template. Tell the user to add a PR template first, then ask them to re-run the request.

## 2. Check if the branch is in a stack

```bash
gh stack view --short
```

- Prints the stack: the branch is stacked.
- Errors with "not part of a stack": the branch is not stacked.
- `gh stack` is not installed: treat the branch as not stacked, unless the user says it is.

## 3. Follow the matching guide

Follow it to the end. Each guide covers the diff, the summary, the template and the PR creation.

- Not in a stack: [plain-pr.md](plain-pr.md)
- In a stack: [stacked-pr.md](stacked-pr.md)

If the user named a base branch, use it in either guide.

## Writing rules

Both guides use these rules.

### Title

A short version of the description, at most 10 words. Plain words, no code identifiers.

Good: "Add password reset from the login page"
Bad: "Add resetPassword() to auth.ts with a one-hour TTL and update the login page and tests"

### Description

Write for a human reviewer who has not read the diff:

- Say what changed and why, in plain words.
- Do not mention line numbers, file paths, function names, variable names, or other code identifiers.
- Group related changes together instead of listing every commit.

Good: "Users can now reset their password from the login page, and the reset link expires after one hour."
Bad: "Added `resetPassword()` in auth.ts and set `TTL = 3600` on line 42."
