---
name: planning
description: Turns a task, ticket or bug into plan.md, an implementation plan organized by order of work (each step with its own files, risks and proof) for other agents to execute; then optionally implements it. Use when the user says "write a plan" or "plan the implementation".
---

# Planning implementation

Write a plan another agent, with no access to this conversation, can execute step by step. Organize it **by order of work**: each step holds its own files, change, risks and proof; no top-level Files, Risks or Proof sections.

Call `EnterPlanMode` first (skip if already in it). Keep the draft in the plan mode file or the scratchpad until approval. Ask every question with **AskUserQuestion**, batched, recommendation first, and wait for answers instead of assuming.

## 1. Goal and code

- Pin down goal and scope from the task, ticket or link. Number the goals `R1`, `R2`...
- Find the files the change touches; verify paths, mark new ones `(new)`, and note how they depend on each other.

## 2. Order of work

Take the order from `AGENTS.md` or `CLAUDE.md` (repo root and touched folders), then `CONTRIBUTING.md`, and quote the rule in the plan's `Order:` line. If none sets one, use this default, adapted, and write `Order: default: <reason>`:

1. Failing test (bug fix)
2. Data: schema, migrations, backfills, backward compatible
3. Contracts and shared code: types, interfaces, API schemas, helpers
4. Backend: domain logic, services, endpoints
5. Client: API client, state, data fetching
6. UI: components, then pages
7. Wiring: routes, nav, feature flags, config, permissions
8. Cleanup: dead code, docs

Always: dependencies before dependents; riskiest unknown as early as dependencies allow; user-visible behavior turned on last; split steps that touch unrelated layers. Steps need not leave the code building: errors between steps are expected, verification runs once at the end.

## 3. Interview

Ask what the code cannot tell you: approach where several fit, rollout, test depth, anything off-limits. If the default order was used, show the step list and ask to keep it. Always ask which writing skills to follow (multi-select of the available ones, those matching the files recommended, plus "None"). Repeat until nothing is assumed.

## 4. Write the plan

Follow [plan-template.md](plan-template.md): header, `## Goals`, one `## Step N` per step in order, `## Across steps`.

- Every step has Requirements, Depends on, Files, Change, Risks, Proof; write "None" rather than drop one. A file changed in several steps appears in each.
- Every goal maps to at least one step and one proof, citing its id; ask about any that do not.
- Snippets on key and risky steps.
- Proof names the tests the step adds or changes (file, what they assert); for a bug fix, step 1 writes the failing test.
- `## Across steps`: shared risks, rejected approaches, and the final check (typecheck, lint and test commands covering every changed file and proof test).

## 5. Stress-test and cold check

Answer in the plan, in the step it belongs to: what could break (callers, data, performance, other teams), which step is riskiest and how it is reduced, which approaches were rejected and why. Ask the engineer about each risky point (mitigations recommended first, plus "Accept as is") until they have no changes.

Then re-read the plan as an agent that never saw this conversation. If a step relies on chat context or on something a later step creates, fix it.

## 6. Approve, save, implement

Give the draft's full absolute path in one line (never paste the plan), then ask "Approve this plan?": "Approve and save only (Recommended)", "Approve, save and implement", "Revise". Only explicit approval counts; on "Revise" ask what to change, update, and ask again. A subagent's draft is reviewed here too.

On approval, call `ExitPlanMode` (if in plan mode) and save to `docs/changes/<YYYY-MM-DD>-<slug>/plan.md` (slug 2–5 kebab-case words) unless the user names a path; if the folder exists, ask to update or pick a new slug. Do not commit; say committing keeps the audit trail.

- **Save only:** stop.
- **Save and implement:** load the plan's writing skills, then implement **one step at a time**, in order, touching only that step's listed files unless you say why.
  - After each step, stop. Name the step and the files it changed (one line, no diff), then ask "Step N done. Review the changes, then:" with "Approve, start step N+1 (Recommended)", "Revise this step", "Stop here". Never start the next step before an explicit approval. On "Revise", ask what to change, apply it, and ask again.
  - Do not run typecheck, lint or tests between steps; ignore errors from dependents not yet updated.
  - After the last step is approved, run the final check once and fix every failure (fix the code, never the test).
  - Update `plan.md` when the implementation departs from it. Leave changes uncommitted unless asked.
