# Creating a PR in a stack

Use when `gh stack view` shows the current branch is part of a stack. Each PR's base is the branch directly below it, so the PR shows only that layer's changes. Never diff or base against the default branch: it would pull the parent branches' changes into this PR. The "Writing rules" section of [SKILL.md](SKILL.md) applies.

## Contents

- Find the base
- Summarize the changes
- Fill the template
- Create the PR
- Link it into the stack
- If `gh stack` is not installed

## 1. Find the base

```bash
gh stack view --short
```

The stack is listed bottom to top. The base is the branch directly below the current one, unless the user named another. For the first branch of the stack, the base is the stack's target (usually the default branch). If the base is unclear, ask the user instead of guessing.

## 2. Summarize the changes

Always read the git diff before writing the summary, against that base only:

```bash
git log <parent-branch>..HEAD
git diff <parent-branch>...HEAD
```

Write the description following the Description rules in SKILL.md, and a title following the Title rules.

## 3. Fill the template

Fill the template found in SKILL.md step 1, keeping its headings and checkboxes and using the description and title you wrote. Write the result to a temp file.

## 4. Create the PR

Push the branch (`git push -u origin HEAD` if it has no upstream), then run:

```bash
# --draft: always a draft, never ready for review
# --assignee @me: assign to the current GitHub user
# --base: the branch directly below this one in the stack
gh pr create --draft --assignee @me --base <parent-branch> --title "<title>" --body-file <file>
```

If a PR already exists for the branch, tell the user instead of creating another.

## 5. Link it into the stack

`gh pr create` alone gives the right diff but does not link the PR into the stack on GitHub. After creating it, link the stack, listing branches bottom to top:

```bash
gh stack link <bottom-branch> ... <this-branch>
```

Existing PRs are reused and missing PRs are created, so list every branch of the stack. Already-linked PRs are never removed.

Do not use `gh stack submit` here: it opens an interactive editor, and new PRs default to ready for review, which breaks the draft and template rules.

Return the PR URL when done.

## If `gh stack` is not installed

Use the branch this one was created from as the base, create the PR as above, and tell the user the PR was not linked into a stack. Install with `gh extension install github/gh-stack`.
