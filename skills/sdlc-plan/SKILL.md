---
name: sdlc-plan
description: Turns a task, or an accepted spec.md and intent.md when they exist, into the implementation plan of the AI-native SDLC, in plan mode when available or read-only without it: reads the code, interviews the engineer with AskUserQuestion, stress-tests the plan, then, once the engineer approves it, implements it. Use when the user says "write a plan", "plan the implementation", or "turn the spec into a plan". Works with or without an intent or spec.
---

# Planning implementation

Stage 3 (Build) of the AI-native SDLC. Previous (optional): `sdlc-spec`. Intent and spec are not required.

Steps 1–7 are **read-only**: edit nothing in the repo until the engineer approves the plan in step 8. Plan mode enforces this when it is available; without it, you enforce it yourself. Do not save the plan to the repo unless the user asks.

Copy this checklist and tick it off:

```
- [ ] 1. Start read-only (plan mode if available)
- [ ] 2. Load inputs (spec and intent if they exist)
- [ ] 3. Read the codebase
- [ ] 4. Interview the engineer
- [ ] 5. Write the plan
- [ ] 6. Stress-test the plan
- [ ] 7. Cold-engineer check
- [ ] 8. Get approval
- [ ] 9. Implement
```

## Asking questions

Every question in this skill goes through the **AskUserQuestion** tool, never as a text block in chat:

- Batch the questions you can ask now into one call (at most 4 per call; split a larger batch across consecutive calls). A question that depends on an answer you have not heard yet waits for the next call.
- Per question: `header` a short title; `question` self-contained (name the thing asked about, since earlier chat may be hidden while the dialog is open); `options` 2–4 plausible answers, your recommended one first and labelled "(Recommended)". The user can always pick "Other" for free text.
- After each call, wait for the answers. Never answer for the user or carry on with an assumed default.
- If AskUserQuestion is missing or errors, ask the same questions in chat as a numbered list, each with your recommended answer, then end the turn and wait for the reply.

## 1. Start read-only

Call `EnterPlanMode`. Already in plan mode: carry on. The user declines: stop and ask how they want to proceed.

If `EnterPlanMode` is unavailable or the project does not allow plan mode, work without it: from here until step 8, only read, search and run read-only commands. No edits, writes, installs, migrations or commits in the repo.

## 2. Load the inputs

Intent and spec are optional. Use the change folder the user names. Otherwise list `docs/changes/*/` and ask which one, or whether this is a new change.

- **`spec.md` exists:** read it (and `intent.md` if present). **If its status is not `accepted`, stop** and tell the user to accept it first (`/sdlc-spec`), unless they say to plan without it.
- **No spec:** work from what the user described (or a ticket/link they give). Ask what is needed to pin down the goal and scope.

## 3. Read the codebase

Find every file the change touches, the existing patterns to follow, the test setup and the commands to run tests and lint (`CLAUDE.md`/`AGENTS.md`, `package.json`, CI config). Verify file paths exist; mark new files as `(new)`.

## 4. Interview

Ask the engineer what the code cannot tell you: preferred approach where several fit, rollout (flag, migration, backfill), test depth, anything off-limits. Skip questions the code already answers. Keep asking rounds until nothing the plan depends on is assumed.

## 5. Write the plan

Use [plan-template.md](plan-template.md). Status: `not executed`.

- In plan mode, write it to the plan file the harness assigned.
- Without plan mode, write it outside the repo (the session scratchpad, or `/tmp` if there is none) and show it in chat.
- Every requirement in the spec (`R1`...) maps to at least one step and one proof. List any that do not and ask about them. With no spec, list the goals you derived from the user at the top of the plan and number them `R1`... so steps and proof can map to them.
- Steps are ordered so each one leaves the code working and testable.
- Proof names concrete tests (file and what they assert) and the commands that run them.

## 6. Stress-test

Answer these in the plan's **Risks** and **Alternatives not taken** sections:

- What could this change break? (callers, data, performance, other teams)
- Which step is most risky, and how is that risk reduced?
- Which other approaches were rejected, and why?

Then ask the engineer about the riskiest points, one question each: options are the mitigations you see (recommended first) and "Accept as is". Revise and repeat until they have no changes.

## 7. Cold-engineer check

Re-read the plan as an engineer who never saw this conversation. Could they implement the change from the plan alone? If anything relies on chat context, write it into the plan.

## 8. Get approval

- **In plan mode:** call `ExitPlanMode`. The engineer's approval accepts the plan. If they reject it, revise in plan mode and call `ExitPlanMode` again.
- **Without plan mode:** ask with AskUserQuestion: "Approve this plan and start implementing?" with options "Approve and implement (Recommended)", "Approve, save to repo, don't implement yet" and "Revise". Only an explicit approval accepts the plan. "Revise": ask what to change, revise, and ask again. "Don't implement yet": save the plan where the user says, then stop.

## 9. Implement

Implement the plan in its order of work, running the proof commands as each step completes. When every step is done and the proof passes, set the plan's `Status: executed`.
