---
name: sdlc-spec
description: Turns an accepted intent.md into spec.md, the requirements and design spec of the AI-native SDLC, applying the policy skills the user names and flagging concerns. Leaves the spec uncommitted for the user. Use when the user says "write a spec", "draft spec.md", "spec this out", or "turn the intent into a spec".
---

# Writing specs

Stage 2 (Design) of the AI-native SDLC. Previous: `sdlc-intent`. Next: `sdlc-plan`.

Never commit, stage or offer to commit `spec.md`; what to do with it is the user's call.

Copy this checklist and tick it off:

```
- [ ] 1. Load the accepted intent
- [ ] 2. Ask which policy skills apply
- [ ] 3. Read the codebase
- [ ] 4. Write spec.md
- [ ] 5. Review with the user, concerns first
- [ ] 6. Accept (only on the user's word)
```

## Asking questions

Every question in this skill goes through the **AskUserQuestion** tool, never as a text block in chat:

- Batch the questions you can ask now into one call (at most 4 per call; split a larger batch across consecutive calls). A question that depends on an answer you have not heard yet waits for the next call.
- Per question: `header` a short title; `question` self-contained (name the thing asked about, since earlier chat may be hidden while the dialog is open); `options` 2–4 plausible answers, your recommended one first and labelled "(Recommended)". The user can always pick "Other" for free text.
- After each call, wait for the answers. Never answer for the user or carry on with an assumed default.
- If AskUserQuestion is missing or errors, ask the same questions in chat as a numbered list, each with your recommended answer, then end the turn and wait for the reply.

## 1. Load the intent

Use the `intent.md` the user names. Otherwise list `docs/changes/*/intent.md` and ask which one with the AskUserQuestion tool.

**If its status is not `accepted`, stop.** Tell the user to accept it first (`/sdlc-intent`).

## 2. Ask which policy skills apply

Use AskUserQuestion with `multiSelect: true` to ask which skills or policy documents constrain this spec. Offer up to 3 available skills that look relevant (for example brand, security, UX, architecture or coding skills) plus "None"; the user names others via "Other". Load each one they name. Do not pick skills on your own. If they pick None, continue without; record "None" in the spec header.

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

Show the spec. Go through **Flagged concerns** first, one question per concern, up to 4 per call; options are the resolutions you see (recommended first), "Accept the risk" and "Someone else decides" (they name who). Then ask, in one call: does the spec solve the stated problem? Are all open questions answered or carried? Apply fixes and repeat.

## 6. Accept

Ask with AskUserQuestion: "Accept spec.md?" with options "Accept" and "Keep editing". The spec is accepted only when the user picks Accept or says so; unresolved flagged concerns must be resolved or explicitly accepted first. Then set `Status: accepted`. Tell the user the next step is `/sdlc-plan`. Do not start it yourself.
