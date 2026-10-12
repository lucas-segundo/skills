---
name: sdlc-plan
description: Turns a task, or an accepted spec.md and intent.md when they exist, into plan.md, the implementation plan of the AI-native SDLC, by reading the code without changing it, interviewing the engineer and stress-testing the plan. Commits the plan. Use when the user says "write a plan", "plan the implementation", "draft plan.md", or "turn the spec into a plan". Works with or without an intent or spec.
---

# Planning implementation

Stage 3 (Build) of the AI-native SDLC. Previous (optional): `sdlc-spec`. Intent and spec are not required.

**No code changes in this skill.** Read the repo, write only `plan.md`. Implementation starts after the plan is accepted.

Copy this checklist and tick it off:

```
- [ ] 1. Load inputs (spec and intent if they exist)
- [ ] 2. Read the codebase
- [ ] 3. Interview the engineer
- [ ] 4. Write plan.md
- [ ] 5. Stress-test the plan
- [ ] 6. Cold-engineer check
- [ ] 7. Commit
- [ ] 8. Accept (only on the user's word)
```

## 1. Load the inputs

Intent and spec are optional. Use the change folder the user names. Otherwise list `docs/changes/*/` and ask with the AskUserQuestion tool which one, or whether this is a new change.

- **`spec.md` exists:** read it (and `intent.md` if present). **If its status is not `accepted`, stop** and tell the user to accept it first (`/sdlc-spec`), unless they say to plan without it.
- **No spec:** work from what the user described (or a ticket/link they give). Ask what is needed to pin down the goal and scope. For a new change, create `docs/changes/<YYYY-MM-DD>-<slug>/`.

## 2. Read the codebase

Find every file the change touches, the existing patterns to follow, the test setup and the commands to run tests and lint (`CLAUDE.md`/`AGENTS.md`, `package.json`, CI config). Verify file paths exist; mark new files as `(new)`.

## 3. Interview

Use the AskUserQuestion tool to ask the engineer what the code cannot tell you, a few questions at a time, with your recommended option first: preferred approach where several fit, rollout (flag, migration, backfill), test depth, anything off-limits. Skip questions the code already answers.

## 4. Write plan.md

Use [plan-template.md](plan-template.md). Save it next to the spec: `docs/changes/<folder>/plan.md`. Status: `draft`.

- Every requirement in the spec (`R1`...) maps to at least one step and one proof. List any that do not and ask with AskUserQuestion. With no spec, list the goals you derived from the user at the top of the plan and number them `R1`... so steps and proof can map to them.
- Steps are ordered so each one leaves the code working and testable.
- Proof names concrete tests (file and what they assert) and the commands that run them.

## 5. Stress-test

Answer these in the plan's **Risks** and **Alternatives not taken** sections, then show the user:

- What could this change break? (callers, data, performance, other teams)
- Which step is most risky, and how is that risk reduced?
- Which other approaches were rejected, and why?

Iterate with the engineer until they are happy.

## 6. Cold-engineer check

Re-read the plan as an engineer who never saw this conversation. Could they implement the change from the plan alone? If anything relies on chat context, write it into the plan.

## 7. Commit

Commit only `plan.md` with message `docs(sdlc): plan implementation for <slug>`. Do not push unless the user asks.

## 8. Accept

The plan is accepted only when the user says so. Then set `Status: accepted` and commit with `docs(sdlc): accept plan for <slug>`. Implement only if the user asks. Tell them: when implementation departs from the plan, update `plan.md` in the same commit as the code.
