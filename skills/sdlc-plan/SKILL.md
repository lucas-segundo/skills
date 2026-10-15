---
name: sdlc-plan
description: Turns a task, or an accepted spec.md and intent.md when they exist, into plan.md, the implementation plan of the AI-native SDLC, inside plan mode: reads the code, interviews the engineer, stress-tests the plan, then, once the engineer approves it, commits plan.md if they want and implements it. Use when the user says "write a plan", "plan the implementation", "draft plan.md", or "turn the spec into a plan". Works with or without an intent or spec.
---

# Planning implementation

Stage 3 (Build) of the AI-native SDLC. Previous (optional): `sdlc-spec`. Intent and spec are not required.

Steps 1–7 run in **plan mode**: the repo stays read-only and the plan lives in the plan file the harness assigns. Approving the plan (`ExitPlanMode`) accepts it; only then is `plan.md` committed (if the user wants) and implementation starts.

Copy this checklist and tick it off:

```
- [ ] 1. Enter plan mode
- [ ] 2. Load inputs (spec and intent if they exist)
- [ ] 3. Read the codebase
- [ ] 4. Interview the engineer
- [ ] 5. Write the plan
- [ ] 6. Stress-test the plan
- [ ] 7. Cold-engineer check
- [ ] 8. Exit plan mode for approval
- [ ] 9. Commit plan.md (ask first)
- [ ] 10. Implement
```

## 1. Enter plan mode

Call `EnterPlanMode`. Already in plan mode: carry on. The user declines: stop and ask how they want to proceed.

## 2. Load the inputs

Intent and spec are optional. Use the change folder the user names. Otherwise list `docs/changes/*/` and ask with the AskUserQuestion tool which one, or whether this is a new change.

- **`spec.md` exists:** read it (and `intent.md` if present). **If its status is not `accepted`, stop** and tell the user to accept it first (`/sdlc-spec`), unless they say to plan without it.
- **No spec:** work from what the user described (or a ticket/link they give). Ask what is needed to pin down the goal and scope. For a new change, pick the folder name `docs/changes/<YYYY-MM-DD>-<slug>/` now; create it in step 9.

## 3. Read the codebase

Find every file the change touches, the existing patterns to follow, the test setup and the commands to run tests and lint (`CLAUDE.md`/`AGENTS.md`, `package.json`, CI config). Verify file paths exist; mark new files as `(new)`.

## 4. Interview

Use the AskUserQuestion tool to ask the engineer what the code cannot tell you, a few questions at a time, with your recommended option first: preferred approach where several fit, rollout (flag, migration, backfill), test depth, anything off-limits. Skip questions the code already answers.

## 5. Write the plan

Use [plan-template.md](plan-template.md). Write it to the plan file the harness assigned in plan mode. Status: `draft`. Fill `Saves to:` with `docs/changes/<folder>/plan.md`; step 9 writes the plan there.

- Every requirement in the spec (`R1`...) maps to at least one step and one proof. List any that do not and ask with AskUserQuestion. With no spec, list the goals you derived from the user at the top of the plan and number them `R1`... so steps and proof can map to them.
- Steps are ordered so each one leaves the code working and testable.
- Proof names concrete tests (file and what they assert) and the commands that run them.

## 6. Stress-test

Answer these in the plan's **Risks** and **Alternatives not taken** sections, then show the user:

- What could this change break? (callers, data, performance, other teams)
- Which step is most risky, and how is that risk reduced?
- Which other approaches were rejected, and why?

Iterate with the engineer until they are happy.

## 7. Cold-engineer check

Re-read the plan as an engineer who never saw this conversation. Could they implement the change from the plan alone? If anything relies on chat context, write it into the plan.

## 8. Exit plan mode

Call `ExitPlanMode`. The engineer's approval accepts the plan. If they reject it, revise in plan mode and call `ExitPlanMode` again.

## 9. Commit plan.md (ask first)

Ask with the AskUserQuestion tool whether to commit the approved plan:

- **Commit it** (recommended): write it to its `Saves to:` path (create the folder if new) with `Status: approved`, and commit only `plan.md` with message `docs(sdlc): plan implementation for <slug>`. Do not push unless the user asks.
- **Don't commit**: write nothing to the repo; the approved plan stays in the harness plan file only.

## 10. Implement

Implement the plan in its order of work, running the proof commands as each step completes. When implementation departs from a committed `plan.md`, update it in the same commit as the code.

Keep the committed plan's `Status:` true, so another session can tell from the file alone whether the plan still needs doing (meanings in [plan-template.md](plan-template.md#status)):

- Starting implementation: set `implementing` in the first code commit.
- Every step done and the proof passes: set `implemented` in the last code commit.
- Stopping for good (abandoned, superseded, blocked): set `halted (<reason>)` and commit it.

Asked to implement an existing `plan.md`: read its status first. `approved` → go. `implementing` → another session may be on it; ask before resuming. `implemented` → tell the user it is already done. `draft` or `halted` → stop and ask.
