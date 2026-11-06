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

Ask every question with **AskUserQuestion**, never as chat text: batch the ones you can ask now, recommendation first, and wait for the answers instead of assuming a default. If the tool is missing or errors, ask in chat as a numbered list, each with your recommended answer, and end the turn.

## 1. Load the intent

Use the `intent.md` the user names. Otherwise list `docs/changes/*/intent.md` and ask which one.

**If its status is not `accepted`, stop.** Tell the user to accept it first (`/sdlc-intent`).

## 2. Ask which policy skills apply

Use AskUserQuestion with `multiSelect: true` to ask which skills or policy documents constrain this spec. Offer up to 3 available skills that look relevant (for example brand, security, UX, architecture or coding skills) plus "None"; the user names others via "Other". Load each one they name. Do not pick skills on your own. If they pick None, continue without; write "Policy skills applied: None" as the first line of Design.

Treat every loaded skill as a hard constraint on the spec, not a suggestion.

## 3. Read the codebase

Read only what the change touches: entry points, the modules and APIs named in the intent, existing patterns for similar features, `CLAUDE.md`/`AGENTS.md`. The spec must fit the code that exists.

## 4. Write spec.md

Build the spec from this prompt, from the playbook, with the intent attached and the policy skills from step 2 loaded. There is no template: the prompt decides the content.

> Read the attached intent.md and produce a requirements and design spec for integrating it into our existing codebase. Apply the skills available to you so the plan conforms to our brand guidelines, security policies and UX standards. Document the spec fully as spec.md, ready to hand to the engineering team. Describe clearly any areas of concern, especially where you cannot satisfy contradicting policies.

Save it next to the intent: `docs/changes/<folder>/spec.md`. Start it with `# Spec: <title>` and `Author: <name>. Status: draft.`

- Number the requirements (`R1`, `R2`...) so the plan can cite them.
- Carry every open question from the intent forward, answered or still open. None is dropped silently.
- Name the area of concern behind each policy, and where two policies contradict. Do not change the intent; if it looks wrong, flag it.

## 5. Review

Show the spec. Go through the areas of concern first, one question per concern, up to 4 per call; options are the resolutions you see (recommended first), "Accept the risk" and "Someone else decides" (they name who). Then ask, in one call: does the spec solve the stated problem? Are all open questions answered or carried? Apply fixes and repeat.

## 6. Accept

Ask with AskUserQuestion: "Accept spec.md?" with options "Accept" and "Keep editing". The spec is accepted only when the user picks Accept or says so; unresolved flagged concerns must be resolved or explicitly accepted first. Then set `Status: accepted`. Tell the user the next step is `/sdlc-plan`. Do not start it yourself.
