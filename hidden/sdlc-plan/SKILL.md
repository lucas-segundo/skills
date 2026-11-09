---
name: sdlc-plan
description: Turns a task, or an accepted spec.md and intent.md when they exist, into an implementation plan saved as plan.md for other agents to execute, then optionally implements it. Use when the user says "write a plan", "plan the implementation", or "turn the spec into a plan".
---

# Planning implementation

Stage 3 (Build) of the AI-native SDLC. Previous (optional): `sdlc-spec`. Intent and spec are not required.

This skill writes a plan. The plan is saved as a `.md` file so another agent, with no access to this conversation, can execute it. Implementing it is optional and only happens if the engineer chooses it in step 7.

**Call `EnterPlanMode` first**, before step 1. If the session is already in plan mode, skip the call.

Drafts live in the plan mode plan file, or the session scratchpad, until step 7.

## Asking questions

Ask every question with **AskUserQuestion**, never as chat text: batch the ones you can ask now, recommendation first, and wait for the answers instead of assuming a default.

## 1. Load the inputs

Intent and spec are optional. Use the change folder the user names. Otherwise list `docs/changes/*/` and ask which one, or whether this is a new change.

- **`spec.md` exists:** read it (and `intent.md` if present). **If its status is not `accepted`, stop** and tell the user to accept it first (`/sdlc-spec`), unless they say to plan without it.
- **No spec:** work from what the user described (or a ticket/link they give). Ask what is needed to pin down the goal and scope.

## 2. Read the codebase

Verify file paths exist; mark new files as `(new)`.

## 3. Interview

Ask the engineer what the code cannot tell you: preferred approach where several fit, rollout (flag, migration, backfill), test depth, anything off-limits. Skip questions the code already answers. Always ask which writing skills the implementation should follow, as a multi-select AskUserQuestion listing the available ones (for example `writing-javascript`, `writing-react`), recommending those that match the files you found in step 2, plus "None". Keep asking rounds until nothing the plan depends on is assumed.

## 4. Write the plan

Use [plan-template.md](plan-template.md), exactly its four sections.

- Every requirement in the spec (`R1`...) maps to at least one step and one proof; cite the ids in the step and the proof text. List any that do not and ask about them. With no spec, list the goals you derived from the user at the top of the plan and number them `R1`... so steps and proof can map to them.
- Name the chosen writing skills in Order of work, so the agent that executes it loads them before writing code.
- Snippets on the key and risky steps let the engineer judge the approach before approving (see the template).
- Proof names concrete tests (file and what they assert) and the commands that run them. For a bug fix, the first step writes the failing test.

## 5. Stress-test

Answer these in the plan's **Risks** section (rejected approaches go there too):

- What could this change break? (callers, data, performance, other teams)
- Which step is most risky, and how is that risk reduced?
- Which other approaches were rejected, and why?

Then ask the engineer about the riskiest points, one question each: options are the mitigations you see (recommended first) and "Accept as is". Revise and repeat until they have no changes.

## 6. Cold-agent check

Re-read the plan as an agent that never saw this conversation and will execute only it. Could it implement the change from the plan alone? If anything relies on chat context, write it into the plan.

## 7. Get approval and save

When planning is finished, send the draft plan file to the engineer for review. Never paste the plan into the chat: give the full absolute path of the draft `.md` (one line, nothing else about its content), then ask once with AskUserQuestion: "Approve this plan?" with options "Approve and save only (Recommended)", "Approve, save and implement" and "Revise". Wait for the answer; do not save or continue before it arrives. Only an explicit approval accepts the plan. "Revise": ask what to change, update the draft file, send its path again, and wait again. Repeat until approved. If a subagent drafted the plan, its output is a draft: the engineer reviews it here, never the subagent.

On either approval, call `ExitPlanMode` to leave plan mode (skip if not in plan mode) and save to the change folder:

Save to `docs/changes/<folder>/plan.md`.

- No change folder yet: create `docs/changes/<YYYY-MM-DD>-<slug>/` (today's date, slug 2–5 kebab-case words from the title). If it already exists, ask whether to update it or pick a new slug.

Do not commit. Tell the user the plan paths, and that committing them keeps the audit trail.

- **Save only:** stop. Do not start implementing.
- **Save and implement:** execute `plan.md` step by step, in order, touching only the files it lists unless you say why. If a test fails, fix the code, never the test. For a bug fix, write the failing test first. Update `plan.md` in the same change whenever the implementation departs from it. Leave the changes uncommitted unless the user asks.
