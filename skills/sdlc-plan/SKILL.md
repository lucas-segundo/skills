---
name: sdlc-plan
description: Turns a task, or an accepted spec.md and intent.md when they exist, into an implementation plan of the AI-native SDLC, saved as .md files in the repo for other agents to execute: reads the code read-only, interviews the engineer with AskUserQuestion, stress-tests the plan, and saves it once the engineer approves. Does not use plan mode and does not implement. Use when the user says "write a plan", "plan the implementation", or "turn the spec into a plan". Works with or without an intent or spec.
---

# Planning implementation

Stage 3 (Build) of the AI-native SDLC. Previous (optional): `sdlc-spec`. Intent and spec are not required.

This skill writes a plan; it never implements it. The plan is saved as a `.md` file so another agent, with no access to this conversation, can execute it. Do not call `EnterPlanMode` or `ExitPlanMode`.

Steps 1–6 are **read-only**: only read, search and run read-only commands. No edits, writes, installs, migrations or commits in the repo. Drafts live outside the repo (the session scratchpad, or `/tmp` if there is none) until step 7.

Copy this checklist and tick it off:

```
- [ ] 1. Load inputs (spec and intent if they exist)
- [ ] 2. Read the codebase
- [ ] 3. Interview the engineer
- [ ] 4. Write the plan
- [ ] 5. Stress-test the plan
- [ ] 6. Cold-agent check
- [ ] 7. Get approval and save
```

## Asking questions

Ask every question with **AskUserQuestion**, never as chat text: batch the ones you can ask now, recommendation first, and wait for the answers instead of assuming a default. If the tool is missing or errors, ask in chat as a numbered list, each with your recommended answer, and end the turn.

## 1. Load the inputs

Intent and spec are optional. Use the change folder the user names. Otherwise list `docs/changes/*/` and ask which one, or whether this is a new change.

- **`spec.md` exists:** read it (and `intent.md` if present). **If its status is not `accepted`, stop** and tell the user to accept it first (`/sdlc-spec`), unless they say to plan without it.
- **No spec:** work from what the user described (or a ticket/link they give). Ask what is needed to pin down the goal and scope.

## 2. Read the codebase

Find every file the change touches, the existing patterns to follow, the test setup and the commands to run tests and lint (`CLAUDE.md`/`AGENTS.md`, `package.json`, CI config). Verify file paths exist; mark new files as `(new)`.

## 3. Interview

Ask the engineer what the code cannot tell you: preferred approach where several fit, rollout (flag, migration, backfill), test depth, anything off-limits. Skip questions the code already answers. Keep asking rounds until nothing the plan depends on is assumed.

## 4. Write the plan

Use [plan-template.md](plan-template.md). Status: `ready`. Write drafts to the scratchpad.

- Every requirement in the spec (`R1`...) maps to at least one step and one proof. List any that do not and ask about them. With no spec, list the goals you derived from the user at the top of the plan and number them `R1`... so steps and proof can map to them.
- Steps are ordered so each one leaves the code working and testable.
- Snippets on the key and risky steps let the engineer judge the approach before approving (see the template).
- Proof names concrete tests (file and what they assert) and the commands that run them.

## 5. Stress-test

Answer these in the plan's **Risks** and **Alternatives not taken** sections:

- What could this change break? (callers, data, performance, other teams)
- Which step is most risky, and how is that risk reduced?
- Which other approaches were rejected, and why?

Then ask the engineer about the riskiest points, one question each: options are the mitigations you see (recommended first) and "Accept as is". Revise and repeat until they have no changes.

## 6. Cold-agent check

Re-read the plan as an agent that never saw this conversation and will execute only it. Could it implement the change from the plan alone? If anything relies on chat context, write it into the plan.

## 7. Get approval and save

When planning is finished, send the draft plan file to the engineer for review. Never paste the plan into the chat: give the full absolute path of the draft `.md` in the scratchpad (one line, nothing else about its content), then ask with AskUserQuestion: "Approve and save this plan?" with options "Approve and save (Recommended)" and "Revise". Wait for the answer; do not save or continue before it arrives. Only an explicit approval accepts the plan. "Revise": ask what to change, update the draft file, send its path again, and wait again. Repeat until approved. If a subagent drafted the plan, its output is a draft: the engineer reviews it here, never the subagent.

On approval, save to the change folder:

Save to `docs/changes/<folder>/plan.md`.

- No change folder yet: create `docs/changes/<YYYY-MM-DD>-<slug>/` (today's date, slug 2–5 kebab-case words from the title). If it already exists, ask whether to update it or pick a new slug.

Leave the files uncommitted. Tell the user the plan paths and stop. Do not start implementing.
