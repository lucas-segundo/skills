---
name: configuring-ai-scripts
description: Adds token-cheap package.json scripts for AI agents (lint:ai, test:ai, test:ai:coverage) using the compact output modes Biome, Jest and Vitest already ship. Interviews the user about which scripts to add. Use when the user wants AI scripts, shorter or cheaper lint/test output for Claude, or says "/configuring-ai-scripts".
---

# Configuring AI scripts

Add `*:ai` scripts so agents see failures without the noise of passing files. Human scripts stay untouched.

## Rules

- **Built-in options only.** No custom formatters, reporters or config files. A tool with no compact mode gets no script.
- **Never hide a problem.** Drop noise only. No `--quiet`, `--diagnostic-level`, `--passWithNoTests`, and no `--max-diagnostics` below the total.
- **Never looser than CI.** Keep strictness flags the project uses (`--max-warnings`, `--error-on-warnings`).
- **Leave developer choices alone**: `.only`, `.skip`, `eslint-disable` comments, ignore patterns.
- **Scripts take no path**, so passing files after `--` scopes the run.
- **No pipes** (`| grep`, `| tail`): a pipeline returns the last command's exit code.
- **Install or upgrade nothing without asking.**

## Workflow

1. **Detect**: the package manager (from the lockfile), the tools and their versions, the strictness flags in the existing scripts and CI, and any existing `*:ai` scripts (ask before replacing one). In a monorepo, ask which packages to configure.
2. **Interview** in one `AskUserQuestion` call. Offer only the tools that have a recipe at their version in [recipes.md](recipes.md), and name the ones left out and why.
   - **Tools** (multiSelect).
   - **Biome mode**: *Check only (Recommended)* or *Fix first* (`--write`).
   - **Coverage**: *Summary only (Recommended)*, *Gaps table* (Vitest only) or *None*.
3. **Write** the scripts from [recipes.md](recipes.md): `lint:ai`, `test:ai`, `test:ai:coverage`.
4. **Verify** each script, then revert the temporary changes:
   - a clean run exits 0 and prints a summary;
   - a planted lint error and a failing assertion exit non-zero with `file:line`;
   - the problem count matches the human script's;
   - passing one file after `--` runs only that file.

   Report the line counts, human script vs AI script.
5. **Document**: append this snippet to `CLAUDE.md` or `AGENTS.md`, adjusted to the scripts added. If neither file exists, ask before creating one.

```md
## AI scripts

Prefer these over the human scripts: same checks, less output. Scope with files: `npm run test:ai -- src/a.test.ts`.

- `lint:ai`: one line per lint problem
- `test:ai`: failing tests only, then totals
- `test:ai:coverage`: same, plus coverage

The exit code is the verdict (a coverage threshold can fail while the totals say "passed"). 0 tests or 0 files checked means nothing was verified.
```
