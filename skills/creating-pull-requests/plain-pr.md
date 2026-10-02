# Creating a PR without a stack

Use when the branch is not part of a gh stack. The "Writing rules" section of [SKILL.md](SKILL.md) applies.

## 1. Find the base

Use the base the user named. Otherwise use the default branch:

```bash
gh repo view --json defaultBranchRef -q .defaultBranchRef.name
```

## 2. Summarize the changes

Always read the git diff before writing the summary:

```bash
git log <base>..HEAD
git diff <base>...HEAD
```

Write the description following the Description rules in SKILL.md, and a title following the Title rules.

## 3. Fill the template

Fill the template found in SKILL.md step 1, keeping its headings and checkboxes and using the description and title you wrote. Write the result to a temp file.

## 4. Create the PR

1. Push the branch if it has no upstream: `git push -u origin HEAD`.
2. Create the PR:

```bash
# --draft: always a draft, never ready for review
# --assignee @me: assign to the current GitHub user
gh pr create --draft --assignee @me --base <base> --title "<title>" --body-file <file>
```

3. If a PR already exists for the branch, tell the user instead of creating another.
4. Return the PR URL.
