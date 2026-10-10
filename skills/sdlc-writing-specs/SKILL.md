---
name: sdlc-writing-specs
description: Turns an accepted intent.md into spec.md, the requirements and design spec of the AI-native SDLC, applying the policy skills the user names and flagging concerns. Commits the spec. Use when the user asks to write, draft, or produce a spec or spec.md from an intent. Manual use only.
disable-model-invocation: true
---

# Writing specs

Stage 2 (Design) of the AI-native SDLC. Previous: `intent`. Next: `sdlc-planning-implementation`.

Copy this checklist and tick it off:

```
- [ ] 1. Load the accepted intent
- [ ] 2. Ask which policy skills apply
- [ ] 3. Read the codebase
- [ ] 4. Write spec.md
- [ ] 5. Review with the user, concerns first
- [ ] 6. Commit
- [ ] 7. Accept (only on the user's word)
```

## 1. Load the intent

Use the `intent.md` the user names. Otherwise list `docs/changes/*/intent.md` and ask which one.

**If its status is not `accepted`, stop.** Tell the user to accept it first (`/intent`).

## 2. Ask which policy skills apply

Ask the user which skills or policy documents constrain this spec (for example brand, security, UX, architecture or coding skills). Load each one they name. Do not pick skills on your own. If they name none, confirm and continue without; record "None" in the spec header.

Treat every loaded skill as a hard constraint on the spec, not a suggestion.

## 3. Read the codebase

Read only what the change touches: entry points, the modules and APIs named in the intent, existing patterns for similar features, `CLAUDE.md`/`AGENTS.md`. The spec must fit the code that exists.

## 4. Write spec.md

Use [spec-template.md](spec-template.md). Save it next to the intent: `docs/changes/<folder>/spec.md`. Status: `draft`.

- Requirements say **what** must be true, each testable and numbered (`R1`, `R2`...). Design says **how** it fits the codebase, at the level of components, data and interfaces, not files and steps (that is the plan).
- Every open question from the intent appears under **Open questions**, either answered with the decision or carried forward. None is dropped silently.
- **Flagged concerns** is required. Flag where a policy cannot be met, where two policies contradict, where the intent is ambiguous, and where risk is high. Name the policy (skill) behind each one. Write "None" only if there truly are none.
- Do not change the intent. If the intent looks wrong, flag it.

## 5. Review

Show the spec. Go through **Flagged concerns** first, one at a time; the user resolves each (or names who must). Then ask: does the spec solve the stated problem? Are all open questions answered or carried? Apply fixes and repeat.

## 6. Commit

Commit only `spec.md` with message `docs(sdlc): write spec for <slug>`. Do not push unless the user asks.

## 7. Accept

The spec is accepted only when the user says so; unresolved flagged concerns must be resolved or explicitly accepted first. Then set `Status: accepted` and commit with `docs(sdlc): accept spec for <slug>`. Tell the user the next step is `/sdlc-planning-implementation`. Do not start it yourself.
